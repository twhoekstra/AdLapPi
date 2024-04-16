#  Copyright (c) 2024 Thijn Hoekstra

import serial, string

output = " "
ser = serial.Serial('/dev/ttyUSB0', 4800, 8, 'N', 1, timeout=1)
while True:
  print("----")
  while output:
    output = ser.readline()
    print(output)

  output = " "