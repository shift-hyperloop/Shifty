import requests
url = "http://shifthyperloop01.it.ntnu.no:8079/kiosk"


def get_product(barcode):
    """
    Get product from database by barcode
    returns: [id] if not exists
    else     [barcode, product name, price, number in stock]
    """
    return requests.get(f"{url}?event=get_product&barcode={barcode}").text.split(",")


def get_user(rfid):
    """
    Get user from database by rfid
    returns: [id] if not exists
    else     [rfid, full name, balance]
    """
    return requests.get(f"{url}?event=get_user&rfid={rfid}").text.split(",")


def post_purchase_order(rfid, barcode, total_price):
    """
        rfid: singluar rfid string
        barcode: 1-infinity codes
        total_price: total price of shopping cart
    """
    data = {
        "event":"finish_purchase","rfid":rfid,
        "barcode":barcode, "total_price":total_price
    }
    response = requests.post(url, data = data)
    if response.status_code != 200:
        print("Fuck, something went wrong")
