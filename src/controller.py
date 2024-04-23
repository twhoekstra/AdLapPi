#  Copyright (c) 2024 Thijn Hoekstra
# Stick control code by Nick at https://stackoverflow.com/a/56419190

import numpy as np
import evdev
from evdev.ecodes import ABS_X, ABS_Y, ABS_BRAKE

CENTER_TOLERANCE = 10000
STICK_MAX = 32768



center = {
    ABS_X: 0,
    ABS_Y: 0,
    ABS_BRAKE: 0,
}
class ControllerPosition:

    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    def as_dict(self) -> dict:
        return {"x": self.x, "y": self.y}

    def as_array(self) -> np.ndarray:
        return np.array([self.x, self.y])

    @staticmethod
    def normalize(v):
        return v / STICK_MAX

    def set(self, code, pos) -> None:
        pos = self.normalize(pos)
        if code == ABS_X:
            self.x = pos
        elif code == ABS_Y:
            self.y = pos
        else:
            pass
    def __str__(self):
        return f"({self.x:,.2f}, {self.y:,.2f})"


    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

ZEROPOSITION = ControllerPosition(0, 0)

def list_devices():

    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

    for device in devices:

        print(device.path, device.name, device.phys)


def controller_thread(dev: evdev.InputDevice, pos: ControllerPosition):

    for event in dev.read_loop():
        # read stick axis movement
        if event.type == evdev.ecodes.EV_ABS:

            if event.code in [ABS_X, ABS_Y, ABS_BRAKE]:

                value = event.value - center[event.code]

                if abs(value) <= CENTER_TOLERANCE:
                    value = 0

                pos.set(event.code, value)





