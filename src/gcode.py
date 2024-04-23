#  Copyright (c) 2024 Thijn Hoekstra
from typing import Union

import numpy as np

FEEDRATE_ALIAS = 'speed'

def move(letter: str = "G", number: int = 0, **kwargs):
    if letter not in ["G", "M", "T"]:
        raise ValueError("Error, Gcode letter must either be G, M, or T.")

    if FEEDRATE_ALIAS in kwargs:
        kwargs["f"] = kwargs.pop(FEEDRATE_ALIAS)

    if "vector" in kwargs:
        if "order" not in kwargs:
            order = "xyz"
        else:
            order = kwargs.pop("order")

        vec = kwargs.pop("vector")
        if not isinstance(vec, (list, np.ndarray)):
            raise ValueError(f"Error, got vector input but input is of type "
                             f"{type(vec)}")
        elif len(vec) != len(order):
            raise ValueError(f"Error, vector length does not match length "
                             f"expected due to order setting: {order}. "
                             f"Expected vector of length {len()} but got "
                             f"{len(vec)}. Resolve this by chaning the order or "
                             f"the vector.")

        for k, v in zip(order, vec):
            kwargs[k] = v

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


