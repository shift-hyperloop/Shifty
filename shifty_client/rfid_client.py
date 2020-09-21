import os
import time
import datetime
import requests

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

endpoint = os.environ.get('RFID_ENDPOINT')

while True:

    try:
        rfid, text = reader.read()
        print(datetime.datetime.now().replace(microsecond=0).isoformat(' ', 'seconds') + ' - Scanned RFID: ' + str(rfid))
        os.system('mpg321 -q Ding-dong.mp3 &')
        time.sleep(3)

    finally:
         GPIO.cleanup()

    try:
         response = requests.post(url=endpoint, data={'rfid': rfid, 'type': 'checkin'}).json()

    except Exception as e:
         print(datetime.datetime.now().replace(microsecond=0).isoformat(' ', 'seconds') + ' - User does not exist!')
