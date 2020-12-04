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

# url = "http://127.0.0.1:8000/kiosk"

# rfid = "904446217592"

# # x = requests.get(f"{url}?barcode={barcode}&key={key}&bought={bought}")
# x = requests.get(f"{url}?event=get_user&rfid={rfid}")
# print(f"{url}?event=get_user&rfid={rfid}")
# # print(x.text)
# # """

import requests
url = "http://129.241.14.60:8079/kiosk"

rfid = "0331190651"
barcode = ["7311041002957", "7311041002957"]
total_price = 20
data = {
    "event":"finish_purchase","rfid":rfid,
    "barcode":barcode, "total_price":total_price
}
response = requests.post(url, data=data)
print(response.status_code)

#8 shift cups
#money aleks 351



# print(f"{url}?rfid={rfid}&loops_used={amount_used}&key={key}")
# """
# returns [name, balance]
# if user does not exist -> returns negative id between -100 -> -300
#  gets added to database with the rfid, change name through slack
# returns -1 if error
# """




# import requests

# url = "http://129.241.14.60:8079/rfid"

# rfid = "904446217592"
# key = "elonsmusk" ##safety key, just some sort of security
# # x = requests.get(f"{url}?rfid={rfid}&loops_used={amount_used}&key={key}")
# data = {"rfid": rfid,}
# x = requests.post(url, data=data)