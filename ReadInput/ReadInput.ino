#include <Servo.h>

Servo myservo;

int angle = 90;

void setup() {
  Serial.begin(115200);
  myservo.attach(9);

}

void loop() {
  angle = readInputInt();
  Serial.println(angle);
  if (angle > 0) {
    myservo.write(angle);
    // Serial.println(angle);
  }
  // Serial.println(angle);
  angle = -1;
  //delay(100);

  // Serial.println("hej");
}

int readInputInt() {
  // String rx= "";
  int rx = -1;
  while(Serial.available() > 0 && rx == -1){
    rx = Serial.parseInt();

  }

  return rx;
  // if(rx!=""){
  //   // Serial.println(rx);
  //   return rx.toInt();
  // }
}

/*
String buff="";
if(Serial.available()){
  Serial.read()
}
*/