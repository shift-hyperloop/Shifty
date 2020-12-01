import requests


def request_user(rfid, amount_used=0, key="elonsmusk"):

    url = "http://shifthyperloop01.it.ntnu.no:8079/user_request"

    return requests.get(f"{url}?rfid={rfid}&loops_used={amount_used}&key={key}").text.split(",")

"""
    returns [name, balance]
    if user does not exist -> returns negative id between -100 -> -300
    gets added to database with the rfid, change name through slack
    returns -1 if error
    """


def request_product(barcode, bought=0, key="elonsmusk"):

    url = "http://shifthyperloop01.it.ntnu.no:8079/product_request"

    return requests.get(f"{url}?barcode={barcode}&key={key}&bought={bought}").text.split(",")


"""
returns [name, price, number in stock]
if item does not exist -> returns negative id between -100 -> -300
 gets added to database with the barcode, change name on internal
 website. Its the frontpage
returns -1 if error
"""
