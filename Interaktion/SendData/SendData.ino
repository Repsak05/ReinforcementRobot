#include <Wire.h>
#include "rgb_lcd.h"
// #include <Encoder.h>
rgb_lcd lcd;


// Encoder knobRight(2, 3);
// int positionRight = 0;

#define PREVIOUS_POSITIONS A0  
#define AMOUNT_OF_LAYERS A1  
#define STEPS A2 


String types[7] = {"hiddenLayers", "neuronsInHiddenLayer", "previousStates", "steps", "angleSpeed", "antalIterationer", "malPlacering"};
int   values[7] = {1,               20,                     3,                5,       5,            50,                 50};

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

  return MIN + (abs(current / (start - end)) * (MAX - MIN));
}

// bool valueChanged(){

// }

void sendValue(String type, int value){
  Serial.print(type + " ");
  Serial.println(value);
}

void updateValue(int index, int value){
  if(value != values[index]){
    values[index] = value;
    sendValue(types[index], values[index]);
    writeOnLCD(types[index], values[index], 0, 0);
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


  int amountOfLayers = analogRead(AMOUNT_OF_LAYERS);
  updateValue(0, convertBetweenPositions(amountOfLayers, 1, 5));
  
  int previousPositions = analogRead(PREVIOUS_POSITIONS);
  updateValue(2, convertBetweenPositions(previousPositions, 1, 100));

  int steps = analogRead(STEPS);
  updateValue(3, convertBetweenPositions(steps, 10, 300));

  //Following slider doesn't work properly :(
  // int iterations = analogRead(A3);
  // updateValue(5, iterations);
  



  delay(100);
}