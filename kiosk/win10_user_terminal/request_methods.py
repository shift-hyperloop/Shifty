import requests


def request_purchase(customer_rfid, purchase_sum=0, key="elonsmusk"):

    url = "http://shifthyperloop01.it.ntnu.no:8079/user_request"

    return requests.get(f"{url}?rfid={customer_rfid}&loops_used={purchase_sum}&key={key}").text.split(",")

"""
    returns [name, balance]
    if user does not exist -> returns negative id between -100 -> -300
    gets added to database with the rfid, change name through slack
    returns -1 if error
    """


def request_product_data(barcode, bought=0, key="elonsmusk"):

    url = "http://shifthyperloop01.it.ntnu.no:8079/product_request"

    return requests.get(f"{url}?barcode={barcode}&key={key}&bought={bought}").text.split(",")


"""
returns [barcode, name, price, number in stock]
if item does not exist -> returns negative id between -100 -> -300
 gets added to database with the barcode, change name on internal
 website. Its the frontpage
returns -1 if error
"""
