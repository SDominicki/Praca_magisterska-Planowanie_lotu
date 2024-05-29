from simple_pid import PID
import serial
import time
from flightgear_python.fg_if import TelnetConnection, HTTPConnection
from xml_reader import xml_reader
import math

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

sm = 0
last_flight_phase = 0
elevator_tbs = 0.0
aileron_tbs = 0.0
previous_elevator = elevator_tbs
previous_aileron = aileron_tbs
turn_radius = 0.8 #Nautical Miles

pid_roll =       PID(0.05, 0.005, 0.05, output_limits=(-0.5,0.5), starting_output=0)
pid_small_roll = PID(0.05, 0.01, 0.05, output_limits=(-1.5,1.5), starting_output=0)
pid_climb_rate = PID(-0.4, -0.2, -0.6, setpoint=0.0, output_limits=(-0.25,0.25), starting_output=0)

telnet_conn = TelnetConnection('localhost', 5500)
#telnet_conn = HTTPConnection('localhost', 8080)
telnet_conn.connect()  # Make an actual connection

telnet_conn.set_prop('/controls/flight/aileron-trim', 0)
telnet_conn.set_prop('/controls/flight/elevator-trim', 0)
telnet_conn.set_prop('/controls/flight/rudder-trim', 0)
telnet_conn.set_prop('/controls/flight/rudder-trim', 0)
telnet_conn.set_prop('/controls/flight/flaps', 0)
telnet_conn.set_prop('/controls/engines/engine/throttle', 0.75)
telnet_conn.set_prop('/controls/engines/engine[1]/throttle', 0.75)
telnet_conn.set_prop('/controls/engines/engine[2]/throttle', 0.75)

arduino.timeout = 0.1

def limiter(n, min_n, max_n):

    if n < min_n:
        return min_n

    if n > max_n:
        return max_n

    else:
        return n

def position_getter():

    longitude = telnet_conn.get_prop('/position/model/longitude-deg')
    latitude = telnet_conn.get_prop('/position/model/latitude-deg')

    position = f"{longitude};{latitude}" #16.88583374;51.10277939
    arduino.write(bytes(position.encode()))
    return 

def speed_getter():
    true_airspeed = float(telnet_conn.get_prop('/fdm/jsbsim/velocities/vtrue-kts'))
    return true_airspeed

def arduino_reader():
    msg = arduino.readline().decode()
    return msg

def roll_calculator():

    roll_deg = telnet_conn.get_prop('/orientation/model/roll-deg')
    
    roll_error = roll_deg - pid_roll.setpoint   # Calculate error
    
    roll_constant = 0.1

    aileron_tbs = previous_aileron + ((pid_roll(roll_error))*roll_constant)

    return aileron_tbs

def small_roll_calculator():

    roll_deg = telnet_conn.get_prop('/orientation/model/roll-deg')

    if (pid_small_roll.setpoint - 0.5 < roll_deg < pid_small_roll.setpoint + 0.5):

        aileron_tbs = previous_aileron
        
    else:

        roll_error = roll_deg - pid_small_roll.setpoint  # Calculate error

        roll_constant = 0.1

        aileron_tbs = previous_aileron + ((pid_small_roll(roll_error))*roll_constant)

    return aileron_tbs

def climb_rate_calculator():

    climb_rate = (telnet_conn.get_prop('/velocities/vertical-speed-fps'))
    
    if (pid_climb_rate.setpoint - 0.2 < climb_rate < pid_climb_rate.setpoint + 0.2):

        elevator_tbs = previous_elevator

    else:

        climb_rate_error = climb_rate + pid_climb_rate.setpoint  # Calculate error
        
        climb_rate_constant = 0.1

        elevator_tbs = previous_elevator + (pid_climb_rate(climb_rate_error)*climb_rate_constant)

    return elevator_tbs

while True:
    
    #start = time.time()

    if(sm==0):
        position_getter()
    time.sleep(0.01)

    flight_phase = arduino.read(1).decode('utf_8')
    if flight_phase!='':
        flight_phase = int(flight_phase)

    if type(flight_phase)==str:
        flight_phase=last_flight_phase
        
    print(flight_phase)

    if flight_phase == 0:

        pid_small_roll.setpoint = 0.0
        #print("Lot poziomy")
        aileron_tbs = limiter(small_roll_calculator(),-0.2,0.2)

    if flight_phase == 1:

        true_airspeed = speed_getter()*0.5144
        pid_roll.setpoint = -math.degrees(math.atan((true_airspeed*true_airspeed)/((turn_radius*1852)*9.81)))
        print(pid_roll.setpoint)
        #print("Zakręt w lewo")
        aileron_tbs = limiter(roll_calculator(),-0.4,0.4)

    if flight_phase == 2:
        
        true_airspeed = speed_getter()*0.5144
        pid_roll.setpoint = math.degrees(math.atan((true_airspeed*true_airspeed)/((turn_radius*1852)*9.81)))
        print(pid_roll.setpoint)
        #print("Zakręt w prawo")
        aileron_tbs = limiter(roll_calculator(),-0.4,0.4)

    if flight_phase == 3:
        
        pid_small_roll.setpoint = -3.0
        #print("Korekta w lewo")
        aileron_tbs = limiter(small_roll_calculator(),-0.3,0.2)

    if flight_phase == 4:
        
        pid_small_roll.setpoint = 3.0
        #print("Korekta w prawo")
        aileron_tbs = limiter(small_roll_calculator(),-0.2,0.3)

    if flight_phase == 5:

        true_airspeed = speed_getter()*0.5144
        pid_roll.setpoint = math.degrees(math.atan((true_airspeed*true_airspeed)/((0.6*1852)*9.81)))
        #print("Zawracanie")
        aileron_tbs = limiter(roll_calculator(),-0.4,0.4)

    if  type(flight_phase)!=str:
        #print(f"Aileron tbs = {aileron_tbs}")
        telnet_conn.set_prop('/controls/flight/aileron', aileron_tbs)
    
    if(sm==1):
        elevator_tbs = limiter(climb_rate_calculator(),-0.05,0.05)
        telnet_conn.set_prop('/controls/flight/elevator', elevator_tbs)
 
    sm = sm+1

    previous_elevator = elevator_tbs
    previous_aileron = aileron_tbs

    if(sm>=2):
        sm=0
    
    if type(flight_phase)!=str:
        last_flight_phase = flight_phase

    #end = time.time()
    
    #print(f"Loop time = {round(end-start,2)}")