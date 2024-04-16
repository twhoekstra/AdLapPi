#  Copyright (c) 2024 Thijn Hoekstra

import unittest
from src.gcode import move, home

class GcodeMoveTestCase(unittest.TestCase):
    def test_x_move(self):
        s = move("G", 0, x=12)

        self.assertEqual("G0 X12", s)

    def test_y_move(self):
        s = move(y=12)

        self.assertEqual("G0 Y12", s)

    def test_y_move_feedrate(self):
        s = move("G", 0, y=12, f=1500)

        self.assertEqual("G0 Y12 F1500", s)
    def test_y_move_feedrate_alias(self):
        s = move("G", 0, y=12, speed=1500)

        self.assertEqual("G0 Y12 F1500", s)

    def test_x_y_move(self):
        s = move(x=12, y=12)

        self.assertEqual("G0 X12 Y12", s)

class GcodeHomeTestCase(unittest.TestCase):

    def test_home_all(self):
        s = home()
        self.assertEqual("G28", s)

    def test_home_x(self):
        s = home(["x"])
        self.assertEqual("G28 X", s)

    def test_home_xy(self):
        s = home(["x", "y"])
        self.assertEqual("G28 X Y", s)

    def test_home_x_convenience(self):
        s = home("x")
        self.assertEqual("G28 X", s)



if __name__ == '__main__':
    unittest.main()
