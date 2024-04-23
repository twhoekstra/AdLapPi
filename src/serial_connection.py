#  Copyright (c) 2024 Thijn Hoekstra

import time
import serial
def read_serial_thread(serial_port):
    while True:
        try:
            data = serial_port.readline().decode().strip()
            if data:
                print("Received:", data)
        except serial.SerialException as e:
            print("Serial error:", e)
            break

def send_serial(serial_port, data):
    try:
        print(f"Sent: {data}")
        serial_port.write(data.encode())
        time.sleep(0.001)
    except serial.SerialException as e:
        print("Serial error:", e)

if __name__ == '__main__':
    pass