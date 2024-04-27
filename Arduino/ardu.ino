#include <floatToString.h>

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

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
}

void  loop() {

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