#include <Wire.h>
#include "rgb_lcd.h"
rgb_lcd lcd;

const int MIN_POSITION = 40;
const int MAX_POSITION = 240;

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

void loop(){
  lcd.clear();

  // Sliding sensor
  int sensorValue = analogRead(A0);
  // Serial.print("Sensor: ");
  // Serial.println(convertBetweenPositions(sensorValue, MIN_POSITION, MAX_POSITION));


  //Encoder
  int encoderValue = analogRead(ROTARY_ANGLE_SENSOR);
  // // Serial.print("Encoder: ");
  // // Serial.println(convertBetweenPositions(encoderValue, 0, 300));
 
 
  // LCD
  writeOnLCD("Episoder", convertBetweenPositions(encoderValue, 0, 300), 0, 0);
  writeOnLCD("Placering", convertBetweenPositions(sensorValue, MIN_POSITION, MAX_POSITION), 0, 1);
  // lcd.print("Episoder:" + convertBetweenPositions(encoderValue, 0, 300));

  delay(100);

}