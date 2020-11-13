from usb_device_handler import *
from send_data import *
import evdev
import threading
import queue
import time
import RPi.GPIO as GPIO


# creates and starts threads for the RFID scanner and the barcode scanner. Daemon means they won't keep python waiting
RFID = threading.Thread(target=monitor_device, args=('/dev/input/event3', q_RFID), daemon=True).start()
barcode = threading.Thread(target=monitor_device, args=('/dev/input/event2', q_barcode), daemon=True).start()
distance_sensor = threading.Thread(target=monitor_distance, args=(q_distance,), daemon=True).start()
web_server = therading.Thread(target=start_web_server, args=(,), deamon=True).start()


if __name__ == '__main__':                      # Only if this script is run directly
    try:
        while True:
            if q_RFID.qsize():
                print('RFID: ' + str(q_RFID.get()))
            if q_barcode.qsize():
                print('Barcode ID: ' + str(q_barcode.get()))
            if q_distance.qsize():
                print('Distance message: ' + str(q_distance.get()))
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        raise e
    finally:
        GPIO.cleanup()