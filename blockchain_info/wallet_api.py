import json

import requests
from .utils import add_if_present
# Assuming you have the local wallet service running on default port 3000

API_BASE_URL = "http://localhost:3000/api/v2"
MERCHANT_BASE_URL = "http://localhost:3000/merchant/{}"

# Full wallet API documentation: https://blockchain.info/api/blockchain_wallet_api


def create_wallet(password, api_code, private_key=None, label=None, email=None):
    """
    :param password: Password for the new wallet
    :param api_code: Api code with permissions to create wallets
    :param private_key: (optional) Private key to add to the wallet
    :param label: (optional) A label to set for the first address in the wallet
    :param email: (optional) Email to associate with the wallet
    :return:
        {
            "guid": "4b8cd8e9-9480-44cc-b7f2-527e98ee3287",
            "address": "12AaMuRnzw6vW6s2KPRAGeX53meTf8JbZS",
            "label": label
        }
    """
    create_wallet_url = "{}/create".format(API_BASE_URL)
    create_wallet_body = {
        "password": password,
        "api_code": api_code
    }
    add_if_present("priv", private_key, create_wallet_body)
    add_if_present("label", label, create_wallet_body)
    add_if_present("email", email, create_wallet_body)
    response = requests.post(create_wallet_url, json=create_wallet_body)
    return response.json()

def merchant_url(guid):
    return MERCHANT_BASE_URL.format(guid)

def wallet_balance(guid, wallet_password):
    """Fetch the balance of the wallet. Includes unconfirmed transactions and possibly double spends

    :param guid: Unique identifier of the wallet
    :param wallet_password: The wallet password
    :return: { "balance": 1000}
    """
    list_balance_url = "{}/balance".format(merchant_url(guid))
    response = requests.get(list_balance_url, params={"password": wallet_password})
    return response.json()

def list_wallet_adresses(guid, wallet_password):
    """Fetch all addresses of the wallet.

        :param guid: Unique identifier of the wallet
        :param wallet_password: The wallet password
        :return: {
                    "addresses": [
                        {
                            "balance": 1400938800,
                            "address": "1Q1AtvCyKhtveGm3187mgNRh5YcukUWjQC",
                            "label": "Deposits",
                            "total_received": 5954572400
                        },
                    ]
                }
        """
    list_addresses_url = "{}/list".format(merchant_url(guid))
    response = requests.get(list_addresses_url, params={"password": wallet_password})
    return response.json()

def create_transaction(guid, main_password, recipient, amount, from_=None, second_password=None, fee=None):

    """ Creates a transaction

    :param guid: Unique identifier of the wallet
    :param main_password: Main wallet password
    :param recipient: Recipient of funds
    :param amount: Amount of funds to transfer
    :param from_: (optional) Address of the sender of the funds
    :param second_password: (optional) Second password if double encryption is enabled
    :param fee: (optional) Transaction fee in satoshi (Must be greater than default fee of 0.0001)
    :return: { "message" : "Response Message" , "tx_hash": "Transaction Hash", "notice" : "Additional Message" }
    """
    params = {
        "main_password": main_password,
        "to": recipient,
        "amount": amount
    }
    add_if_present("from", from_, params)
    add_if_present("second_password", second_password, params)
    add_if_present("fee", fee, params)

    full_url = "{}/payment".format(merchant_url(guid))
    response = requests.get(full_url, params=params)
    return response.json()



