from simple_pid import PID
import time
import math
from flightgear_python.fg_if import FDMConnection, CtrlsConnection

pid_roll = PID(5, 1, 0.3, setpoint=0.0, auto_mode= True, sample_time=0.01)
pid_pitch = PID(5, 1, 0.3, setpoint=0.0, auto_mode= True, sample_time=0.01)

child_aileron_state = 0.0
child_rudder_state = 0.0
child_elevator_state = 0.0
def ctrls_callback(ctrls_data, event_pipe):
    global child_aileron_state
    global child_rudder_state
    global child_elevator_state
    if event_pipe.child_poll():
        ctrl_pipe, = event_pipe.child_recv()
        # Unpack tuple from parent
        # TODO: FG sometimes ignores "once" updates? i.e. if we set `ctrls_data.aileron`
        #  the next callback will still have the old value of `ctrls_data.aileron`, not
        #  the one that we set. To fix this we can just keep our own state of what the value
        #  should be and set it every time. I still need to figure out a clean way to fix
        #  this on the backend
        child_aileron_state = child_aileron_req
        child_rudder_state = child_rudder_req
        child_elevator_state = child_elevator_req
    ctrls_data.aileron = child_aileron_state  # from -1..1
    return ctrls_data

def fdm_callback(fdm_data, event_pipe):
    roll_deg = math.degrees(fdm_data.phi_rad) #ROLL
    yaw_deg = math.degrees(fdm_data.psi_rad) #YAW
    pitch_deg = math.degrees(fdm_data.alpha_rad) #PITCH
    event_pipe.child_send((pitch_deg,roll_deg)) # Send tuple to parent

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

    roll_deg_setpoint = 0.0  # Let's say the setpoint is 5deg clockwise
    pitch_deg_setpoint = 0.0

    while True:
        if fdm_event_pipe.parent_poll():  # Only update controller when we get FDM updates
            pipe_data = fdm_event_pipe.parent_recv()  # Unpack tuple from FDM
            parent_pitch_deg = pipe_data[0]
            parent_roll_deg = pipe_data[1]
            roll_error = roll_deg_setpoint - parent_roll_deg  # Calculate error
            pitch_error = pitch_deg_setpoint - parent_pitch_deg
            # Calculate the aileron request (technically should clamp to -1..1 but it doesn't really matter)
            if (roll_error > 0):
                parent_aileron_req = roll_error * (pid_roll(parent_roll_deg)*0.001)
            if (roll_error < 0):
                parent_aileron_req = roll_error * (pid_roll(parent_roll_deg)*-0.001)

            if (pitch_error > 0):
                parent_elevator_req = pitch_error * (pid_pitch(parent_pitch_deg)*0.001)
            if (pitch_error < 0):
                parent_elevator_req = pitch_error * (pid_pitch(parent_pitch_deg)*-0.001)

            ctrls_event_pipe.parent_send((parent_aileron_req,parent_elevator_req))  # Send tuple to Ctrls

        time.sleep(0.01)  # Faster than 30Hz but still sleeping a bit