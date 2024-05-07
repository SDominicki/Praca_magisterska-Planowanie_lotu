import serial
import time

arduino = serial.Serial(port='COM13',   baudrate=115200, timeout=0.01)
num = 0
aileron = 0.0
elevator = 0.0
i = 0

def write_read(x):
    arduino.write(bytes(x,   'utf-8'))
    data = arduino.readline()
    return   data

while True:
    if i <= 10:
        sm = 0
    if 10 < i <= 20:
        sm = 1
    if 20 < i <= 30:
        sm = 2
    if 30 < i <= 40:
        sm = 3
    if 40 < i <= 50:
        sm = 4
    if i >=51:
        i = 0

    aileron = aileron + 0.1
    elevator = elevator - 0.1
    if aileron >= 5 or elevator <= -5:
        aileron = 0
        elevator = 0
    data_in = f"{sm}A{round(aileron,3)};E{round(elevator,3)};"
    data_out = write_read(data_in)
    values = data_out.decode()
    print(values)
    i = i+1
    