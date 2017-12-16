import requests

API_URL = "https://api.gdax.com/"
def get_products():
    """ List all available products for trading
    :return: [{
        "id":"LTC-EUR",
        "base_currency":"LTC",
        "quote_currency":"EUR",
        "base_min_size":"0.01",
        "base_max_size":"1000000",
        "quote_increment":"0.01",
        "display_name":"LTC/EUR",
        "status":"online",
        "margin_enabled":false,
        "status_message":null
    }]
    """
    return requests.get(API_URL + "products").json()

def get_product_orderbook(product_id, level=1):
    """ Return product orderbook

    :param product_id: The product which orderbook you need (BTC-USD, LTC-EUR)
    :param level: The level of data you need, available levels are 1,2,3
        Level 1: returns only the first (best) buy and sell orders
        Level 2: returns all orders aggregated by price
        Level 3: returns all orders separately, not aggregated
    :return:
    {"sequence":4578336950,"bids":[["18818.25","8.49",2]],"asks":[["18819.98","0.02247951",2]]}
    """
    return requests.get(API_URL + "products/{}/book".format(product_id), params={"level": level}).json()

def get_product_ticker(product_id):
    """Provides latest data about the product
    The last executed trade, the latest price, the best buy and sell orders and 24h volume

    :param product_id: The product id
    :return: {
        "trade_id": 4729088,
        "price": "333.99",
        "size": "0.193",
        "bid": "333.98",
        "ask": "333.99",
        "volume": "5957.11914015",
        "time": "2015-11-14T20:46:03.511254Z"
    }
    """
    return requests.get(API_URL + "/products/{}/ticker".format(product_id)).json()

def get_product_trades(product_id):
    """Latest trades for a product

    :param product_id: The product id
    :return: [{
        "time": "2014-11-07T22:19:28.578544Z",
        "trade_id": 74,
        "price": "10.00000000",
        "size": "0.01000000",
        "side": "buy"
    },
    """
    return requests.get(API_URL + "/products/{}/trades".format(product_id)).json()

def get_product_history(product_id, start_time, end_time, granularity):
    """Historical data for product

    :param product_id: The product id
    :param start_time: Start time of period
    :param end_time: End time of period
    :param granularity: Granularity at which to receive the response data points
    :return: [[1513438200, 259.68, 260.73, 259.68, 259.88, 267.94151752],
    Response values are:
        time - start time of bucket
        low - lowest price in time bucket
        high - highest price in time bucket
        open - price at beginning of time bucket
        close - price at end of time bucket
        volume - volume of trading activity during period
    """
    params = {
        "start": start_time.isoformat(),
        "end": end_time.isoformat(),
        "granularity": granularity
    }
    return requests.get(API_URL + '/products/{}/candles'.format(product_id), params=params).json()