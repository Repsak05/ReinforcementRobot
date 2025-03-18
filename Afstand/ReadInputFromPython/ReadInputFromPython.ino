#include <Servo.h>

const int servoPin = 9;
const int trans_pin = 10; //Trig
const int recv_pin = 11; //Echo

const unsigned long baudRate = 115200;

const float CENTER_DISTANCE = 0.14;
float distance = 12;

Servo myservo;

void setup() {
  Serial.begin(baudRate);
  myservo.attach(servoPin); 
  
  pinMode(trans_pin,OUTPUT); //transmit is ouput
  pinMode(recv_pin,INPUT); //receive is input
}

void loop() {

  int rx = 0;
  if(Serial.available()){
    // Read and write angle to servo
    rx = Serial.read(); //Read raw byte value - Should be directly parseable as integer (0-180) ... technically uint8_t (char) but well within bounds for a regular signed int.
    myservo.write(rx);
  
    //Calculate and send distance
    Serial.println(calcDist(distance));

    if(rx == 180) Serial.println(u8"\U0001f60e");
    if(rx == 0) Serial.println(u8"\U0001F4A9");
  } 
}


float calcDist(float oldDist) {
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

  if(distRaw > 0.0 && distRaw <= 2 * CENTER_DISTANCE){
    return distRaw;
  }else{
    // Serial.println("NOT VALID:");
    // Serial.println(distRaw);
    return oldDist;
  }
}
