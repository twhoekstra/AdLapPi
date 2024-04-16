#  Copyright (c) 2024 Thijn Hoekstra
from typing import Union

FEEDRATE_ALIAS = 'speed'

def move(letter: str = "G", number: int = 0, **kwargs):
    if letter not in ["G", "M", "T"]:
        raise ValueError("Error, Gcode letter must either be G, M, or T.")

    if FEEDRATE_ALIAS in kwargs:
        kwargs["f"] = kwargs.pop(FEEDRATE_ALIAS)

    s = f"{letter}{number} " + " ".join(
        f"{k.upper()}{v}" for k, v in kwargs.items())

    return s

def relative_positioning():
    return "G91"

def absolute_positioning():
    return "G90"

def home(axes: Union[list, str] = None):
    if axes is None:
        return "G28"
    elif axes is str:
        axes = [axes]

    else:
        return "G28 " + " ".join(a.upper() for a in axes)


