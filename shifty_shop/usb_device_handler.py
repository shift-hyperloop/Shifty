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

def monitor_distance():
    while True:
        distance = get_distance()               # Get initial distance 
        startTime = time.perf_counter()         # Get start time for when object enters range

        while distance < 5:
            currentTime = time.perf_counter()   # Get current time
            distance = get_distance()           # Update distance

            if currentTime-startTime > 3:         # If time held is greater than 3 seconds, delete all 
                q_distance.put("all")
                print("all")

            elif currentTime-startTime > 0.5:       # If time held is greater than 0.5 seconds, delete last
                q_distance.put("last")
                print("last")





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
                    print(str(device.name) + ' did stuff.\n')                    # TODO: delete after debugging
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
RFID = threading.Thread(target=monitor_device, args=('/dev/input/event0', q_RFID), daemon=True).start()
barcode = threading.Thread(target=monitor_device, args=('/dev/input/event1', q_barcode), daemon=True).start()
distance_sensor = threading.Thread(target=monitor_distance, daemon=True).start()


if __name__ == '__main__':                      # Only if this script is run directly
    import time
    tilt = 0

    while True:
        inp = input('Press enter to fetch scan from queue, or type "exit" to quit\n')

        if inp.lower() == "exit":
            break

        elif inp == '':
            tilt = 0
            if q_RFID.qsize():
                print('RFID: ' + str(q_RFID.get()))
            elif q_barcode.qsize():
                print('Barcode ID: ' + str(q_barcode.get()))
            elif q_RFID.empty() and q_barcode.empty():
                print('Queues are empty.')

        elif inp:
            tilt += 1
            if tilt == 1:
                print("Invalid input. Try again: ")
            elif tilt == 2:
                print("What did I just tell you. Read the damn instructions..: ")
            elif tilt == 3:
                print("""You're as useless as the "ueue" in "queue". """)
            elif tilt == 4:
                print("I would tell you to eat shit, but that would be cannibalism. ")
            elif tilt == 5:
                print("""I will smash your face into a car windshield, take your mother out for a nice seafood dinner
                and then never call her again.""")
            elif tilt == 6:
                print("Remember to look both ways before you go fuck yourself. ")
            elif tilt == 7:
                print("You talk so much shit, I don't know whether to offer you breath mint or toilet paper. ")
            elif tilt == 8:
                print("I'm gonna harvest your toes. ")
            elif tilt == 9:
                print("""Type something again! I dare you! I double dare you motherf***ker! Type something one more"
                goddamn time!""")
            elif tilt == 10:
                print()
                print("OK BYE :*")
                import os
                time.sleep(3)
                os.system('shutdown /s /t 1')
                break
