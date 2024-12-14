from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import requests, sys, io, json, logging
from web3 import Web3
from rest_framework.permissions import AllowAny
from .models import (BeastClass, AquaticClass, PlantClass,
                     BirdClass, BugClass, ReptileClass, MechClass,
                     DawnClass, DuskClass)
from .constants import AXIE_API_URL, INFURA_URL, API_KEY, ABI, CONTRACT_ADDRESS

# Set stdout to use UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Set up logging
logger = logging.getLogger(__name__)

class AxieContractView(APIView):
    permission_classes = [IsAuthenticated]

    def get_web3(self):
        """Create and return a Web3 instance connected to the Ethereum network."""
        w3 = Web3(Web3.HTTPProvider(INFURA_URL))

        # Check connection
        try:
            w3.eth.block_number  # Attempt to get the latest block number
        except Exception as e:
            raise ConnectionError("Failed to connect to Ethereum network: " + str(e))

        return w3

    def get(self, request):
        """
        Handle GET requests to interact with the Axie ERC-20 smart contract.

        This view allows clients to fetch various data from the Axie Infinity 
        smart contract, such as total supply, balance, the name of the token, 
        and the symbol. It determines the action requested via query parameters 
        and calls the corresponding smart contract function.

        Args:
            request: The incoming HTTP request containing query parameters for the action.

        Returns:
            Response: A JSON response with the results requested (e.g., total supply,
            balance, token name, or symbol) or an error message if the action is invalid
            or required parameters are missing.
        """
        try:
            w3 = self.get_web3()  # Establish a connection to the Ethereum network
            contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)  # Create a contract instance

            # Determine which action was requested
            action = request.query_params.get('action')

            if action == 'totalSupply':
                total_supply = contract.functions.totalSupply().call()
                return Response({"total_supply": total_supply})

            elif action == 'balanceOf':
                address = request.query_params.get('address')
                if not address:
                    return Response({"error": "Missing 'address' parameter."}, status=400)
                balance = contract.functions.balanceOf(Web3.to_checksum_address(address)).call()
                return Response({"balance": balance})

            elif action == 'name':
                name = contract.functions.name().call()
                return Response({"name": name})

            elif action == 'symbol':
                symbol = contract.functions.symbol().call()
                return Response({"symbol": symbol})

            else:
                return Response({"error": "Invalid action."}, status=400)

        except Exception as e:
            return Response({"error": str(e)}, status=400)
        
class FetchAxieDataView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Fetch Axie data from Axie Infinity marketplace.

        This view sends a GraphQL query to retrieve axie data including their 
        ID, name, class, stage, and highest offer price in USD. It processes
        the response and updates or creates records in the database.

        Args:
            request: The incoming HTTP request.

        Returns:
            Response: A JSON response with a message indicating success,
            or error details.
        """
        
        # Define the GraphQL query to fetch Axie data
        query_axies = """
        query MyQuery {
            axies(sort: PriceAsc, from: 0, size: 300) {
                results {
                    id
                    name
                    highestOffer {
                        currentPriceUsd
                    }
                    class
                    stage
                }
            }
        }
        """

        # Prepare the payload for the POST request to the Axie API
        payload = {
            "query": query_axies  # The GraphQL query to be sent
        }

        # Set the appropriate headers for the request
        headers = {
            "Content-Type": "application/json",  # Indicate the content type of the request
            "X-API-Key": API_KEY  # Use the correct header for the API key
        }

        try:
            # Send the POST request to the Axie API
            response = requests.post(AXIE_API_URL, json=payload, headers=headers)

            # Log the raw response for debugging
            logger.info("Raw response: %s", response.text)

            # Check for a successful response, raise error for bad responses (4xx or 5xx)
            response.raise_for_status()

            # Parse the response JSON for further processing
            data = response.json()

            # Debugging: Output the structure of the response for insights
            logger.debug("Response JSON: %s", json.dumps(data, indent=2, ensure_ascii=False))

            # Validate if 'data' and 'axies' keys are present in the response
            if 'data' not in data or 'axies' not in data['data']:
                return Response({"error": "Invalid data structure returned."}, status=500)

            # Extract the list of Axies from the response
            axies = data['data']['axies']['results']

            # Check if there are any Axies found in the response
            if not axies or not isinstance(axies, list):
                return Response({"error": "No Axies found or invalid structure."}, status=404)

            # Mapping of Axie class names to Django model classes
            class_models = {
                "Beast": BeastClass,
                "Aquatic": AquaticClass,
                "Plant": PlantClass,
                "Bird": BirdClass,
                "Bug": BugClass,
                "Reptile": ReptileClass,
                "Mech": MechClass,
                "Dawn": DawnClass,
                "Dusk": DuskClass,
            }

            # Loop through the result set of Axies and save them to the database
            for axie in axies:
                # Access Axie attributes directly
                axie_id = axie['id']  # Unique identifier for the Axie
                name = axie['name']    # Name of the Axie
                axie_class = axie['class']  # Class type of the Axie
                stage = axie['stage']  # Current stage of the Axie

                # Determine the current price in USD, handle if highestOffer is not available
                current_price_usd = axie['highestOffer']['currentPriceUsd'] if 'highestOffer' in axie and axie['highestOffer'] else 0

                # Retrieve the model class based on the Axie class name
                model = class_models.get(axie_class)
                if model:
                    # Use update_or_create to update existing records or create new ones
                    model.objects.update_or_create(
                        axie_id=axie_id,  # Use the axie_id to detect duplicates
                        defaults={
                            'name': name,  # Update or set the Axie's name
                            'stage': stage,  # Update or set the Axie's stage
                            'current_price_usd': current_price_usd,  # Update or set the price in USD
                        }
                    )

            # Return a success message after processing
            return Response({"message": "Axie data processed successfully!"})

        except requests.exceptions.HTTPError as http_err:
            return Response({"error": f"Error in fetching Axies: {http_err}"}, status=400)
        except KeyError as e:
            return Response({"error": f"Missing key in response data: {str(e)}"}, status=500)
        except Exception as err:
            return Response({"error": f"An error occurred: {err}"}, status=500)
    
class GetAxieDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve all Axie classes and their data.

        This view fetches Axie data for multiple classes including Beast, Aquatic, 
        Plant, Bird, Bug, Reptile, Mech, Dawn, and Dusk. It aggregates the data 
        from the corresponding Django model and returns it as a JSON response.

        Args:
            request: The incoming HTTP request.

        Returns:
            Response: A JSON response containing a dictionary with the Axie class data.
            The dictionary contains the following keys:
                - beast_class: List of Axies belonging to the Beast class.
                - aquatic_class: List of Axies belonging to the Aquatic class.
                - plant_class: List of Axies belonging to the Plant class.
                - bird_class: List of Axies belonging to the Bird class.
                - bug_class: List of Axies belonging to the Bug class.
                - reptile_class: List of Axies belonging to the Reptile class.
                - mech_class: List of Axies belonging to the Mech class.
                - dawn_class: List of Axies belonging to the Dawn class.
                - dusk_class: List of Axies belonging to the Dusk class.
        """
        
        # Create a dictionary to hold Axie data for each class
        axie_data = {
            "beast_class": list(BeastClass.objects.all().values()),
            "aquatic_class": list(AquaticClass.objects.all().values()),
            "plant_class": list(PlantClass.objects.all().values()),
            "bird_class": list(BirdClass.objects.all().values()),
            "bug_class": list(BugClass.objects.all().values()),
            "reptile_class": list(ReptileClass.objects.all().values()),
            "mech_class": list(MechClass.objects.all().values()),
            "dawn_class": list(DawnClass.objects.all().values()),
            "dusk_class": list(DuskClass.objects.all().values()),
        }

        # Return the assembled Axie data as a JSON response
        return Response(axie_data)

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        """
        Handle user registration via POST request.

        This view allows a new user to register by providing a username 
        and password. If the username already exists, an error is returned. 
        Upon successful registration, a new user is created and an 
        authentication token is generated.

        Args:
            request: The incoming HTTP request containing the username and password.

        Returns:
            Response: A JSON response containing the authentication token 
            if registration is successful, or an error message with the 
            appropriate status code if the username already exists or 
            if the required data is not provided.
        """
        username = request.data.get('username')
        password = request.data.get('password')
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)
    
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        """
        Handle user login via POST request.

        This view allows a user to log in by providing a username and 
        password. If the credentials are valid, it returns an authentication 
        token. If the credentials are invalid, an error message is returned.

        Args:
            request: The incoming HTTP request containing the username and password.

        Returns:
            Response: A JSON response containing the authentication token 
            if login is successful, or an error message with the 
            appropriate status code if the credentials are invalid.
        """
        
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Invalid credentials."}, status=400)
