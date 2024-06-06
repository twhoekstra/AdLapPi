#  Copyright (c) 2024 Thijn Hoekstra

import time
import warnings

import serial
import logging

BAUD_RATE = 250000
TIMEOUT = 1

logger = logging.getLogger(__name__)

def acquire_arduinos(serial_ports):

    arduinos = []

    for arm, serial_port in zip(("Left", "Right"), serial_ports):
        if serial_port:
            ser = wait_to_get_arduino(serial_port, arm)
        else:
            ser = None
            warnings.warn(f"Using dummy arduino for {arm} side.")

        arduinos.append(ser)

    return arduinos

def wait_to_get_arduino(port, arduino_id=None, timeout=5, check_every=0.1) -> serial.Serial:
    if arduino_id is None:
        arduino_id = ''
    else:
        arduino_id = arduino_id + ' '

    start_time = time.time()

    while True:
        try:
            ser = serial.Serial(port, BAUD_RATE, timeout=TIMEOUT)
            return ser
        except serial.SerialException:
            pass
        if time.time() - start_time > timeout:
            break

        time.sleep(check_every)
        logger.info(f"Couldn't find {arduino_id}Arduino. Trying again in {check_every} seconds...")


    raise RuntimeError(f"Error: {arduino_id}Arduino not found.")


def read_serial_thread(serial_port):
    while True:
        try:
            data = serial_port.readline().decode().strip()
            if data:
                logger.debug(f"Received: {data}" )
        except serial.SerialException as e:
            logger.info(f"Serial error: {e}")
            break

def send_serial(serial_port, data):
    if serial_port:
        try:
            logger.debug(f"Sent: {data}")
            serial_port.write(data.encode())
            time.sleep(0.001)
        except serial.SerialException as e:
            logger.info(f"Serial error: {e}")

def send_serials(serial_ports, data):
    if isinstance(serial_ports, (list, tuple)):
        for serial_port in serial_ports:
            send_serial(serial_port, data)
    else:
        send_serial(serial_ports, data)

if __name__ == '__main__':
    pass