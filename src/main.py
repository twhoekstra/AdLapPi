#  Copyright (c) 2024 Thijn Hoekstra
import argparse
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

SERIAL_PERIOD_MS = 20
SPEED = 1
FEEDRATE = 10000
ACCELERATION = 3000

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
def main(verbose=False,
         feedrate=None,
         speed=None,
         accel=None,
         serial_period_ms=None):

    if feedrate is None:
        feedrate = FEEDRATE
    if speed is None:
        speed = SPEED
    if accel is None:
        accel = ACCELERATION
    if serial_period_ms is None:
        serial_period_ms = SERIAL_PERIOD_MS

    # Open serial port
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO,
                        handlers=[
                                logging.FileHandler("debug.log"),
                                logging.StreamHandler()
                        ])

    arduinos = serial_connection.acquire_arduinos(SERIAL_PORTS)

    if verbose:
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

    # Set axes to relative mode
    # serial_connection.send_serials(arduinos, gcode.relative_positioning())

    serial_connection.send_serials(arduinos, gcode.set_acceleration(accel))

    # Main loop to handle key presses
    s = np.zeros((2, 3))
    v = np.zeros((2, 3))
    wait = serial_period_ms / 1e3 / len(arduinos)
    while True:

        for armvel, arduino in zip(v.round(3), arduinos):
            if np.any(armvel != ZEROPOSITION):
                send_serial(arduino, gcode.relative_positioning())
                send_serial(arduino,
                            gcode.move(vector=armvel, order="xyz", speed=feedrate))
                time.sleep(wait)

        # pos.clear()
        v = pos.as_array()
        v *= speed

        s += v

        print(s)

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--feedrate', help="Feedrate for stepper moves.",
                        type=int)
    parser.add_argument('-s', '--speed', help="Speed for moving with the joystick.",
                        type=float)
    parser.add_argument('-a', '--acceleration', help="Acceleration for stepper moves.",
                        type=int)
    parser.add_argument('-t', '--serial_period', help="Period of serial loop in milliseconds.",
                        type=int)
    parser.add_argument('-v', '--verbose',
                        action='store_true')
    args = parser.parse_args()

    main(verbose=args.verbose,
         feedrate=args.feedrate,
         speed=args.speed,
         accel=args.acceleration,
         serial_period_ms=args.serial_period)
