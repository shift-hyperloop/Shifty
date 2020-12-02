# import requests

# url = "http://129.241.14.60:8079/user_request"

# rfid = "904446217592"
# key = "elonsmusk" ##safety key, just some sort of security
# x = requests.get(f"{url}?rfid={rfid}&loops_used={amount_used}&key={key}")

# print(x.text.split(","))

# # print(f"{url}?rfid={rfid}&loops_used={amount_used}&key={key}")
# """
# returns [name, balance]
# if user does not exist -> returns negative id between -100 -> -300
#  gets added to database with the rfid, change name through slack
# returns -1 if error
# """



# import requests

# url = "http://129.241.14.60:8079/product_request"

# barcode = "dsaddsafdgf3"
# key = "elonsmusk"
# bought = 0
# x = requests.get(f"{url}?barcode={barcode}&key={key}&bought={bought}")

# print(x.text.split(","))
# """
# returns [name, price, number in stock]
# if item does not exist -> returns negative id between -100 -> -300
#  gets added to database with the barcode, change name on internal
#  website. Its the frontpage
# returns -1 if error
# """


# import requests

# url = "http://192.168.1.132:5000/distance"

# barcode = "dsaddsafdgf3"
# key = "elonsmusk"
# bought = 0
# # x = requests.get(f"{url}?barcode={barcode}&key={key}&bought={bought}")
# x = requests.get(f"{url}")
# print(x.text)
# # """

# import requests

# url = "http://127.0.0.1:8000/product_request"

# rfid = "904446217592"
# key = "elonsmusk" ##safety key, just some sort of security
# # x = requests.get(f"{url}?rfid={rfid}&loops_used={amount_used}&key={key}")
# data = {"product": ["coke","chocolate"],}
# x = requests.post(url, data=data)

# print(x.text.split(","))

# print(f"{url}?rfid={rfid}&loops_used={amount_used}&key={key}")
"""
returns [name, balance]
if user does not exist -> returns negative id between -100 -> -300
 gets added to database with the rfid, change name through slack
returns -1 if error
"""




import requests

url = "http://129.241.14.60:8079/rfid"

rfid = "155958981051"
key = "elonsmusk" ##safety key, just some sort of security
# x = requests.get(f"{url}?rfid={rfid}&loops_used={amount_used}&key={key}")
data = {"rfid": rfid,}
x = requests.post(url, data=data)