import os
import time
import requests

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

endpoint = os.environ.get('RFID_ENDPOINT')

while True:
    try:
        rfid, text = reader.read()
        print('RFID: ', rfid)
        os.system('mpg321 -q Ding-dong.mp3 &')
        time.sleep(5)

    finally:
         GPIO.cleanup()
    try:
         response = requests.post(url=endpoint, data={'rfid': rfid, 'type': 'checkin'}).json()
    except Exception as e:
         print('User does not exist!')
