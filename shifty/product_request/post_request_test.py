# import requests

# url = "http://127.0.0.1:8000/user_request"

# rfid = "3921874810n"
# key = "elonsmusk" ##safety key, just some sort of security
# amount_used = 0
# x = requests.get(f"{url}?rfid={rfid}&loops_used={amount_used}&key={key}")

# print(x.text.split(","))
# """
# returns [name, balance]
# if user does not exist -> returns negative id between -100 -> -300
#  gets added to database with the rfid, change name through slack
# returns -1 if error
# """



import requests

url = "http://127.0.0.1:8000/product_request"

barcode = "dsaddsafdgf3"
key = "elonsmusk"
bought = -1
x = requests.get(f"{url}?barcode={barcode}&key={key}&bought={bought}")

print(x.text.split(","))
"""
returns [name, price, number in stock]
if item does not exist -> returns negative id between -100 -> -300
 gets added to database with the barcode, change name on internal
 website. Its the frontpage
returns -1 if error
"""
