#include <Wire.h>
#include "rgb_lcd.h"
#include <Encoder.h>

rgb_lcd lcd;

const int MIN_POSITION = 40;
const int MAX_POSITION = 240;

Encoder knobRight(2, 3);
long positionRight = 0;


#define ROTARY_ANGLE_SENSOR A1  

int convertBetweenPositions(int current, int MIN, int MAX){
  // if(MAX_POSITION > MIN_POSITION) swap(MIN_POSITION, MAX_POSITION);

  float start = 0;
  float end = 1023;
  return MIN + (abs(current / (start - end)) * (MAX - MIN));
}

void setup() {
  Serial.begin(115200);
  pinMode(ROTARY_ANGLE_SENSOR, INPUT);

  lcd.begin(16, 2);
  lcd.setRGB(200, 0, 0); //RGB colors for the background
}

void writeOnLCD(String s, int val, int col, int row){
  lcd.setCursor(col, row);
  lcd.print(s);
  lcd.setCursor(col + s.length() + 2, row);
  lcd.print(val);
}

int getEncoderPosition(){
  long newRight;
  newRight = knobRight.read();
  if (newRight != positionRight) {
    Serial.println();
    positionRight = newRight;
  }
  return int(newRight / 4);
}

void loop(){
  Serial.println(getEncoderPosition(););

  lcd.clear();

  // Sliding sensor
  int sensorValue = analogRead(A0);

  //Encoder
  int encoderValue = analogRead(ROTARY_ANGLE_SENSOR);
 
  // LCD
  writeOnLCD("Episoder", convertBetweenPositions(encoderValue, 0, 300), 0, 0);
  writeOnLCD("Placering", convertBetweenPositions(sensorValue, MIN_POSITION, MAX_POSITION), 0, 1);

  delay(100);

}