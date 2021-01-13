from sensor_handler import *
from flask import Flask
import threading
import RPi.GPIO as GPIO
import queue
import time


if __name__ == '__main__':      # Only if this script is run directly
    q_rfid = queue.Queue()      # Queue used for transferring the intercepted number sequences
    q_barcode = queue.Queue()   # Queue used for transferring the intercepted number sequences
    q_distance = queue.Queue()  # Queue for distance sensor

    #devices = find_USB_devices()
    #RFID_device_path = devices['RFID_device_path']
    #barcode_device_path = devices['barcode_device_path']

    RFID_device_path = r"/dev/input/event1"
    barcode_device_path = r"/dev/input/event0"


    # creates and starts threads for the RFID scanner and the barcode scanner. Daemon means they won't keep python waiting
    if RFID_device_path:
        rfid_scanner_thread = threading.Thread(target=monitor_device, args=(RFID_device_path, q_rfid), daemon=True).start()
    else:
        print('Warning! No RFID scanner device found!')
    time.sleep(5)

    if barcode_device_path:
        barcode_scanner_thread = threading.Thread(target=monitor_device, args=(barcode_device_path, q_barcode), daemon=True).start()
    else:
        print('Warning! No barcode scanner device found!')
    time.sleep(5)

    distance_sensor_thread = threading.Thread(target=monitor_distance, args=(q_distance,), daemon=True).start() # TODO: check!

    app = Flask(__name__)


    @app.route('/init')
    def init_get():
        q_rfid.queue.clear()
        q_distance.queue.clear()
        q_barcode.queue.clear()
        return "Success"


    @app.route('/RFID')
    def rfid_get():
        if q_rfid.qsize():
            return q_rfid.get()
        else:
            return "nothing new!"


    @app.route('/barcode')
    def barcode_get():
        if q_barcode.qsize():
            return q_barcode.get()
        else:
            return "nothing new!"


    @app.route('/distance')
    def distance_get():
        if q_distance.qsize():
            return q_distance.get()
        else:
            return "nothing new!"


    try:
        app.run(debug=False, host='0.0.0.0')
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        raise e
    finally:
        GPIO.cleanup()