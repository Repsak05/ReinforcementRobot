// #include <bits/stdc++.h>
// using namespace std;

// class Layer {
//     public:
//     	vector<Node> nodes;
// 		float bias;
// };


// class Node {
// 	float input;
// 	float output;
// };

// class Connection {
// 	public:
// 		// Node& input;
// 		// Node& output;
// 		float weight;
// };

// class AI {
// 	vector<Layer> layers;
// 	vector<vector<Connection>> connections; //[i][j] is weight from node i to node j

//   	public:
// 		AI(int hiddenLayerSize) {
// 			connections.resize(layers.size());

// 			if(layers.size() < 2) cout << "ERROR - wrong size";

// 			for(int i = 0; i < layers.size() - 1; i++){
// 				vector<Node> thisLayer = layers[i].nodes;
// 				vector<Node> nextLayer = layers[i + 1].nodes;

// 				for(int k = 0; k < thisLayer.size(); k++){
// 					for(int j = 0; j < nextLayer.size(); j++){
// 						Connection connection;
// 						connection.weight = rand() % 1;
		
// 						connections[k].push_back(connection);
// 					}
// 				}
// 			}
			
// 		}

// 		void update() {
// 			// MATH!
// 			Layer& inputLayer = layers[0];
// 			Layer& outputLayer = layers[layers.size() - 1];
		
// 			for(int i = 1; i < layers.size() - 1; i++){
// 				vector<Node>& hiddenLayer = layers[i].nodes;
// 				float& layerBias = layers[i].bias;
// 			// Hidden layers
			
// 			}
// 		}

// 	private:
// 		float activationFunction(int val){
// 			return 1/(1 + pow(2.71828, -val));
// 		}
		
// 		float getAngle(){
// 			return 90;
// 		}
// };