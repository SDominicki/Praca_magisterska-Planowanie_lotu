#include <PID_v1.h>

double Setpoint1, Input1, Output1;
double Setpoint2, Input2, Output2;
double Kp=15, Ki=1, Kd=0.3;

PID myPID1(&Input1, &Output1, &Setpoint2, Kp, Ki, Kd, DIRECT);
PID myPID2(&Input2, &Output2, &Setpoint1, Kp, Ki, Kd, DIRECT);

int zero = 0;
int max = 255;

String data_in;
float output;
int first_value;
int second_value;
int third_value;
int fourth_value;
String sm;
int state_machine;
String aileron;
String elevator;
String data_out;
float aileron_calc;
float elevator_calc;

void setup() 
{
  Serial.begin(115200);
  Serial.setTimeout(1);

  Setpoint1 = 75;
  Setpoint2 = 75;
  
  myPID1.SetMode(AUTOMATIC);
  myPID2.SetMode(AUTOMATIC);
  //turn the PID on
  myPID1.SetTunings(Kp,Ki,Kd);
  myPID2.SetTunings(Kp,Ki,Kd);
  myPID1.SetOutputLimits(-1000,1000);
  myPID1.SetInputLimits(-100,100);
  myPID2.SetOutputLimits(-1000,1000);
  myPID2.SetInputLimits(-100,100);
}

void loop() 
{

  while (!Serial.available());
  data_in = Serial.readString();
  sm = data_in.substring(0,1);
  state_machine = sm.toInt();
  first_value = data_in.indexOf("A");
  second_value = data_in.indexOf(";");
  third_value = data_in.indexOf("E");
  fourth_value = data_in.indexOf(";", third_value+1);
  aileron = data_in.substring(first_value+1,second_value);
  elevator = data_in.substring(third_value+1,fourth_value);
  aileron_calc = aileron.toFloat();
  elevator_calc = elevator.toFloat();
  aileron = "";
  elevator = "";

  Input1 = analogRead(0);
  myPID1.Compute();
  analogWrite(3, Output1);

  Input2 = analogRead(1);
  myPID2.Compute();
  analogWrite(9, Output2);

  switch (state_machine)
  {
    case 0:
    {
      aileron_calc = aileron_calc * 5;
      elevator_calc = elevator_calc * 5;
      break;
    }
    case 1:
    { 
      aileron_calc = aileron_calc * 10;
      elevator_calc = elevator_calc * 10;
      break;
    }
    case 2:
    {
      aileron_calc = aileron_calc * 100;
      elevator_calc = elevator_calc  * 100;
      break;
    }
    case 3:
    {
      aileron_calc = aileron_calc / 10;
      elevator_calc = elevator_calc  / 10;
      break;
    }
    case 4:
    {
      aileron_calc = aileron_calc + 5;
      elevator_calc = elevator_calc  - 5;
      break;
    }
    default:
      Serial.print("Dupa");
  }
  aileron = String(aileron_calc,3);
  elevator = String(elevator_calc,3);
  data_out = "A" + aileron + ";E" + elevator + "SM" + sm;
  Serial.print(data_out);
}