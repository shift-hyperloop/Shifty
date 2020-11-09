import evdev
import threading
import queue
import time
import RPi.GPIO as GPIO


def get_distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance


def monitor_distance(q):
    while True:

        distance = get_distance()   # Get initial distance
        t0 = time.perf_counter()    # Get start time for when object enters range

        while distance < 5:
            t = time.perf_counter()     # Get current time
            distance = get_distance()   # Update distance

            if distance >= 5:

                if t-t0 > 3:                # If time held is greater than 3 seconds, delete all
                    q.put("all")

                elif t-t0 > 0.5:            # If time held is greater than 0.5 seconds, delete last
                    q.put("last")


# method for grabbing and monitoring an USB device, and transferring the intercepted number sequences
def monitor_device(device_id, q):
    device = evdev.InputDevice(device_id)   # Creates the device object
    device.grab()                           # Occupies the device and blocks it from being a keyboard
    scanned_chars = []
    
    for event in device.read_loop():

        if event.type == evdev.ecodes.EV_KEY:
            char = evdev.categorize(event).keycode[4:]                           # Saves the number trailing "KEY_"
            scanned_chars.append(char)                                           # Appends this number to a list
            if len(scanned_chars) > 1:                                           # If the list isn't empty
                if scanned_chars[-2] == 'ENTER':                                 # Looks for 2 consecutive ENTER presses
                    scanned_string = "".join([x for x in scanned_chars[:-2:2]])  # Concatenate every 2 number into str
                    q.put(scanned_string)                    # Puts dev name and num seq. into queue
                    scanned_chars = []                                           # Resets variable


#Defining global objects
q_RFID = queue.SimpleQueue()        # Queue used for transferring the intercepted number sequences
q_barcode = queue.SimpleQueue()     # Queue used for transferring the intercepted number sequences
q_distance = queue.SimpleQueue()    # Queue for distance sensor

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)              # BCM mode
 
#set GPIO Pins
GPIO_TRIGGER = 18                   # TRIGGER is connected to pin 18
GPIO_ECHO = 24                      # ECHO is connected to pin 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)  # TRIGGER is set to output
GPIO.setup(GPIO_ECHO, GPIO.IN)      # ECHO is set to input

GPIO.output(GPIO_TRIGGER, False)    # Setting Trigger to False for redundancy


# creates and starts threads for the RFID scanner and the barcode scanner. Daemon means they won't keep python waiting
RFID = threading.Thread(target=monitor_device, args=('/dev/input/event3', q_RFID), daemon=True).start()
barcode = threading.Thread(target=monitor_device, args=('/dev/input/event2', q_barcode), daemon=True).start()
distance_sensor = threading.Thread(target=monitor_distance, args=(q_distance,), daemon=True).start()


if __name__ == '__main__':                      # Only if this script is run directly

    while True:
        if q_RFID.qsize():
            print('RFID: ' + str(q_RFID.get()))
        if q_barcode.qsize():
            print('Barcode ID: ' + str(q_barcode.get()))
        if q_distance.qsize():
            print('Distance message: ' + str(q_distance.get()))
        time.sleep(0.05)
