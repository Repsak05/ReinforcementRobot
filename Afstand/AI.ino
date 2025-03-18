// #include <Arduino.h>

// class QLearningAI {
// private:
//     struct QState {
//         float qValues[3] = {0.0, 0.0, 0.0};  // Q-values for actions {-1, 0, 1}
//     };
    
//     QState qTable[150][10];  // Limited discrete states for platform angle (-90 to 90) and ball distance (-10 to 10)
//     float learningRate = 0.1;
//     float discountFactor = 0.9;
//     float explorationRate = 0.2;
//     int actions[3] = {-1, 0, 1};  // Tilt left, stay, tilt right

// public:
//     QLearningAI() {}

//     int chooseAction(int angle, int distance) {
//         angle = constrain(angle + 90, 0, 179);  // Map -90 to 90 into 0 to 179
//         distance = constrain(distance + 10, 0, 19);  // Map -10 to 10 into 0 to 19
        
//         if (random(100) < explorationRate * 100) {
//             return actions[random(3)];  // Explore a random action
//         }

//         float* qVals = qTable[angle][distance].qValues;
//         int bestIndex = 0;
//         for (int i = 1; i < 3; i++) {
//             if (qVals[i] > qVals[bestIndex]) bestIndex = i;
//         }
//         return actions[bestIndex];  // Exploit best known action
//     }

//     void updateQValue(int angle, int distance, int action, float reward, int nextAngle, int nextDistance) {
//         angle = constrain(angle + 90, 0, 179);
//         distance = constrain(distance + 10, 0, 19);
//         nextAngle = constrain(nextAngle + 90, 0, 179);
//         nextDistance = constrain(nextDistance + 10, 0, 19);

//         int actionIndex = (action == -1) ? 0 : (action == 0) ? 1 : 2;
//         float* qVals = qTable[angle][distance].qValues;
//         float* nextQVals = qTable[nextAngle][nextDistance].qValues;

//         float maxFutureQ = max(max(nextQVals[0], nextQVals[1]), nextQVals[2]);
//         qVals[actionIndex] += learningRate * (reward + discountFactor * maxFutureQ - qVals[actionIndex]);
//     }
// };

// QLearningAI ai;
// int ballDistance = 10;

// #include <Servo.h>

// const int trans_pin = 10; //Trig
// const int recv_pin = 11; //Echo

// float distance = 0;

// Servo myservo;

// int angle = 90;

// void setup() {
//     myservo.attach(9);

//     pinMode(trans_pin,OUTPUT); //transmit is ouput
//     pinMode(recv_pin,INPUT);

//     Serial.begin(9600);
//     Serial.println("Reinforcement Learning AI for Ball Centering (Arduino)");
// }

// void loop() {
//     Serial.print("Current Angle: "); Serial.println(angle);
//     Serial.print("Current Ball Distance: "); Serial.println(ballDistance);

//     int action = ai.chooseAction(angle, ballDistance);
//     // Serial.print("AI Suggests Action (Tilt Left: -1, Stay: 0, Tilt Right: 1): ");
//     Serial.println(action);
//     angle += action*5;
//     myservo.write(angle);

//     // Serial.println("Enter new ball distance after action:");
//     // while (!Serial.available());
//     // ballDistance = Serial.parseInt();
//     ballDistance = calcDist(distance, 0.34);

//     float reward = -abs(ballDistance);
//     ai.updateQValue(angle, ballDistance, action, reward, angle + (action * 5), ballDistance);
//     angle += action * 5;

//     Serial.println("Q-learning updated!\n");
//     delay(100);  // Pause before next iteration
// }



// float calcDist(float oldDist, float maxDist) {
//   float duration; //time var

//   digitalWrite(trans_pin,LOW); // ensure no errant transmission
//   delayMicroseconds(5);

//   digitalWrite(trans_pin,HIGH); // transmit
//   delayMicroseconds(10);

//   digitalWrite(trans_pin,LOW); // stop transmission
//   duration = pulseIn(recv_pin,HIGH); // listen for pulses

//   float distRaw = duration*(340)/(2*1000000); // calculate distance
//   /*
//   d = c*delta(t)/2
//   c = 340 m/s
//   39.79 inch per meter
//   duration is in microseconds, so 1*10^6 is divided
//   */

//   if (maxDist < distRaw) {
//     return oldDist;
//   }
//   if (distRaw < 0.0) {
//     return 0.01;
//   }


//   return distRaw;
// }
