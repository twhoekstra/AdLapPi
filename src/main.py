#  Copyright (c) 2024 Thijn Hoekstra
import queue

import evdev
import numpy as np
import serial
import threading
import time
import logging

# import keyboard

import gcode
import controller
from controller import ControllerPosition, ZEROPOSITION
import serial_connection
from serial_connection import read_serial_thread, send_serial

STICK_MULTIPLIER = 0.5

logger = logging.getLogger(__name__)

SPEED = 10000

# Serial port settings
SERIAL_PORTS = ['/dev/ttyACM0', '/dev/ttyACM1']  # Change this to your serial port
HOME_FIRST = False


# Controller settings
CONTROLLER_NAME = None

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
def main(debug=True):
    # Open serial port
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO,
                        handlers=[
                                logging.FileHandler("debug.log"),
                                logging.StreamHandler()
                        ])

    arduinos = serial_connection.acquire_arduinos(SERIAL_PORTS)

    if debug:
        # Start a thread to read data from the serial port
        read_threads = []
        for arduino in arduinos:
            read_threads.append(threading.Thread(target=read_serial_thread,
                                           args=(arduino,),
                                           daemon=True))
        [t.start() for t in read_threads]

    pos = ControllerPosition()
    dev = controller.wait_to_get_devices()

    ctrl_thread = threading.Thread(target=controller.controller_thread,
                                   args=(dev, pos),
                                   daemon=True)
    ctrl_thread.start()

    time.sleep(2) # Give arms time to setup

    if HOME_FIRST:
        serial_connection.send_serials(arduinos, gcode.home())

    if True:
        serial_connection.send_serials(arduinos, gcode.software_endstops())
    # Set axes to relative mode
    # serial_connection.send_serials(arduinos, gcode.relative_positioning())

    # Main loop to handle key presses
    s = np.zeros((2, 3))
    while True:

        for armpos, arduino in zip(s.round(3), arduinos):
            if np.any(armpos != ZEROPOSITION):
                send_serial(arduino, gcode.move(vector=armpos, order="xyz", speed=SPEED))
                # send_serial(arduino, gcode.relative_positioning())
                time.sleep(0.01)

        # pos.clear()
        v = pos.as_array()

        v *= STICK_MULTIPLIER
        # v = v.round(3)

        s += v


if __name__ == "__main__":
    main()
