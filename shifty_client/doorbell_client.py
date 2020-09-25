import os
import time

import requests

endpoint = os.environ.get('DOORBELL_ENDPOINT')

def play_sound():
    os.system('mpg321 -q SoundFX/Ding-dong.mp3 &')

while True:

    result = requests.get(endpoint).json()

    if result['is_ringing']:
        play_sound()
    
    time.sleep(5)

