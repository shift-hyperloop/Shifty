import os
from urllib.parse import urlparse

import requests

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

from selenium import webdriver

rfid_paths = ['checkin', 'checkout', 'register']

reader = SimpleMFRC522()

endpoint = os.environ.get('RFID_ENDPOINT')

browser = webdriver.Chrome('chromedriver.exe')
browser.fullscreen_window()

browser.get(os.environ.get('INDEX_URL'))

while True:
    current_url = browser.current_url
    url_path = urlparse(current_url)[2]
    url_path = url_path.replace('/', '')

    if url_path not in rfid_paths:
        continue

    try:
        rfid, text = reader.read()

    finally:
         GPIO.cleanup()

    requests.post(url=endpoint, data={'rfid': rfid, 'type': url_path})