import serial
import time
from xml_reader import xml_reader

points = xml_reader()
point_len = len(points)
i=0
x=0

arduino = serial.Serial(port='COM5', baudrate=115200, timeout=0.01)

while arduino.readline().decode() != 'ReadyA':
        time.sleep(0.05)
        arduino.write(bytes("ReadyP", 'utf-8'))

time.sleep(0.5)

arduino.write(bytes(str(len(points)), 'utf-8'))

time.sleep(0.5)

while i < len(points):
    
    to_send = str(points[i]) #16.88583374;51.10277939;i

    arduino.write(bytes(to_send.encode()))
    print(to_send)
    time.sleep(0.2)
    i = i + 1

time.sleep(1)
arduino.flush()

while arduino.readline().decode() != 'ReadyA':
        time.sleep(0.05)
        arduino.write(bytes("ReadyP", 'utf-8'))

while True:

    time.sleep(0.5)
