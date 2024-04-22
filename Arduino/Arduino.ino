#include <PID_v1.h>

double Setpoint1, Input1, Output1;
double Setpoint2, Input2, Output2;
double Kp=1, Ki=0, Kd=0;

PID myPID1(&Input1, &Output1, &Setpoint2, Kp, Ki, Kd, DIRECT);
PID myPID2(&Input2, &Output2, &Setpoint1, Kp, Ki, Kd, DIRECT);

int zero = 0;
int max = 255;

void setup() {

  Serial.begin(9600);

  Setpoint1 = 75;
  Setpoint2 = 75;
  
  myPID1.SetMode(AUTOMATIC);
  myPID2.SetMode(AUTOMATIC);
  //turn the PID on
  myPID1.SetTunings(Kp,Ki,Kd);
  myPID2.SetTunings(Kp,Ki,Kd);
}

void loop() {
  
  Input1 = analogRead(0);
  myPID1.Compute();
  analogWrite(3, Output1);

  Input2 = analogRead(1);
  myPID2.Compute();
  analogWrite(9, Output2);
  Serial.print("PID1 INPUT:");
  Serial.println(Input1);
  Serial.print("PID1 OUTPUT:");
  Serial.println(Output1);

  Serial.print("PID2 INPUT:");
  Serial.println(Input2);
  Serial.print("PID2 OUTPUT:");
  Serial.println(Output2);
  
  delay(1000);

}

