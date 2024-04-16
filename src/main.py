#  Copyright (c) 2024 Thijn Hoekstra


import serial
import threading
import keyboard

import gcode
from serial_connection import read_serial_thread, send_serial

SPEED = 500

# Serial port settings
SERIAL_PORT = '/dev/ttyACM0'  # Change this to your serial port
BAUD_RATE = 250000
TIMEOUT = 1


def keyboard_callback(key):
    # Send the key to the serial device
    if key.event_type == keyboard.KEY_DOWN:
        return gcode.move(x=20, speed=SPEED)

    elif key.event_type == keyboard.KEY_UP:
        return gcode.move(x=-20, speed=SPEED)
    else:
        return None




# Main function
def main():
    # Open serial port
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)

    # Start a thread to read data from the serial port
    read_thread = threading.Thread(target=read_serial_thread, args=(ser,), daemon=True)
    read_thread.start()

    print("Press 'q' to quit.")

    # Set axes to relative mode
    send_serial(ser, gcode.relative_positioning())

    # Main loop to handle key presses
    while True:
        if keyboard.is_pressed('q'):
            print("Exiting...")
            break

        # Get the pressed key
        key = keyboard.read_event(suppress=True)
        action = keyboard_callback(key)

        if action:
            send_serial(ser, action)

    # Close serial port
    ser.close()

if __name__ == "__main__":
    main()
