import numpy as np
import math
import copy

class NeuralNetwork:
    def randInit(self, inputSize, outputSize, hiddenLayerSize, amountHidLayers):
        self.layers = [np.random.uniform(-0.5, 0.5, (hiddenLayerSize, inputSize))]
        self.biases = [np.zeros((hiddenLayerSize,1))]
        for i in range(amountHidLayers):
            self.layers.append(np.random.uniform(-0.5, 0.5, (hiddenLayerSize,hiddenLayerSize)))
            self.biases.append(np.zeros((hiddenLayerSize,1)))
        self.biases.append(np.zeros((outputSize,1)))
        self.layers.append(np.random.uniform(-0.5, 0.5, (outputSize, hiddenLayerSize)))

    def init(self, layers, biases, randThreshold, randChange):
        self.layers = copy.deepcopy(layers)
        self.biases = copy.deepcopy(biases)
        for iLayer in range(len(layers)):
            layer = self.layers[iLayer]
            
            for ix in range(len(layer)):
                x = layer[ix]
                
                for iweight in range(len(x)):
                    weight = x[iweight]     
                         
                    if(np.random.uniform(0, 1) < randThreshold):
                        n = np.random.uniform(1 - randChange, 1 + randChange)
                        
                        self.layers[iLayer][ix][iweight] = weight * n

    def calcOutput(self, input):
        curValues = input

        for i, layer in enumerate(self.layers):
            preValues = self.biases[i] + layer @ curValues
            curValues = 1 / (1 + np.exp(-preValues))
        return curValues
        
# inputSize = 785
# test = NeuralNetwork()
# test.randInit(inputSize, 10, 20, 1)
# print(np.argmax(test.calcOutput(np.random.uniform(0, 1, (inputSize, 1)))))
# print(np.argmax(test.calcOutput(np.random.uniform(0, 1, (inputSize, 1)))))
# print(np.argmax(test.calcOutput(np.random.uniform(0, 1, (inputSize, 1)))))
# print(np.argmax(test.calcOutput(np.random.uniform(0, 1, (inputSize, 1)))))

# print(test.calcOutput(np.matrix([[0.8],[0.8]])))

# test = NeuralNetwork()
# test.randInit(784, 10, 20, 1)

# print(np.argmax(test.calcOutput(np.random.uniform(0, 1, (784, 1)))))
# print(np.argmax(test.calcOutput(np.random.uniform(0, 1, (784, 1)))))
# print(np.argmax(test.calcOutput(np.random.uniform(0, 1, (784, 1)))))
# print(np.argmax(test.calcOutput(np.random.uniform(0, 1, (784, 1)))))

# new = NeuralNetwork()
# new.init(test.layers, test.biases, 0.5, 0.5)

# print(test.layers[1][0])
# print(new.layers[1][0])

# print(test.biases)

# print(np.matrix([[30],[120]]).shape)
# print(np.zeros((2,1)).shape)


# print(np.argmax(test.calcOutput(np.matrix([[30/(2*math.pi)],[120/170]]))) - 1)



# print(test.calcOutput(np.zeros((2,1))))


# wih = np.random.uniform(-0.5, 0.5, (20,2))
# whh = np.random.uniform(-0.5, 0.5, (20,20))
# who = np.random.uniform(-0.5, 0.5, (3,20))

# bih = np.zeros((20,1))
# bhh = np.zeros((20,1))
# bho = np.zeros((3,1))

# learnRate = 0.01

# inp = np.zeros((2,1))

# while True:
#     curAngle = float(input("Angle: "))
#     curDist = float(input("Dist: "))
#     inp[0][0] = curAngle/180
#     inp[1][0] = (curDist-40)/(240-40)

#     hPre = bih + wih @ inp
#     h = 1/ (1 + np.exp(-hPre))

#     # print("bhh:",bhh)
#     # print("h:",h)
#     hhPre = bhh + whh @ h
#     hh = 1 / (1 + np.exp(-hhPre))

#     oPre = bho + who @ hh
#     output = 1 / (1 + np.exp(-oPre))
#     print(output)


        

