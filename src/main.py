#  Copyright (c) 2024 Thijn Hoekstra


import serial
import threading
import time
# import keyboard

import gcode
from serial_connection import read_serial_thread, send_serial

SPEED = 500

# Serial port settings
SERIAL_PORT = '/dev/ttyACM0'  # Change this to your serial port
BAUD_RATE = 250000
HOME_FIRST = False
TIMEOUT = 1


# def keyboard_callback(key):
#     # Send the key to the serial device
#     if key.event_type == keyboard.KEY_DOWN:
#         return gcode.move(x=20, speed=SPEED)
#
#     elif key.event_type == keyboard.KEY_UP:
#         return gcode.move(x=-20, speed=SPEED)
#     else:
#         return None

def timer_callback(key):
    # Send the key to the serial device
    if key.event_type == keyboard.KEY_DOWN:
        return gcode.move(x=20, speed=SPEED)

    elif key.event_type == keyboard.KEY_UP:
        return gcode.move(x=-20, speed=SPEED)
    else:
        return None


class Timer:

    def __init__(self, interval=1):
        self.prev = None
        self.interval = interval

    def start(self):
        self.prev = time.time()
        return self

    def __call__(self):
        if self.prev is None:
            raise RuntimeError("The timer has not been started yet")

        current = time.time()
        if current - self.prev > self.interval:
            self.prev = current
            return True
        else:
            return False



# Main function
def main():
    # Open serial port
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)

    # Start a thread to read data from the serial port
    read_thread = threading.Thread(target=read_serial_thread, args=(ser,), daemon=True)
    read_thread.start()

    time.sleep(5) # Give arms time to setup

    timer = Timer(5).start()
    long_timer = Timer(100).start()

    print("Press 'q' to quit.")

    if HOME_FIRST:
        send_serial(ser, gcode.home())

    # Set axes to relative mode
    send_serial(ser, gcode.relative_positioning())

    # Main loop to handle key presses
    dir = 1
    while True:
        # if keyboard.is_pressed('q'):
        #     print("Exiting...")
        #     break

        # Get the pressed key
        # key = keyboard.read_event(suppress=True)
        # action = keyboard_callback(key)

        action = timer()
        if action:
            send_serial(ser, gcode.move(x=dir*10, speed=SPEED))
            dir *= -1

        if long_timer():
            break

    # Close serial port
    ser.close()

if __name__ == "__main__":
    main()
