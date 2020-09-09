import os
import time

import requests

endpoint = os.environ.get('DOORBELL_ENDPOINT')

while True:

    result = requests.get(endpoint).json()

    if result['is_ringing']:
        play_sound()
    
    time.sleep(5)

def play_sound():
    # TODO: Play ringing sound
    pass