from flask import Flask
app = Flask(__name__)

@app.route('/RFID')
def rfid_get():
	if q_rfid.qsize():
		message = q_rfid.get()
		print(message)
		return message
	else:
		return "nothing new!"

@app.route('/barcode')
def barcode_get():
	if q_barcode.qsize():
		message = q_barcode.get()
		print(message)
		return message
	else:
		return "nothing new!"

@app.route('/distance')
def distance_get():
	if q_distance.qsize():
		message = q_distance.get()
		print(message)
		return message
	else:
		return "nothing new!"

