import requests
url = "http://shifthyperloop01.it.ntnu.no:8079/kiosk"


def get_product_data(barcode):
    """
    Get product from database by barcode
    returns: [id] if not exists, which is a placeholder name for the product in the database which has just been created
    else     [barcode, product name, price, number in stock]
    """
    return requests.get(f"{url}?event=get_product&barcode={barcode}").text.split(",")


def get_user_data(rfid):
    """
    Get user from database by rfid
    returns: [id] if not exists, which is a placeholder name for the user in the database which has just been created
    else     [rfid, full name, balance]
    """
    return requests.get(f"{url}?event=get_user&rfid={rfid}").text.split(",")


def post_purchase_order(rfid, barcode_list, total_price):
    """
        rfid: singluar rfid string
        barcode: 1-infinity codes
        total_price: total price of shopping cart
    """
    data = {
        "event": "finish_purchase",
        "rfid": rfid,
        "barcode": barcode_list,
        "total_price": total_price
    }

    response_code = requests.post(url, data=data).status_code
    print(response_code)

    if response_code == 200:
        return True
    else:
        return False
