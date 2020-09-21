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
        print()
        print(datetime.datetime.now().replace(microsecond=0).isoformat(' ', 'seconds'))
        print('Scanned RFID: ' + str(rfid))

    finally:
        time.sleep(.1)
        GPIO.cleanup()

    try:
        response = requests.post(url=endpoint, data={'rfid': rfid, 'type': 'checkin'}).json()
        os.system('mpg321 -q Ding-dong.mp3 &')

    except Exception as e:
        print('ERROR! User not found =( !')
        os.system('mpg321 -q Error.mp3 &')

    time.sleep(3)
