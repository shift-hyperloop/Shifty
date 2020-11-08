import evdev
import threading
import queue


# method for grabbing and monitoring an USB device, and transferring the intercepted number sequences
def monitor_device(device_id):
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
                    q.put([str(device.name), scanned_string])                    # Puts dev name and num seq. into queue
                    print(str(device.name) + ' did stuff.\n')                    # TODO: delete after debugging
                    scanned_chars = []                                           # Resets variable


q = queue.SimpleQueue()     # Queue used for transferring the intercepted number sequences

# creates and starts threads for the RFID scanner and the barcode scanner. Daemon means they won't keep python waiting
RFID = threading.Thread(target=monitor_device, args=('/dev/input/event5',), daemon=True).start()
barcode = threading.Thread(target=monitor_device, args=('/dev/input/event6',), daemon=True).start()


if __name__ == '__main__':                      # Only if this script is run directly
    import time
    tilt = 0

    while True:
        inp = input('Press enter to fetch scan from queue, or type "exit" to quit\n')

        if inp.lower() == "exit":
            break

        elif inp == '':
            tilt = 0
            if q.empty():
                print('Queue is empty.')
            else:
                device_name, num_seq = [item for item in q.get()]
                print('Device: ' + str(device_name))
                print('Sequence: ' + str(num_seq))

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
