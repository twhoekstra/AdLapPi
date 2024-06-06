#  Copyright (c) 2024 Thijn Hoekstra
import numpy as np


class Limit:

    def __init__(self, start: float, end: float, home_to_min=True):
        self.min = start
        self.max = end
        self.home_to_min = home_to_min


class ArmLimits:

    def __init__(self,
                 x_min, x_max,
                 y_min, y_max,
                 z_min, z_max,
                 x_home_to_min=True,
                 y_home_to_min=True,
                 z_home_to_min=True):
        self.x = Limit(x_min, x_max, x_home_to_min)
        self.y = Limit(y_min, y_max, y_home_to_min)
        self.z = Limit(z_min, z_max, z_home_to_min)


class BothLimits:

    def __init__(self, left: ArmLimits, right: ArmLimits):
        self.left = left
        self.right = right
        self._max_array = self.get_max_array()
        self._min_array = self.get_min_array()

    def get_min_array(self):
        return np.array([
            [self.left.x.min, self.left.y.min, self.left.z.min, ],
            [self.right.x.min, self.right.y.min, self.right.z.min, ],
        ])
    def get_max_array(self):
        return np.array([
            [self.left.x.max, self.left.y.max, self.left.z.max, ],
            [self.right.x.max, self.right.y.max, self.right.z.max, ],
        ])

    def check_array_outside_limit(self, a):
        if np.any(np.less_equal(a, self._min_array)):
            return True
        elif np.any(np.greater_equal(a, self._max_array)):
            return True
        else:
            return False

ADLAP_LIMITS = BothLimits(
    ArmLimits(0, 150,
              0, 200,
              0, 150),
    ArmLimits(0, 150,
              0, 200,
              150, 300, z_home_to_min=False),
)