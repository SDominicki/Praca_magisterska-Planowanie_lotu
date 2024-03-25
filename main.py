from simple_pid import PID
import time
from flightgear_python.fg_if import TelnetConnection

roll_deg_setpoint = 0.0
pitch_deg_setpoint = 0.0
heading_setpoint = 0.0
climb_rate_setpoint = 5.0
sm = 0

pid_roll = PID(15, 1, 0.3, setpoint=roll_deg_setpoint, output_limits=(-0.5,0.5), sample_time=0.5, starting_output=0)
pid_pitch = PID(1.1, 0.1, 0.3, setpoint=pitch_deg_setpoint, output_limits=(-0.1,0.1), sample_time=0.5, starting_output=0)
pid_heading = PID(1.1, 0.1, 0.3, setpoint=heading_setpoint, output_limits=(-0.1,0.1), sample_time=0.5, starting_output=0)
pid_climb_rate = PID(1.1, 0.1, 15, setpoint=climb_rate_setpoint*60, output_limits=(-0.1,0.1), sample_time=0.5, starting_output=0)

telnet_conn = TelnetConnection('localhost', 5500)
telnet_conn.connect()  # Make an actual connection

def roll_calculator():

    roll_deg = telnet_conn.get_prop('/orientation/roll-deg')

    roll_error = roll_deg_setpoint - roll_deg  # Calculate error
    
    roll_constant = 0.1

    if (roll_error >= 0.01):
        aileron_tbs = roll_error * ((pid_roll(roll_deg))*roll_constant)

    if (roll_error <= 0.01):
        aileron_tbs = roll_error * -((pid_roll(roll_deg))*roll_constant)

    #print(f"Roll error = {round(roll_error,2)}")

    return aileron_tbs

def pitch_calculator():


    pitch_deg = telnet_conn.get_prop('/orientation/pitch-deg')

    pitch_error = pitch_deg_setpoint - pitch_deg  # Calculate error
    
    pitch_constant = 0.1

    if (pitch_error >= 0.1):
        elevator_tbs = pitch_error * ((pid_pitch(pitch_deg))*pitch_constant)

    if (pitch_error <= -0.1):
        elevator_tbs = pitch_error * -((pid_pitch(pitch_deg))*pitch_constant)

    print(f"Pitch error = {round(pitch_error,2)}")

    return elevator_tbs

def climb_rate_calculator():

    climb_rate = (telnet_conn.get_prop('/velocities/vertical-speed-fps')) * 60

    climb_rate_error = climb_rate_setpoint*60 - climb_rate  # Calculate error
    
    climb_rate_constant = 0.003

    if (climb_rate_error >= 50):
        elevator_tbs = climb_rate_error * -(pid_climb_rate(climb_rate)*climb_rate_constant)

    if (climb_rate_error <= -50):
        elevator_tbs = climb_rate_error * (pid_climb_rate(climb_rate)*climb_rate_constant)

    if (climb_rate_error < 50 and climb_rate_error > -50):
        elevator_tbs = climb_rate_error * (pid_climb_rate(climb_rate)*(climb_rate_constant/5))

    print(f"Climb rate error = {round(climb_rate_error,2)} ; Climb rate = {round(climb_rate,2)} ; Elevator tbs = {round(elevator_tbs,2)}")
    
    return elevator_tbs

def heading_calculator():

    heading_deg = telnet_conn.get_prop('/orientation/track-magnetic-deg')

    heading_error = heading_setpoint - heading_deg

    if -360 <= heading_error <= -180:
        true_heading_error = heading_error + 360
    elif 180 <= heading_error <= 360:
        true_heading_error = heading_error - 360
    else:
        true_heading_error = heading_error

    return true_heading_error

while True:

    start = time.time()

    #alt_ft = telnet_conn.get_prop('/position/altitude-ft')
    
    if(sm==0):
        elevator_tbs = climb_rate_calculator()
        telnet_conn.set_prop('/controls/flight/elevator', elevator_tbs)
    if(sm==1):
        aileron_tbs = roll_calculator()
        telnet_conn.set_prop('/controls/flight/aileron', aileron_tbs)

    sm = sm+1
    
    if(sm>=2):
        sm=0

    end = time.time()
    #print(f"Loop time = {round(end-start,2)}")