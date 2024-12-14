# Gig Rewards Web Application

This project is a web application built using Django, Django REST Framework, and MongoDB as the database. It serves to fetch and manage Axie data from the Axie Infinity marketplace.

## Table of Contents
- [Installation](#installation)
- [Setting Up the Database](#setting-up-the-database)
- [Running the Application](#running-the-application)
- [Handling Encoding Issues](#handling-encoding-issues)
- [Endpoints](#endpoints)

## Installation

### Required Software
1. **Python**: Ensure Python 3.x is installed on your machine. You can download it from [python.org](https://www.python.org/downloads/).
2. **Pip**: Usually comes with Python, but you can check by running `pip --version` in the command prompt or terminal.
3. **MongoDB**: Install MongoDB by following this link: [MongoDB Installation](https://www.mongodb.com/try/download/community).
4. **Git**: If you don't have Git installed, download it from [git-scm.com](https://git-scm.com/downloads).
5. **Postman**: Optionally, download Postman from [postman.com](https://www.postman.com/downloads/) for API testing.

### Clone the Repository
```bash
git clone https://github.com/jerome2525/gig_rewards.git
cd gig_rewards
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Setting Up the Database

### Run MongoDB Locally
To run the MongoDB server, execute the following command in your terminal or command prompt:
```bash
"C:\Program Files\MongoDB\Server\8.0\bin\mongod.exe"
```

## Running the Application

### Database Migrations
If the project has migrations, run these commands to apply them:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Start the Development Server
Start the Django development server to see the application in action:
```bash
python manage.py runserver
```

## Handling Encoding Issues
If you encounter the error `UnicodeEncodeError: 'charmap' codec can't encode character '\u8349'`, it indicates an encoding issue when printing characters not supported by your console's default encoding. This often occurs in Windows environments.

To solve this issue, open your terminal and run:
```bash
chcp 65001
```

## Endpoints

### User Registration
- **Endpoint**: `http://127.0.0.1:8000/api/register/`
- **Method**: POST
- **Description**: Register a new user.
- **Request Body**:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```

### User Login
- **Endpoint**: `http://127.0.0.1:8000/api/login/`
- **Method**: POST
- **Description**: Log in an existing user to retrieve an authentication token.
- **Request Body**:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```

### Fetch Axie Data
- **Endpoint**: `http://127.0.0.1:8000/api/fetch-axie-data/`
- **Method**: POST
- **Description**: Fetches Axie data from the Axie Infinity marketplace.
- **Request Body**: No specific fields required.

### Get Stored Axie Data
- **Endpoint**: `http://127.0.0.1:8000/api/get-axie-data/`
- **Method**: GET
- **Description**: Retrieves stored Axies from the database, categorized by class.
- **Request Body**: None.

### Get Smart Contract Data
- **Endpoint**: `http://127.0.0.1:8000/api/get-smart-contract-data/`
- **Method**: GET
- **Description**: Retrieves data from the Ethereum smart contract associated with the Axie Infinity marketplace.
- **Query Parameters**:
  - `action` (required): Specifies the action to perform. Supported values are:
    - `totalSupply`: Retrieves the total supply of the token.
    - `balanceOf`: Retrieves the balance of a specified address. Requires an additional parameter `address`.
    - `name`: Retrieves the name of the token.
    - `symbol`: Retrieves the symbol of the token.
  - `address` (optional): Required only if `action=balanceOf`. Specifies the Ethereum address to query.
- **Examples**:
  1. Fetch total supply:
     ```bash
     http://127.0.0.1:8000/api/get-smart-contract-data/?action=totalSupply
     ```
  2. Fetch balance for an address:
     ```bash
     http://127.0.0.1:8000/api/get-smart-contract-data/?action=balanceOf&address=0xYourEthereumAddress
     ```
  3. Fetch token name:
     ```bash
     http://127.0.0.1:8000/api/get-smart-contract-data/?action=name
     ```
  4. Fetch token symbol:
     ```bash
     http://127.0.0.1:8000/api/get-smart-contract-data/?action=symbol
     ```

