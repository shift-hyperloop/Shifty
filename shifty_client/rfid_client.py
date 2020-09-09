import os

import requests

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


reader = SimpleMFRC522()

endpoint = os.environ.get('RFID_ENDPOINT')

while True:
    try:
        rfid, text = reader.read()

        requests.post(url=endpoint, data={'rfid': rfid})

    finally:
         GPIO.cleanup()