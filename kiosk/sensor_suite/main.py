from sensor_handler import *
import send_data
from flask import Flask
import threading
import RPi.GPIO as GPIO
import queue
import time


if __name__ == '__main__':                      # Only if this script is run directly
    q_rfid = queue.SimpleQueue()  # Queue used for transferring the intercepted number sequences
    q_barcode = queue.SimpleQueue()  # Queue used for transferring the intercepted number sequences
    q_distance = queue.SimpleQueue()  # Queue for distance sensor

    #devices = find_USB_devices()
    #RFID_device_path = devices['RFID_device_path']
    #barcode_device_path = devices['barcode_device_path']

    RFID_device_path = r"/dev/input/event2"
    barcode_device_path = r"/dev/input/event1"


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
    #web_server_thread = threading.Thread(target=start_web_server, args=(), daemon=True).start()

    app = Flask("send_data")

    try:
        app.run(debug=True, host='0.0.0.0')
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        raise e
    finally:
        GPIO.cleanup()
