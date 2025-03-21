#include <Servo.h>

const int servoPin = 9;

const unsigned long baudRate = 115200;

Servo myservo;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(baudRate);
  myservo.attach(servoPin);

}

void loop() {
  // put your main code here, to run repeatedly:

    int rx = 0;
    rx = Serial.parseInt(); //Read raw byte value - Should be directly parseable as integer (0-180) ... technically uint8_t (char) but well within bounds for a regular signed int.
    if(Serial.available() && rx > 0){
      Serial.println(rx);
    // Read and write angle to servo
      myservo.write(rx);
  } 
}
