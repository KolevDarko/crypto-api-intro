import requests

from coinbase.authentication import CoinbaseExchangeAuth

API_URL = 'https://api.gdax.com/'
API_KEY = ''
API_SECRET = ''
API_PASS = ''

auth = CoinbaseExchangeAuth(API_KEY, API_SECRET, API_PASS)

def get_accounts():
    """
    List all user accounts
    :return: [
        {
            "id": "71452118-efc7-4cc4-8780-a5e22d4baa53",
            "currency": "BTC",
            "balance": "0.0000000000000000",
            "available": "0.0000000000000000",
            "hold": "0.0000000000000000",
            "profile_id": "75da88c5-05bf-4f54-bc85-5c775bd68254"
        }
    ]
    """
    return requests.get(API_URL + 'accounts', auth=auth).json()

def get_account(account_id):
    """
    Data for single account
    :param account_id: The account id
    :return:{
        "id": "a1b2c3d4",
        "balance": "1.100",
        "holds": "0.100",
        "available": "1.00",
        "currency": "USD"
    }
    """
    return requests.get(API_URL + 'account/{}'.format(account_id), auth=auth).json()

def place_order(size, price, side, product):
    """Create an order
    Some parameters have been omitted for simplicity
    Full documentation is here: https://docs.gdax.com/#orders
    :param size: Amount of BTC to buy or sell
    :param price: Price per Bitcoin
    :param side: buy or sell
    :param product: BTC-USD or any other supported product,
    :return: {
        "id": "d0c5340b-6d6c-49d9-b567-48c4bfca13d2",
        "price": "0.10000000",
        "size": "0.01000000",
        "product_id": "BTC-USD",
        "side": "buy",
        "stp": "dc",
        "type": "limit",
        "time_in_force": "GTC",
        "post_only": false,
        "created_at": "2016-12-08T20:02:28.53864Z",
        "fill_fees": "0.0000000000000000",
        "filled_size": "0.00000000",
        "executed_value": "0.0000000000000000",
        "status": "pending",
        "settled": false
    }
    Example parameters:
        {
            "size": "0.01",
            "price": "0.100",
            "side": "buy",
            "product_id": "BTC-USD"
        }
    """
    order = {
        'size': size,
        'price': price,
        'side': side,
        'product': product
    }
    response = requests.post(API_URL + 'orders', json=order, auth=auth)
    return response.json()

def get_order(order_id):
    """Data for single order
    :param order_id: Order id
    :return: {
        "id": "d0c5340b-6d6c-49d9-b567-48c4bfca13d2",
        "price": "0.10000000",
        "size": "0.01000000",
        "product_id": "BTC-USD",
        "side": "buy",
        "stp": "dc",
        "type": "limit",
        "time_in_force": "GTC",
        "post_only": false,
        "created_at": "2016-12-08T20:02:28.53864Z",
        "fill_fees": "0.0000000000000000",
        "filled_size": "0.00000000",
        "executed_value": "0.0000000000000000",
        "status": "pending",
        "settled": false
    }
    """
    return requests.get(API_URL + 'orders/{}'.format(order_id), auth=auth).json()

def cancel_order(order_id):
    """ Cancel order
    :param order_id: The id of the order returned from the server on creation
    :return: Response object with status 200 or 204 if successful, otherwise the error will be under
    message key
    """
    return requests.delete(API_URL + 'orders/{}'.format(order_id), auth=auth)