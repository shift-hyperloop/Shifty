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
    
    except Exception as e:
        print(e)
        GPIO.cleanup()

    try:
        response = requests.post(url=endpoint, data={'rfid': rfid, 'type': 'checkin'}).json()
        if response['success']:
            if response['type'] == 'check_in':
                os.system('mpg321 -q SoundFX/Checkin.mp3 &')
            elif response['type'] == 'check_out':
                os.system('mpg321 -q SoundFX/Checkout.mp3 &')
        else:
            print('User not found =( !')
            os.system('mpg321 -q SoundFX/Error.mp3 &')

    except Exception as e:
        print(e)
        os.system('mpg321 -q SoundFX/Error.mp3 &')
        GPIO.cleanup()

    time.sleep(3)

