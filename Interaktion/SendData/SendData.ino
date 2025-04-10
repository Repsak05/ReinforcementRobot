#include <Wire.h>
#include "rgb_lcd.h"
#include <Encoder.h>
rgb_lcd lcd;


#define MUTATIONS_RATE A0   //Slider
#define MAX_SIM_TID A1      //Rotary
#define INPUT_STADIER A2    //Rotary
#define AI A3               //Rotary  
//MUTATIONSRATE             //Encoder turn
//START GAME                //Encoder click

Encoder myEnc(2, 3);
int currentEncoderPosition = 1;
const int START = 4;
int HAS_STARTED = 0;

//                  0              1              2                3                  4               5              
String types[6] = {"Iterationer", "Max Sim Tid", "Input Stadier", "Parallelle AI's", "Mutationsrate", "Start" };
int   values[6] = {50,             250,           3,               50,                90,              0};


void setup(){
  Serial.begin(115200);
  pinMode(AI, INPUT);
  pinMode(MAX_SIM_TID, INPUT);
  pinMode(INPUT_STADIER, INPUT);

  lcd.begin(16, 2);
  lcd.setRGB(0, 200, 0); //R
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

int updateEncoder(){
  int newVal = myEnc.read();
  int increment = 5;
  int MAX_VAL = 200;
  currentEncoderPosition = max(1, min(int(round(abs(newVal / 4.0) * increment)) % MAX_VAL, MAX_VAL));
  return currentEncoderPosition;
}

void loop(){
  
  int maxSimulationsTid = 1023 - analogRead(MAX_SIM_TID);
  updateValue(1, convertBetweenPositions(maxSimulationsTid, 1, 30) * 10);

  int inputStadier = 1023 - analogRead(INPUT_STADIER);
  updateValue(2, convertBetweenPositions(inputStadier, 1, 10));

  int parallelleAI = 1023 - analogRead(AI);
  updateValue(3, convertBetweenPositions(parallelleAI, 1, 20) * 10);

  int mutationsRate = 1023 - analogRead(MUTATIONS_RATE);
  updateValue(4, convertBetweenPositions(mutationsRate, 0, 50) * 2);

  // Encoder
  updateValue(0, updateEncoder());
  Serial.println(currentEncoderPosition);

  int currentState = !digitalRead(START);
  if(HAS_STARTED != currentState){
    HAS_STARTED = currentState;
    updateValue(5, HAS_STARTED); //Press encoder to start

    if(HAS_STARTED){
      lcd.setRGB(200, 0, 0); //G
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("AI IS TRANING");
      delay(3000);

      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Wait till traning");
      lcd.setCursor(0, 1);
      lcd.print("is complete");
      delay(3000);
      lcd.setRGB(0, 200, 0); //R
    }
  }

  

  delay(10);
}