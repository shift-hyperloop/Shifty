import os
from urllib.parse import urlparse

import requests

"""import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

rfid_paths = ['checkin', 'checkout', 'rfid_register']

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

    response = requests.post(url=endpoint, data={'rfid': rfid, 'type': url_path}).json()
    if response['success'] and url_path == 'checkin':
        browser.get(os.environ.get('INDEX_URL') + '/checkin_success')
    if response['success'] and url_path == 'checkout':
        browser.get(os.environ.get('INDEX_URL') + '/checkout_success')
    if response['success'] and url_path == 'register':
        browser.get(os.environ.get('INDEX_URL') + '/register_success')