from flask import Flask
#from usb_device_handler import q_RFID, q_barcode, q_distance

app = Flask(__name__)

@app.route('/RFID')
def RFID():
	if q_RFID.qsize():
	    return q_RFID.get()
	else:
		return "nothing new!"
	
@app.route('/barcode')
def barcode():
	if q_barcode.qsize():
		return q_barcode.get()
	else:
		return "nothing new!"

@app.route('/distance')
def distance():
	if q_distance.qsize():
		return q_distance.get()
	else:
		return "nothing new!"

def start_web_server():
	app.run(debug=True, host='0.0.0.0')

