import requests

RFID_URL = "http://192.168.1.150:5000/RFID"

r = requests.get(url = RFID_URL)
data = r.content.decode("utf-8")
print(data)
