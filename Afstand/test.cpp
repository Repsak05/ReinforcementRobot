// #include <bits/stdc++.h>
// using namespace std;

// class QLearningAI {
// private:
//     unordered_map<string, vector<float>> QTable; // Q-values for state-action pairs
//     float learningRate = 0.1f;
//     float discountFactor = 0.9f;
//     float explorationRate = 0.2f;
//     vector<int> actions = {-1, 0, 1}; // Tilt left, stay, tilt right

//     string getStateKey(float angle, float distance) {
//         return to_string((int)angle) + "_" + to_string((int)distance);
//     }

// public:
//     QLearningAI() {}

//     int chooseAction(float angle, float distance) {
//         string stateKey = getStateKey(angle, distance);
//         if (QTable.find(stateKey) == QTable.end()) {
//             QTable[stateKey] = vector<float>(3, 0.0f); // Initialize Q-values
//         }
        
//         if ((rand() % 100) / 100.0f < explorationRate) {
//             return actions[rand() % actions.size()]; // Explore random action
//         }
        
//         return actions[max_element(QTable[stateKey].begin(), QTable[stateKey].end()) - QTable[stateKey].begin()];
//     }

//     void updateQValue(float angle, float distance, int action, float reward, float nextAngle, float nextDistance) {
//         string stateKey = getStateKey(angle, distance);
//         string nextStateKey = getStateKey(nextAngle, nextDistance);
        
//         if (QTable.find(nextStateKey) == QTable.end()) {
//             QTable[nextStateKey] = vector<float>(3, 0.0f);
//         }
        
//         int actionIndex = find(actions.begin(), actions.end(), action) - actions.begin();
//         float maxFutureQ = *max_element(QTable[nextStateKey].begin(), QTable[nextStateKey].end());
        
//         QTable[stateKey][actionIndex] += learningRate * (reward + discountFactor * maxFutureQ - QTable[stateKey][actionIndex]);
//     }
// };

// int main() {
//     srand(time(0));
//     QLearningAI ai;
    
//     // cout << "Reinforcement Learning AI for Ball Centering" << endl;
    
//     while (true) {
//         float angle, ballDistance;
//         // cout << "Enter platform angle: ";
//         cin >> angle;
//         // cout << "Enter ball distance from center: ";
//         cin >> ballDistance;
        
//         int action = ai.chooseAction(angle, ballDistance);
//         // cout << "AI Suggests Action (Tilt Left: -1, Stay: 0, Tilt Right: 1): " << action << endl;
//         cout << action << endl;
        
//         float newBallDistance;
//         // cout << "Enter new ball distance after action: ";
//         cin >> newBallDistance;
        
//         float reward = -abs(newBallDistance); // Closer to center is better
//         ai.updateQValue(angle, ballDistance, action, reward, angle + (action * 5), newBallDistance);
        
//         // cout << "Q-learning updated!" << endl;
//     }
    
//     return 0;
// }
