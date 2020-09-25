import os
import time

import requests

endpoint = os.environ.get('DOORBELL_ENDPOINT')


def play_sound():
    os.system('mpg321 -q SoundFX/Ding-dong.mp3 &')


while True:
    try:
        result = requests.get(endpoint).json()

        if result['is_ringing']:
            play_sound()

    except Exception as e:
        print('ERROR')
        time.sleep(10)

    time.sleep(5)
