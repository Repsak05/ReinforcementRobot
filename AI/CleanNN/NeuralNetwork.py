import numpy as np
import math
import copy

class NeuralNetwork:
    def randInit(self, inputSize, outputSize, hiddenLayerSize, amountHidLayers):
        self.layers = [np.random.uniform(-0.5, 0.5, (hiddenLayerSize, inputSize))]
        self.biases = [np.zeros((hiddenLayerSize, 1))]
        
        for i in range(amountHidLayers):
            self.layers.append(np.random.uniform(-0.5, 0.5, (hiddenLayerSize,hiddenLayerSize)))
            self.biases.append(np.zeros((hiddenLayerSize,1)))
            
        self.biases.append(np.zeros((outputSize,1)))
        self.layers.append(np.random.uniform(-0.5, 0.5, (outputSize, hiddenLayerSize)))

    def init(self, layers, biases, randThreshold, randChange):
        self.layers = copy.deepcopy(layers)
        self.biases = copy.deepcopy(biases)
        
        for arr in self.biases:
            for bias in arr:
                n = np.random.uniform(-randChange, randChange)
                bias[0] = n
                
        for iLayer in range(len(layers)):
            layer = self.layers[iLayer]
            
            for ix in range(len(layer)):
                x = layer[ix]
                
                for iweight in range(len(x)):
                    weight = x[iweight]     
                         
                    if(np.random.uniform(0, 1) < randThreshold):
                        # print("hej")
                        n = np.random.uniform(-randChange, randChange)
                        self.layers[iLayer][ix][iweight] = n


    def calcOutput(self, input):
        curValues = input

        for i, layer in enumerate(self.layers):
            preValues = self.biases[i] + layer @ curValues
            curValues = 1 / (1 + np.exp(-preValues))
        return curValues