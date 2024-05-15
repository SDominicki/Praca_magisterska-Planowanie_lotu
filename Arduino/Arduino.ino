#include <LiquidCrystal.h>
const int rs = 6, en = 12, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

float GPS[100]; // Max 50 points
float Tangents[100]; // Max 50 points
int Turns[100]; //Max 50 turns

float Plane_curr[2]={0,0};
float Plane_prev[2]={0,0};

int iteration = 0;
int len = 0;
int i = 0;
int n = 0;
int m = 0;

int turn_radius = 0.4; //nautical miles
float turn_diameter = (turn_radius*2)/60;

void setup() 
{
  lcd.begin(16, 2);
  analogWrite(10,255);

  lcd.clear();
  lcd.print("    LAUNCHED    ");

  Serial.begin(115200);
  Serial.setTimeout(1);

  while (Serial.readString() != "ReadyP") 
  {
  Serial.print("ReadyA");
  delay(100);
  }
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("     READY      ");
  delay(500);

  len = Serial.readString().toInt();
  lcd.clear();
  lcd.print(len);
  delay(500);

  if (iteration <= len)
  {
    while (i <= len-1)
    {
      pointreader();
    }

    Serial.flush();
    delay(100);

    while (iteration <= len-6)
    {
      turnpoint_calculator(GPS[iteration],GPS[iteration+1],GPS[iteration+2],GPS[iteration+3],GPS[iteration+4],GPS[iteration+5],iteration);
      iteration = iteration + 2;
    }
  }

  lcd.clear();
  lcd.print(" Turns finished ");
  delay(500);

  while (Serial.readString() != "ReadyP") 
  {
  Serial.print("ReadyA");
  delay(100);
  }
}

void loop()
{

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(GPS[n],8);
  lcd.setCursor(14, 0);
  lcd.print(iteration);
  lcd.setCursor(0, 1);
  lcd.print(GPS[n+1],8);
  lcd.setCursor(14, 1);
  lcd.print(n);

  delay(2000);

  n = n + 2;

  if (n >= len)
    {
      n = 0;
    }
}

void position_getter()
{
  if (Serial.available() > 0)
  {
    String position = Serial.readString();
    Serial.flush();
    int breakpoint = position.indexOf(";");
    Plane_curr[0] = position.substring(0,breakpoint).toFloat();
    Plane_curr[1] = position.substring(breakpoint+1).toFloat();
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(Plane_curr[0]);
    lcd.setCursor(0, 1);
    lcd.print(Plane_curr[1]);
  }
}

void pointreader()
{
  if (Serial.available() > 0)
  {
    lcd.clear();
    String point = Serial.readString();
    GPS[i] = point.toFloat();
    lcd.print(point);
    lcd.setCursor(0, 1);
    lcd.print(i);

    i = i + 1;
  }
}

float turnpoint_calculator(float GPS_1_x, float GPS_1_y, float GPS_2_x, float GPS_2_y, float GPS_3_x, float GPS_3_y, int iteration)
{
  float GPS_1[2] = {0,0};
  float GPS_2[2] = {0,0};
  float P[2] = {0,0};

  float circle_center[4] = {0,0,0,0};
  float true_circle_center[2] = {0,0};

  float vector_1[2] = {0,0};
  float vector_2[2] = {0,0};

  float angle_degrees;

  float positive_angled[2] = {0,0};
  float negative_angled[2] = {0,0};
  float comparison_point[2] = {0,0};

  float tangent_1[2] = {0,0};
  float tangent_2[2] = {0,0};

  int turn_direction = 0;
  int iterator = iteration;

  GPS_1[0] = GPS_1_x;
  GPS_1[1] = GPS_1_y;
  P[0] = GPS_2_x;
  P[1] = GPS_2_y;
  GPS_2[0] = GPS_3_x;
  GPS_2[1] = GPS_3_y;

  vector_1[0] = (P[0]-GPS_1[0]);
  vector_1[1] = (P[1]-GPS_1[1]);

  vector_2[0] = (P[0]-GPS_2[0]);
  vector_2[1] = (P[1]-GPS_2[1]);

  float resultAngle = angle_calculator(GPS_1[0],GPS_1[1],P[0],P[1],GPS_2[0],GPS_2[1]);

  angle_degrees = degrees(resultAngle);

  if (angle_degrees >= 170 or angle_degrees <= -170)
  {
    tangent_1[0] = P[0];
    tangent_1[1] = P[1];
  }
  else
  {
  float distance_from_circle_center = (turn_diameter/2)/(sin(resultAngle/2));

  positive_angled[0] = P[0] + cos(resultAngle/2) * (GPS_1[0] - P[0]) - sin(resultAngle/2) * (GPS_1[1] - P[1]);    //https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
  positive_angled[1] = P[1] + sin(resultAngle/2) * (GPS_1[0] - P[0]) + cos(resultAngle/2) * (GPS_1[1] - P[1]);    //czasami dobrze obraca
  negative_angled[0] = P[0] + cos(-resultAngle/2) * (GPS_1[0] - P[0]) - sin(-resultAngle/2) * (GPS_1[1] - P[1]);  //czasami źle
  negative_angled[1] = P[1] + sin(-resultAngle/2) * (GPS_1[0] - P[0]) + cos(-resultAngle/2) * (GPS_1[1] - P[1]);  //dlatego sprawdzam dwa możliwe przypadki

  circle_center[0] = (positive_angled[0]-P[0]);
  circle_center[1] = (positive_angled[1]-P[1]);
  circle_center[2] = (negative_angled[0]-P[0]);
  circle_center[3] = (negative_angled[1]-P[1]);

  float circle_center_len = magnitude_calc(circle_center[0], circle_center[1]);

  float scale = distance_from_circle_center/circle_center_len;

  circle_center[0] = (circle_center[0] * scale) + P[0];
  circle_center[1] = (circle_center[1] * scale) + P[1];
  circle_center[2] = (circle_center[2] * scale) + P[0];
  circle_center[3] = (circle_center[3] * scale) + P[1];

  comparison_point[0] = GPS_1[0] - vector_2[0];
  comparison_point[1] = GPS_1[1] - vector_2[1];

  float distance_from_positive = distance_calculator(positive_angled[0], positive_angled[1], comparison_point[0], comparison_point[1]);

  float distance_from_negative = distance_calculator(negative_angled[0], negative_angled[1], comparison_point[0], comparison_point[1]);
  
  if (distance_from_negative - distance_from_positive > 0) {
  true_circle_center[0] = circle_center[0];
  true_circle_center[1] = circle_center[1];
  turn_direction = -1;
  }
  else if (distance_from_negative - distance_from_positive < 0) {
  true_circle_center[0] = circle_center[2];
  true_circle_center[1] = circle_center[3];
  turn_direction = 1;
  }

  float tangent_coefficient_1 = tangent_calculator(GPS_1[0], GPS_1[1], P[0], P[1], true_circle_center[0], true_circle_center[1], turn_diameter);
  float tangent_coefficient_2 = tangent_calculator(GPS_2[0], GPS_2[1], P[0], P[1], true_circle_center[0], true_circle_center[1], turn_diameter);

  tangent_1[0] = (P[0]-GPS_1[0])*tangent_coefficient_1+GPS_1[0];
  tangent_1[1] = (P[1]-GPS_1[1])*tangent_coefficient_1+GPS_1[1];

  tangent_2[0] = (P[0]-GPS_2[0])*tangent_coefficient_2+GPS_2[0];
  tangent_2[1] = (P[1]-GPS_2[1])*tangent_coefficient_2+GPS_2[1];
  }

  Tangents[iterator] = tangent_1[0];
  Tangents[iterator+1] = tangent_1[1];
  Turns[iterator] = turn_direction;
/*
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(Tangents[iterator],8);
  lcd.setCursor(14, 0);
  lcd.print(iterator);
  lcd.setCursor(0, 1);
  lcd.print(Tangents[iterator+1],8);
  lcd.setCursor(14, 1);
  lcd.print(Turns[iterator]);
*/
}

float magnitude_calc(float vector_x,float vector_y)
{
  float magnitude = (vector_x*vector_x + vector_y*vector_y);
  magnitude = pow(magnitude, 0.5);

  return magnitude;
}

float distance_calculator(float x_0, float y_0, float x_1, float y_1)
{
  float distance = ((x_1-x_0)*(x_1-x_0) + (y_1-y_0)*(y_1-y_0));
  distance = pow(distance, 0.5);

  return distance;
}

float tangent_calculator(float x_0, float y_0, float x_1, float y_1, float h, float k, float turn_diameter) //https://math.stackexchange.com/questions/311921/get-location-of-vector-circle-intersection
{

  //https://math.stackexchange.com/questions/311921/get-location-of-vector-circle-intersection

  float a = (x_1-x_0)*(x_1-x_0)+(y_1-y_0)*(y_1-y_0);
  float b = 2*(x_1-x_0)*(x_0-h)+2*(y_1-y_0)*(y_0-k);
  float c = (x_0-h)*(x_0-h)+(y_0-k)*(y_0-k)-(turn_diameter/2*turn_diameter/2);
  float delta = -1*(b*b)-4*a*c;

  //printer(a);
  //printer(b);
  //printer(c);

  if (delta <= 0)
    {
    delta = 0;
    }

  delta = pow(delta, 0.5);

  //printer(delta);

  float tangent = (2*c)/(-b+delta);

  return tangent;
}

float dot_product_calculator(float vector_0_x, float vector_0_y, float vector_1_x, float vector_1_y)
{
  float dot_product = vector_0_x * vector_1_x + vector_0_y * vector_1_y;

  return dot_product;
}

float angle_calculator(float x_0, float y_0, float x_1, float y_1, float x_2, float y_2)
{
  float vector_A[2] = {0,0};
  float vector_B[2] = {0,0};

  vector_A[0] = (x_1-x_0);
  vector_A[1] = (y_1-y_0);

  vector_B[0] = (x_1-x_2); //współrzędne zostały zmienione (powinno być x_2-x_1)
  vector_B[1] = (y_1-y_2); //w celu poprawnego liczenia kątu pomiędzy punktami

  float dot_product = dot_product_calculator(vector_A[0],vector_A[1],vector_B[0],vector_B[1]);

  float magnitude_A = magnitude_calc(vector_A[0],vector_A[1]);
  float magnitude_B = magnitude_calc(vector_B[0],vector_B[1]);

  float resultAngle = acos(dot_product/(magnitude_A*magnitude_B));

  return resultAngle;
}

int intersector_checker(float x_A, float y_A, float x_B, float y_B, float x_C , float y_C)
{
  //https://stackoverflow.com/questions/1073336/circle-line-segment-collision-detection-algorithm
  

  float real_radius = 0.1; //change for tighter target, unit is nautical miles
  float diameter_around_point = (real_radius*2)/60 ;

  float vector_AC[2] = {0,0};
  float vector_AB[2] = {0,0};

  vector_AC[0] = (x_C-x_A);
  vector_AC[1] = (y_C-y_A);

  vector_AB[0] = (x_B-x_A);
  vector_AB[1] = (y_B-y_A);

  float point_D[2] = {0,0};

  int intersector;

  float dot_product_AB = dot_product_calculator(vector_AC[0],vector_AC[1],vector_AB[0],vector_AB[1]);
  float dot_product_BB = dot_product_calculator(vector_AB[0],vector_AB[1],vector_AB[0],vector_AB[1]);

  float k = dot_product_AB/dot_product_BB;

  point_D[0] = (vector_AB[0]*k)+x_A;
  point_D[1] = (vector_AB[1]*k)+y_A;

  float distance_D_to_C = distance_calculator(point_D[0],point_D[1],x_C,y_C);

  if  (distance_D_to_C <= (diameter_around_point/2))
  {
    intersector = "0";
  }

  if  (distance_D_to_C > (diameter_around_point/2))
  {
    float point_D_positive[2] = {0,0};
    float point_D_negative[2] = {0,0};

    point_D_positive[0] = (vector_AB[0]*(k*2))+x_A;
    point_D_positive[1] = (vector_AB[1]*(k*2))+x_A;

    point_D_negative[0] = (vector_AB[0]*(k/2))+y_A;
    point_D_negative[1] = (vector_AB[1]*(k/2))+y_A;

    float distance_D_positive_to_C = distance_calculator(point_D_positive[0],point_D_positive[1],x_C,y_C);
    float distance_D_negative_to_C = distance_calculator(point_D_negative[0],point_D_negative[1],x_C,y_C);

    if (distance_D_positive_to_C < distance_D_negative_to_C)
      {
      intersector = -1;
      }

    else if (distance_D_positive_to_C > distance_D_negative_to_C)
      {
      intersector = 1;
      }

    else if (distance_D_positive_to_C = distance_D_negative_to_C)
      {
      intersector = 0;
      }  
  }
  return intersector;
}