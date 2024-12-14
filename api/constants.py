from web3 import Web3
from dotenv import load_dotenv
import os
load_dotenv()
AXIE_API_URL = os.getenv("AXIE_API_URL_ENV") #Axie api url env from https://developers.skymavis.com/
INFURA_URL = os.getenv("INFURA_URL_ENV") #Infura api url and key 
API_KEY = os.getenv("API_KEY_ENV") #Axie api key from https://developers.skymavis.com/
CONTRACT_ADDRESS = Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS_ENV"))

ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "pure",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "pure",
        "type": "function"
    },
]