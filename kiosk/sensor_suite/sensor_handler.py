import evdev
import time
import RPi.GPIO as GPIO


def get_distance(trigger_pin, echo_pin):

    # set Trigger to HIGH
    GPIO.output(trigger_pin, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(trigger_pin, False)
 
    startTime = time.time()
    stopTime = time.time()
 
    # save startTime
    while GPIO.input(echo_pin) == 0:
        startTime = time.time()
    
    # save time of arrival
    while GPIO.input(echo_pin) == 1:
        stopTime = time.time()
    
    # time difference between start and arrival
    TimeElapsed = stopTime - startTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance


def monitor_distance(q):

    #GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BCM)              # BCM mode

    #set GPIO Pins
    GPIO_trigger = 3                    # TRIGGER is connected to pin 18
    GPIO_echo = 2                       # ECHO is connected to pin 24

    #set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_trigger, GPIO.OUT)  # TRIGGER is set to output
    GPIO.setup(GPIO_echo, GPIO.IN)      # ECHO is set to input

    while True:

        distance = get_distance(GPIO_trigger, GPIO_echo)   # Get initial distance
        t0 = time.perf_counter()    # Get start time for when object enters range

        time.sleep(0.05)

        while distance < 15:
            t = time.perf_counter()     # Get current time
            distance = get_distance(GPIO_trigger, GPIO_echo)   # Update distance

            if distance >= 15:

                if t-t0 > 0.5:                # If time held is greater than 3 seconds, delete all
                    q.put("del_all")

                    if t-t0 > 10:
                        q.put("easter_egg")

                elif t-t0 > 0.1:            # If time held is greater than 0.5 seconds, delete last
                    q.put("del_last")

            time.sleep(0.05)


def find_USB_devices():

    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    device_paths = {"RFID_device_path":False, "barcode_device_path":False}
    for device in devices:
        name = device.name
        if name.startswith('Sycreader'):
            device_paths["RFID_device_path"] = device.path
        elif name.startswith('SZ World'):
            device_paths["barcode_device_path"] = device.path

    return device_paths


# method for grabbing and monitoring an USB device, and transferring the intercepted number sequences
def monitor_device(device_path, q):
    print(f'starting monitor for {str(device_path)} using queue {str(q)}')
    device = evdev.InputDevice(device_path)     # Creates the device object
    print(f'grabbing {str(device_path)} using queue {str(q)}')
    device.grab()                               # Occupies the device and blocks it from being a keyboard
    scanned_chars = []
    
    for event in device.read_loop():

        if event.type == evdev.ecodes.EV_KEY:
            char = evdev.categorize(event).keycode[4:]                           # Saves the number trailing "KEY_"
            scanned_chars.append(char)                                           # Appends this number to a list
            if len(scanned_chars) > 1:                                           # If the list isn't empty
                if scanned_chars[-2] == 'ENTER':                                 # Looks for 2 consecutive ENTER presses
                    scanned_string = "".join([x for x in scanned_chars[:-2:2]])  # Concatenate every 2 number into str
                    q.put(scanned_string)                                        # Puts dev name and num seq. into queue
                    scanned_chars = []                                           # Resets variable
