import requests

from blockchain_info.utils import add_if_present


def get_block(block_hash):
    """
    Data for single block
    :param block_hash: The block hash
    :return: {
        "hash":"0000000000000bae09a7a393a8acded75aa67e46cb81f7acaa5ad94f9eacd103",
        "ver":1,
        "prev_block":"00000000000007d0f98d9edca880a6c124e25095712df8952e0439ac7409738a",
        "mrkl_root":"935aa0ed2e29a4b81e0c995c39e06995ecce7ddbebb26ed32d550a72e8200bf5",
        "time":1322131230,
        "bits":437129626,
        "nonce":2964215930,
        "n_tx":22,
        "size":9195,
        "block_index":818044,
        "main_chain":true,
        "height":154595,
        "received_time":1322131301,
        "relayed_by":"108.60.208.156",
        "tx":[--Array of Transactions--]
    }
    """
    return requests.get("https://blockchain.info/rawblock/{}".format(block_hash)).json()

def get_transaction(transaction_hash):
    """
    Data for transaction
    :param transaction_hash: The transaction hash
    :return: {
            "hash":"b6f6991d03df0e2e04dafffcd6bc418aac66049e2cd74b80f14ac86db1e3f0da",
            "ver":1,
            "vin_sz":1,
            "vout_sz":2,
            "lock_time":"Unavailable",
            "size":258,
            "relayed_by":"64.179.201.80",
            "block_height, 12200,
            "tx_index":"12563028",
            "inputs":[
                    {
                        "prev_out":{
                            "hash":"a3e2bcc9a5f776112497a32b05f4b9e5b2405ed9",
                            "value":"100000000",
                            "tx_index":"12554260",
                            "n":"2"
                        },
                        "script":"76a914641ad5051edd97029a003fe9efb29359fcee409d88ac"
                    }
                ],
            "out":[

                        {
                            "value":"98000000",
                            "hash":"29d6a3540acfa0a950bef2bfdc75cd51c24390fd",
                            "script":"76a914641ad5051edd97029a003fe9efb29359fcee409d88ac"
                        },

                        {
                            "value":"2000000",
                            "hash":"17b5038a413f5c5ee288caa64cfab35a0c01914e",
                            "script":"76a914641ad5051edd97029a003fe9efb29359fcee409d88ac"
                        }
                ]
        }
    """
    return requests.get("https://blockchain.info/rawtx/{}".format(transaction_hash)).json()

def get_blocks_at_height(height):
    """
    Get all blocks at specific height
    :param height: The height
    :return: {
       "blocks" :
        [
            --Array Of Blocks at the specified height--
        ]
    }
    """
    return requests.get("https://blockchain.info/block-height/{}".format(height), params={"format": "json"}).json()

def get_address_data(address, offset=None, limit=None):
    """
    Returns blockchain information about an address
    :param address: The address
    :param offset: (optional) Skip the first n transactions
    :param limit: (optional) Show only n transactions
    :return: {
        "hash160":"660d4ef3a743e3e696ad990364e555c271ad504b",
        "address":"1AJbsFZ64EpEfS5UAjAfcUG8pH8Jn3rn1F",
        "n_tx":17,
        "n_unredeemed":2,
        "total_received":1031350000,
        "total_sent":931250000,
        "final_balance":100100000,
        "txs":[--Array of Transactions--]
    }
    """
    url = "https://blockchain.info/rawaddr/{}".format(address)
    params = dict()
    add_if_present("offset", offset, params)
    add_if_present("limit", limit, params)
    return requests.get(url, params=params).json()


def latest_block():
    """
    Latest block on the Bitcoin blockchain
    :return: {
        "hash":"0000000000000538200a48202ca6340e983646ca088c7618ae82d68e0c76ef5a",
        "time":1325794737,
        "block_index":841841,
        "height":160778,
        "txIndexes":[13950369,13950510,13951472]
     }
    """
    return requests.get("https://blockchain.info/latestblock").json()

def address_balance(addresses):
    """
    Balance of list of addresses
    :param addresses: List of addresses to get balance for
    :return: {
            "1MDUoxL1bGvMxhuoDYx6i11ePytECAk9QK": {
                "final_balance": 0,
                "n_tx": 0,
                "total_received": 0
            },
            "15EW3AMRm2yP6LEF5YKKLYwvphy3DmMqN6": {
                "final_balance": 0,
                "n_tx": 2,
                "total_received": 310630609
            }
        }
    """
    addrs_param = "|".join(addresses)
    return requests.get("https://blockchain.info/balance", params={"active": addrs_param}).json()

def unconfirmed_transactions():
    """
    Current unconfirmed transactions
    :return:
    """
    return requests.get("https://blockchain.info/unconfirmed-transactions?format=json").json()

def chart_data(chart_type):
    """
    Get different data in chart format
    Full list of chart types: https://blockchain.info/charts/
    :param chart_type: Chart type
    :return: {
            "values" : [
                {
                    "x" : 1290602498, //Unix timestamp
                    "y" : 1309696.2116000003
                }]
        }
    """
    return requests.get("https://blockchain.info/charts/$chart-type?format=json").json()