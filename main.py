from simple_pid import PID
import time
import math
import keyboard
from flightgear_python.fg_if import FDMConnection, CtrlsConnection

roll_deg_setpoint = 0.00
pitch_deg_setpoint = 0.00
yaw_deg_setpoint = 0.00
heading_setpoint = 0.0
climb_rate_setpoint = 3.0

pid_roll = PID(15, 1, 0.3, setpoint=roll_deg_setpoint, auto_mode= True, output_limits=(-1,1), sample_time=0.01, starting_output=0)
pid_pitch = PID(15, 1, 0.3, setpoint=pitch_deg_setpoint, auto_mode= True, output_limits=(-1,1), sample_time=0.01, starting_output=0)
pid_yaw = PID(15, 1, 0.3, setpoint=yaw_deg_setpoint, auto_mode= True, output_limits=(-1,1), sample_time=0.01, starting_output=0)
pid_heading = PID(15, 1, 0.3, setpoint=heading_setpoint, auto_mode= True, output_limits=(-1,1), sample_time=0.01, starting_output=0)
pid_climb_rate = PID(1.1, 0.2, 1, setpoint=climb_rate_setpoint, auto_mode= True, output_limits=(-1,1), sample_time=0.01, starting_output=0)

child_aileron_state = 0.0
child_rudder_state = 0.0
child_elevator_state = 0.0
child_elevator_trim = 0.0

def ctrls_callback(ctrls_data, event_pipe):

    global child_aileron_state
    global child_elevator_state
    global child_rudder_state
    global child_elevator_trim_state
   
    if (True):
        child_aileron,child_elevator,child_rudder,child_elevator_trim  = event_pipe.child_recv()

    child_aileron_state = child_aileron
    child_elevator_state = child_elevator
    child_rudder_state = child_rudder
    child_elevator_trim_state = child_elevator_trim

    ctrls_data.aileron_trim = 0.0
    ctrls_data.aileron = child_aileron_state  # from -1..1
    ctrls_data.elevator = child_elevator_state
    ctrls_data.rudder = child_rudder_state
    ctrls_data.elevator_trim = child_elevator_trim_state

    return ctrls_data

def fdm_callback(fdm_data, event_pipe):
    pitch_deg = math.degrees(fdm_data.theta_rad) #PITCH
    roll_deg = math.degrees(fdm_data.phi_rad) #ROLL
    yaw_deg = math.degrees(fdm_data.beta_rad) #YAW
    heading_deg = math.degrees(fdm_data.psi_rad)
    climb_rate = fdm_data.climb_rate_ft_per_s
    event_pipe.child_send((pitch_deg,roll_deg,yaw_deg,heading_deg,climb_rate,)) # Send tuple to parent

"""
Start FlightGear with:
`--native-fdm=socket,out,30,localhost,5501,udp --native-ctrls=socket,out,30,localhost,5503,udp --native-ctrls=socket,in,30,localhost,5504,udp`
"""
if __name__ == '__main__':  # NOTE: This is REQUIRED on Windows!
    ctrls_conn = CtrlsConnection(ctrls_version=27)
    ctrls_event_pipe = ctrls_conn.connect_rx('localhost', 5503, ctrls_callback)
    ctrls_conn.connect_tx('localhost', 5504)

    fdm_conn = FDMConnection(fdm_version=24)  # May need to change version from 24
    fdm_event_pipe = fdm_conn.connect_rx('localhost', 5501, fdm_callback)

    ctrls_conn.start()  # Start the Ctrls RX/TX loop
    fdm_conn.start()  # Start the FDM RX loop

    while True:
        if fdm_event_pipe.parent_poll():  # Only update controller when we get FDM updates
            pipe_data = fdm_event_pipe.parent_recv()  # Unpack tuple from FDM
            parent_pitch_deg,parent_roll_deg,parent_yaw_deg,parent_heading_deg,parent_climb_rate = pipe_data
            roll_error = roll_deg_setpoint - parent_roll_deg  # Calculate error
            pitch_error = pitch_deg_setpoint - parent_pitch_deg
            yaw_error = yaw_deg_setpoint - parent_yaw_deg
            heading_error = heading_setpoint - parent_heading_deg

            climb_rate_error = climb_rate_setpoint - parent_climb_rate

            if -360 <= heading_error <= -180:
                true_heading_error = heading_error + 360
            elif 180 <= heading_error <= 360:
                true_heading_error = heading_error - 360
            else:
                true_heading_error = heading_error
            # Calculate the aileron request (technically should clamp to -1..1 but it doesn't really matter)


            roll_calculator = (pid_roll(parent_roll_deg))*0.1
            climb_rate_calculator = (pid_climb_rate(climb_rate_error))
            climb_rate_to_be_set = climb_rate_calculator

            if (roll_error > 0 and roll_error <= 20):
                parent_aileron_req = roll_error * roll_calculator
            elif(parent_roll_deg > 20):
                parent_aileron_req = 0.9

            if (roll_error < 0 and roll_error >= -20):
                parent_aileron_req = roll_error * -roll_calculator
            elif(parent_roll_deg < -20):
                parent_aileron_req = -0.9

            if (climb_rate_error > 0):
                parent_elevator_trim_req = climb_rate_error * (climb_rate_calculator*0.02)
            elif (climb_rate_error > 0 and parent_climb_rate < 0):
                parent_elevator_trim_req = climb_rate_error * (-climb_rate_calculator*0.02)

            if (climb_rate_error < 0):
                parent_elevator_trim_req = climb_rate_error * -(climb_rate_calculator*0.02)
            elif (climb_rate_error < 0 and parent_climb_rate > 0):
                parent_elevator_trim_req = climb_rate_error * (climb_rate_calculator*0.02)

            parent_elevator_req = 0.0

            if (yaw_error > 0.1):
                parent_rudder_req = yaw_error * (pid_yaw(parent_yaw_deg)*0.0001)
            if (yaw_error < -0.1):
                parent_rudder_req = yaw_error * (pid_yaw(parent_yaw_deg)*-0.0001)
            if ((yaw_error <= 0.1) & (yaw_error >= -0.1)): 
                parent_rudder_req = 0.0
            #Roll error = {round(roll_error,3)} ; 
            #Roll degrees = {round(parent_roll_deg,2)} ; 
            #Aileron position = {round(parent_aileron_req,3)} ; 
            #Heading = {round(parent_heading_deg,2)} ; 
            #Heading error = {round(true_heading_error,2)} ; 
            print(f"Climb rate = {round(parent_climb_rate,4)} ; Climb error = {round(climb_rate_error,4)} ; Climb rate to be set = {round(climb_rate_to_be_set,4)}")
            ctrls_event_pipe.parent_send((parent_aileron_req,parent_elevator_req,parent_rudder_req,parent_elevator_trim_req,))  # Send tuple to Ctrls
            
            if keyboard.is_pressed('k'):
                print("Test")
                ctrls_conn.connect_tx('localhost', 5504)
                ctrls_conn.start()  # Start the Ctrls RX/TX loop
                fdm_conn.start()  # Start the FDM RX loop


            if keyboard.is_pressed('q'):  # if key 'q' is pressed
                print("Loop broken")
                break  # finishing the loop

            time.sleep(0.01)  # Faster than 30Hz but still sleeping a bit
            
    ctrls_conn.start()
    fdm_conn.start()  # Start the FDM RX loop