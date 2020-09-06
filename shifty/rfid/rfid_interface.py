"""
RFID Interface
"""
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


class RFIDInterface:

    def __init__(self):
        self.reader = SimpleMFRC522()
    
    def read(self) -> str:
        try:
            rfid, text = self.reader.read()
            return rfid

        finally:
            GPIO.cleanup()
    


