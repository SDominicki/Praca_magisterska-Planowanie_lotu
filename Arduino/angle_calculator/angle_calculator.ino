#include <math.h>

float GPS_1[2] = {-10,1};
float GPS_2[2] = {10,4};
float P[2] = {-1,6};

float diameter = 10;
float circle_center[4] = {0,0,0,0};
float true_circle_center[2] = {0,0};

float vector_1[2] = {0,0};
float vector_2[2] = {0,0};

float positive_angled[2] = {0,0};
float negative_angled[2] = {0,0};
float comparison_point[2] = {0,0};
float tangent_1[2] = {0,0};
float tangent_2[2] = {0,0};

void setup() {
  Serial.begin(115200);
}

float magnitude_calc(float x,float y)
{
  float magnitude = (x*x + y*y);
  magnitude = pow(magnitude, 0.5);

  return magnitude;
}

float tangent_calculator(float x_0, float y_0, float x_1, float y_1, float h, float k, float diameter) //https://math.stackexchange.com/questions/311921/get-location-of-vector-circle-intersection
{
  float a = (x_1-x_0)*(x_1-x_0)+(y_1-y_0)*(y_1-y_0);
  float b = 2*(x_1-x_0)*(x_0-h)+2*(y_1-y_0)*(y_0-k);
  float c = (x_0-h)*(x_0-h)+(y_0-k)*(y_0-k)-(diameter/2*diameter/2);
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

String printer(float var)
{
  Serial.println(var,4);
}

void loop() {

  vector_1[0] = (P[0]-GPS_1[0]);
  vector_1[1] = (P[1]-GPS_1[1]);

  vector_2[0] = (P[0]-GPS_2[0]);
  vector_2[1] = (P[1]-GPS_2[1]);

  float dot_product = vector_1[0] * vector_2[0] + vector_1[1] * vector_2[1];

  float magnitude_1 = magnitude_calc(vector_1[0],vector_1[1]);
  float magnitude_2 = magnitude_calc(vector_2[0],vector_2[1]);

  float resultAngle = acos(dot_product/(magnitude_1*magnitude_2));
  
  float distance_from_circle_center = (diameter/2)/(sin(resultAngle/2));

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

  float distance_from_positive = ((comparison_point[0]-positive_angled[0])*(comparison_point[0]-positive_angled[0]))+(comparison_point[1]-positive_angled[1])*(comparison_point[1]-positive_angled[1]);
  distance_from_positive = pow(distance_from_positive, 0.5);

  float distance_from_negative = ((comparison_point[0]-negative_angled[0])*(comparison_point[0]-negative_angled[0]))+((comparison_point[1]-negative_angled[1])*(comparison_point[1]-negative_angled[1]));
  distance_from_negative = pow(distance_from_negative, 0.5);
  
  if (distance_from_negative - distance_from_positive > 0) {
  true_circle_center[0] = circle_center[0];
  true_circle_center[1] = circle_center[1];
  }
  else if (distance_from_negative - distance_from_positive < 0) {
  true_circle_center[0] = circle_center[2];
  true_circle_center[1] = circle_center[3];
  }

  float tangent_coefficient_1 = tangent_calculator(GPS_1[0], GPS_1[1], P[0], P[1], true_circle_center[0], true_circle_center[1], diameter);
  float tangent_coefficient_2 = tangent_calculator(GPS_2[0], GPS_2[1], P[0], P[1], true_circle_center[0], true_circle_center[1], diameter);

  tangent_1[0] = (P[0]-GPS_1[0])*tangent_coefficient_1+GPS_1[0];
  tangent_1[1] = (P[1]-GPS_1[1])*tangent_coefficient_1+GPS_1[1];

  tangent_2[0] = (P[0]-GPS_2[0])*tangent_coefficient_2+GPS_2[0];
  tangent_2[1] = (P[1]-GPS_2[1])*tangent_coefficient_2+GPS_2[1];

  //printer(tangent_coefficient_1);
  //printer(tangent_coefficient_2);
  //printer(tangent_1[0]);
  //printer(tangent_1[1]);
  //printer(tangent_2[0]);
  //printer(tangent_2[1]);

  delay(100);
}
