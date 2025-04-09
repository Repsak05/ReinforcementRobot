#include <Wire.h>
#include "rgb_lcd.h"
#include <Encoder.h>
rgb_lcd lcd;


Encoder myEnc(2, 3);
int encoderPos = 1;
int oldEncoderPos = -1;

#define AMOUNT_OF_LAYERS A1  
#define STEPS A3 
#define PREVIOUS_POSITIONS A3  

//                  0               1                       2                 3       4              5                   6               7
String types[8] = {"hiddenLayers", "neuronsInHiddenLayer", "previousStates", "steps", "angleSpeed", "antalIterationer", "malPlacering", "start"};
int   values[8] = {1,               20,                     3,                200,     5,            50,                 50,             0};

void setup(){
  Serial.begin(9600);
  pinMode(PREVIOUS_POSITIONS, INPUT);
  pinMode(AMOUNT_OF_LAYERS, INPUT);
  pinMode(STEPS, INPUT);

  lcd.begin(16, 2);
  lcd.setRGB(200, 0, 0); //R
}

void writeOnLCD(String s, int val, int col, int row){
  lcd.clear();
  lcd.setCursor(col, row);
  lcd.print(s);
  lcd.setCursor(0, row + 1);
  lcd.print(val);
}

int convertBetweenPositions(int current, int MIN, int MAX){
  float start = 0;
  float end = 1023;

  return MIN + round(abs(current / (start - end)) * (MAX - MIN));
}

void sendValue(String type, int value){
  Serial.print(type + ": ");
  Serial.println(value);
}

void updateValue(int index, int value){
  if(value != values[index]){
    values[index] = value;
    sendValue(types[index], values[index]);
    writeOnLCD(types[index], values[index], 0, 0);
  }
}

void updateEncoder(){
    encoderPos = myEnc.read();

    if (encoderPos != oldEncoderPos) {
      oldEncoderPos = encoderPos;
      Serial.println(encoderPos);
    }
}

// int getEncoderPosition(){
//   int newRight;
//   newRight = knobRight.read();
//   if (newRight != positionRight) {
//     Serial.println();
//     sendValue("antalIterationer", positionRight);
//     positionRight = newRight;
//   }
//   return int(newRight / 4);
// }


int example = 1;


void loop(){
  // sendValue(types[example], values[example]);
  // getEncoderPosition();'
  // updateEncoder();
  updateValue(7, !digitalRead(4));


  int amountOfLayers = analogRead(AMOUNT_OF_LAYERS);
  updateValue(0, convertBetweenPositions(amountOfLayers, 1, 5));
  
  // int previousPositions = analogRead(PREVIOUS_POSITIONS);
  // updateValue(2, convertBetweenPositions(previousPositions, 1, 10));

  int steps = analogRead(STEPS);
  updateValue(3, convertBetweenPositions(steps, 1, 30) * 10);

  //Following slider doesn't work properly :(
  int iterations = analogRead(A0);
  updateValue(5, convertBetweenPositions(iterations, 1, 30) * 10);


  

  delay(10);
}