import json
from web3 import Web3
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from ".env" file
# Code of your application, which uses environment variables (e.g. from `os.environ` or `os.getenv`) as if they came from the actual environment.
install_solc("0.6.0")

with open("./SimpleStorage.sol", "r") as file:
    # here we are reading briefly and naming it as file
    simple_storage_file = file.read()  # here we are reading all contents
    # print(simple_storage_file)


# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)
# print(compiled_sol)

with open("compiled_code.json", "w") as file:
    json.dump(
        compiled_sol, file
    )  # the above "w" is for writing "compiled_code.json" as file
    # here "json.dump" just take our "compiled_code.json" variable and dump it to the "file" but in the "json-format"

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]
# print(bytecode)

# get abi
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]
# print(abi)

# Now we will be going to deploy this on simulated or fake blockchain network i.e "Ganache",
# Earlier we are doing the same on the "javascriptVM" in RemixIDE i.e fake blockchain...
# for knowing more about the providers we should visit here "https://web3py.readthedocs.io/en/stable/providers.html" in web3py documentation

# For connecting to ganache
# w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
# here in Ganache's fake blockchain instance we have the "RPC Server URL", Recall in RemixIDE we are using Metamask directly to connect to the blockchain...
# chain_id = 1337
# my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"  # Same as we saw fake account in RemixIDE
# private_key = os.getenv("PRIVATE_KEY")
# print(private_key)
# Always remember to put "0x" in front of Account_Address and Private_Key while working with web3py as python always wants "hexadecimal representation" of private key
# REMEMBER! it's a bad practise and risky to put our private key in the public github repositories for this we had to set environment variables...
# IMPORTANT:- but the environment variable we set using export method only work for the duration our shell is live...
# So, when we close out of our shell we have to re-run the export command:-(i.e "export PRIVATE_KEY=0xc33e0759c42ee88deaf3d104dbbbc7e234126ca991319ffa53d9377d4861eed0")
# hence we now learn a way to set our environment variable so that we not need to re-run the export command
# We would learn more effective way to set our environment variable when we learn "BROWNIE"

# For connecting to metamask's rinkeby test network for our original account
w3 = Web3(Web3.HTTPProvider(os.getenv("RINKEBY_RPC_URL")))
chain_id = 4
# Also known as "NetworkID" and we can check this from "https://chainlist.org/"
my_address = "0xFe63c8dE1b9A79E4EA5c740F4bFe62ADFb26dc8B"
private_key = os.getenv("ORIGINAL_PRIVATE_KEY")

# Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# print(SimpleStorage)
# for more details about this new "...datatypes.Contracts" checkout the this documentation of web3py:- "https://web3py.readthedocs.io/en/stable/contracts.html"

# Now for deploying all the above thing we have to build a "TRANSACTION" and for this we have to:-
# 1. Build the Contract Deploy(i.e Transaction)
# 2. Sign in the Transaction
# 3. Send the Transaction

# Remember we have learn little about the "Nonce" in the "Blockchain Demo" view it here:-"https://andersbrownworth.com/blockchain/block"
# There we used "Nonce" to solve the answer for a really difficult mining problem..
# In cryptography, a "nonce" is an arbitrary number that can be used just once in a cryptographic communication.
# But here "nonce" means number of transaction our account had made every time we make another transaction our transaction is hashed with a new "nonce"...
# this is what going behind the scene with our transaction and we need this to send our transaction and we can actually get our nonce by just grabbing our latest transaction
# which we can see in the activity section of our metamask account about the recent transaction on the "etherscan" after every transaction which we had learned earlier
# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
# print(nonce)
# here we would get "nonce = 0" as we had'nt did any transaction

# Submit the transaction that deploys the contract(i.e doing a transaction)
# Remember every contract technically have at least an implied constructor but our SimpleStorage.sol is blank (i.e doesn't have any constructor)
# but in our "FundMe.sol" which we created in RemixIDE have constructor.

# 1. Build the Contract Deploy(i.e Transaction)
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)
# here we have to give some Transaction Parameters(that we can see above) atleast couple of parameters while using web3.py
# print(transaction)

# As we had seen in the "BlockChain Demo:Signatures" view it here:-"https://andersbrownworth.com/blockchain/public-private-keys/signatures"
# So, there our "Private Key" will be the only Key to sign-in to the Message that was defining how to "deploy simple_storage"...
# ...so as to create unique "Message Signature", hence, anybody else in the network can verify that it was us who signed it.

# 2. Sign in the Transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# print(signed_txn)
# Here we are doing the same as we did in the case of Blockchain Demo: Transaction to a Blank account number
# view it here:- "https://andersbrownworth.com/blockchain/public-private-keys/transaction"

# 3. Send the above signed Transaction
print("Deploying Contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# After running we can view this transaction on our Ganache GUI's Transaction part
# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

# Working with Contracts, we always need:-
# Contract Address
# Contract ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Making Transaction(i.e Interaction) in a Blockchain can be done in two different ways:-
# 1. Interact with a Call--> this is for Simulating the call and getting a return value
# ("Calls don't make a state change to the Blockchain" which is similar to how in Remix we would call...
# ...the "BLUE buttons"(i.e Call in Remix) and "ORANGE buttons"(i.e Transact in Remix) and nothing on blockchain gets changed)
# 2. Interact with a Transact--> Actually make a state change
# Now just update the "favoriteNumber" using "store()" in SimpleStorage.sol file (of RemixIDE)

# Initial value of favoriteNumber
# print(simple_storage.functions.retrieve().call())
# print(simple_storage.functions.store(15).call())
# After doing some changes in the "store()" so that it can return some value which was assigned to it in "SimpleStorage.sol" file
# And if we go to the Ganache GUI we will see whole bunch of different Transactions but none of these are contract interactions...
# that's because when we call a function we just "simulate" working with it.
# So if we call retrieve() again right afterwards we'll see that it's still Zero...
# print(simple_storage.functions.retrieve().call())
# So, let's actually build a new transaction to actually store some value  into this contract...
print(f"Initial Stored Value {simple_storage.functions.retrieve().call()}")
print("Updating Contract...")
# 1. Build the Contract Deploy(i.e Transaction)
greeting_transaction = simple_storage.functions.store(15).buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce + 1}
)
# here in above code we write "nonce +1" because we already used "nonce" when we created our initial "transaction"
# REMEMBER! a "nonce" can only be used for each transaction, so "greeting_transaction" would have to have different nonce than the nonce we used to deploy the initial "transaction" contract

# 2. Sign in the Transaction
signed_greeting_txn = w3.eth.account.sign_transaction(
    greeting_transaction, private_key=private_key
)

# 3. Send the above signed Transaction
tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
print("Updating stored Value...")

# Waiting for the transaction to finish
tx_greeting_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
print(f"Done! Contract deployed to {tx_greeting_receipt.contractAddress}")
print("Updated!")
print(simple_storage.functions.retrieve().call())

# Now we will use Ganache CLI...because "Brownie" uses nodejs in the backend also CLI provides more functionality to code...
"""
So, here we have to write our own "compile code" and our own "storage code" is going to take lots of work and also if we want to interact to one o the contract that we had deployed in the past,
well for that we had to keep track of all those addresses and manually update our address features here with an address, maybe we didin't want to deploy a new contract every single time, 
maybe we just want to work with the contracts that we've already deployed, what if we want to work with a whole bunch of different chains (i.e we want to work with Rinkeby, Mainnet and our own local network)
there seems to be a lot to manage here and we still haven't even talked about writing tests...this is where "Brownie" come into play. 
Brownie is currently the most popular Smart Contract Development Platform build based on Python. It's currently used by Defi giants such as "yearn.finance", "curve.fi", "badger.finance".
"""
