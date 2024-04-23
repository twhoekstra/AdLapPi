#  Copyright (c) 2024 Thijn Hoekstra
import queue

import evdev
import serial
import threading
import time
# import keyboard

import gcode
import controller
from controller import ControllerPosition, ZEROPOSITION
import serial_connection
from serial_connection import read_serial_thread, send_serial



SPEED = 10000

# Serial port settings
SERIAL_PORT = '/dev/ttyACM0'  # Change this to your serial port
BAUD_RATE = 250000
HOME_FIRST = False
TIMEOUT = 1

# Controller settings
CONTROLLER_NAME = '/dev/input/event4'

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

    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT) as ser:

        # Start a thread to read data from the serial port
        read_thread = threading.Thread(target=read_serial_thread,
                                       args=(ser,),
                                       daemon=True)
        read_thread.start()

        pos = ControllerPosition(0, 0)
        dev = evdev.InputDevice(CONTROLLER_NAME)
        ctrl_thread = threading.Thread(target=controller.controller_thread,
                                       args=(dev, pos),
                                       daemon=True)
        ctrl_thread.start()

        time.sleep(2) # Give arms time to setup

        if HOME_FIRST:
            send_serial(ser, gcode.home())

        # Set axes to relative mode
        send_serial(ser, gcode.relative_positioning())

        # Main loop to handle key presses
        dir = 1
        pos_prev = ZEROPOSITION
        while True:
            # if keyboard.is_pressed('q'):
            #     print("Exiting...")
            #     break

            # Get the pressed key
            # key = keyboard.read_event(suppress=True)
            # action = keyboard_callback(key)

            v = pos.as_array()
            v *= 2
            v = v.round(3)

            if pos != ZEROPOSITION:
                send_serial(ser, gcode.move(vector=v, order="xy", speed=SPEED))
                send_serial(ser, gcode.relative_positioning())

            time.sleep(0.01)


if __name__ == "__main__":
    main()
