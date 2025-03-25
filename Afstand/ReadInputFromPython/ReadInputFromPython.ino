#include <Servo.h>
#include <Wire.h>
#include <VL53L0X.h>

const int servoPin = 9;
const int trans_pin = 10; //Trig
const int recv_pin = 11; //Echo

const unsigned long baudRate = 115200;

const float CENTER_DISTANCE = 0.14;
float distance = 0.14;

Servo myservo;

VL53L0X sensor;

void setup() {
  Serial.begin(baudRate);
  myservo.attach(servoPin); 
  
  pinMode(trans_pin,OUTPUT); //transmit is ouput
  pinMode(recv_pin,INPUT); //receive is input

  Wire.begin();

  sensor.setTimeout(500);
  if (!sensor.init())
  {
    Serial.println("Failed to detect and initialize sensor!");
    while (1) {}
  }

  sensor.startContinuous();
}



void loop() {

  int rx = 0;
  int dist = sensor.readRangeContinuousMillimeters();
  if(Serial.available()){
    // Read and write angle to servo
    rx = Serial.read(); //Read raw byte value - Should be directly parseable as integer (0-180) ... technically uint8_t (char) but well within bounds for a regular signed int.
    if(rx >= 60 && rx <= 120) myservo.write(rx);
  
    //Calculate and send distance
    Serial.println(dist);

    if(rx == 180) Serial.println(u8"\U0001f60e");
    if(rx == 0) Serial.println(u8"\U0001F4A9");
  } 
}