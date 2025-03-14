#include <Servo.h>

const int trans_pin = 10; //Trig
const int recv_pin = 11; //Echo

float distance = 0;

Servo myservo;

int angle;

void setup() {
  myservo.attach(9);

  Serial.begin(9600);
  pinMode(trans_pin,OUTPUT); //transmit is ouput
  pinMode(recv_pin,INPUT); //receive is input
}

void loop() {

  distance = calcDist(distance, 0.34);

  angle = 90-(distance-0.14)*300;



  // Serial.println(angle);
  myservo.write(angle);

  Serial.print(distance);
  Serial.println("m");

  delay(100); // can alter based on needs of application
}

float calcDist(float oldDist, float maxDist) {
  float duration; //time var

  digitalWrite(trans_pin,LOW); // ensure no errant transmission
  delayMicroseconds(5);

  digitalWrite(trans_pin,HIGH); // transmit
  delayMicroseconds(10);

  digitalWrite(trans_pin,LOW); // stop transmission
  duration = pulseIn(recv_pin,HIGH); // listen for pulses

  float distRaw = duration*(340)/(2*1000000); // calculate distance
  /*
  d = c*delta(t)/2
  c = 340 m/s
  39.79 inch per meter
  duration is in microseconds, so 1*10^6 is divided
  */

  if (maxDist < distRaw) {
    return oldDist;
  }
  if (distRaw < 0.0) {
    return 0.01;
  }


  return distRaw;
}

void setAngle(float angle) {
  myservo.write(angle);
}
