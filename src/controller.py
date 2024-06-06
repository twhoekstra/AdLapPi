#  Copyright (c) 2024 Thijn Hoekstra
# Stick control code by Nick at https://stackoverflow.com/a/56419190
import time
import logging
from typing import List

import numpy as np
import evdev
from evdev import InputDevice

from evdev.ecodes import ABS_X, ABS_Y, ABS_Z, ABS_RZ, ABS_BRAKE, ABS_GAS, BTN_TL, BTN_TR

TRIGGER_MAX = 1024

TRIGGER_CONTROLS = [ABS_GAS, ABS_BRAKE]
BUMPER_CONTROLS = [BTN_TL, BTN_TR]
STICK_CONTROLS = [ABS_X, ABS_Y, ABS_Z, ABS_RZ]

logger = logging.getLogger(__name__)

CENTER_TOLERANCE = 0.1
STICK_MAX = 65536

class Position:

    def __init__(self, x=None, y=None, z=None):
        self.x = x
        self.y = y
        self.z = z

    def as_array(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z], dtype=np.float64)

    def __str__(self):
        return f"({self.x:,.2f}, {self.y:,.2f}, {self.z:,.2f})"


class ControllerPosition:

    def __init__(self):
        self.left = Position(0, 0, 0)
        self.right = Position(0, 0, 0)

    def as_array(self) -> np.ndarray:
        return np.vstack([self.left.as_array(), self.right.as_array()], dtype=np.float64)

    def clear(self):
        self.left.x = 0
        self.left.y = 0
        self.left.z = 0
        self.right.x = 0
        self.right.y = 0
        self.right.z = 0

    def set(self, code, pos) -> None:
        if code in STICK_CONTROLS:
            pos = (pos / STICK_MAX - 0.5) * 2

            if abs(pos) < CENTER_TOLERANCE:
                pos = 0

            self.map_abs_controls(code, pos)

        elif code in TRIGGER_CONTROLS:
            pos = -pos / TRIGGER_MAX

            if abs(pos) < CENTER_TOLERANCE:
                pos = 0

            if code == ABS_BRAKE:
                self.left.z = pos
            elif code == ABS_GAS:
                self.right.z = pos

        elif code in BUMPER_CONTROLS:
            if code == BTN_TL:
                self.left.z = int(bool(pos))
            if code == BTN_TR:
                self.right.z = int(bool(pos))

        else:
            pass

    def map_abs_controls(self, code, pos):
        if code == ABS_X:
            self.left.x = pos
        elif code == ABS_Y:
            self.left.y = pos
        elif code == ABS_BRAKE:
            self.left.z = pos
        elif code == ABS_Z:
            self.right.x = -pos # Flipped
        elif code == ABS_RZ:
            self.right.y = pos

    def __str__(self):
        return f"(Left: {self.left}, Right: {self.right})"


ZEROPOSITION = Position(x=0, y=0, z=0).as_array()

def wait_to_get_devices(timeout=100, check_every=1) -> InputDevice:

    start_time = time.time()

    while True:
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

        for device in devices:
            if 'xbox' in device.name.lower():
                logger.info('Found XBox controller!')
                return device

        if time.time() - start_time > timeout:
            break

        time.sleep(check_every)
        logger.info(f"Couldn't find XBox controller. Trying again in {check_every} seconds...")


    raise RuntimeError("Error: XBox controller not found.")


def list_devices():

    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

    for device in devices:

        print(device.path, device.name, device.phys)


def controller_thread(dev: evdev.InputDevice, pos: ControllerPosition):

    for event in dev.read_loop():

        if event.type == evdev.ecodes.EV_ABS:
            # Sticks and triggers
            if event.code in STICK_CONTROLS or event.code in TRIGGER_CONTROLS:
                pos.set(event.code, event.value)

        if event.type == evdev.ecodes.EV_KEY:
            # Buttons
            if event.code in BUMPER_CONTROLS:
                # Bumpers used for moving
                pos.set(event.code, event.value)

            else:
                # Other buttons for presets
                pass





