from neuralnet import NeuralNetwork
from Envrioment import Environment
import math
import numpy as np
import matplotlib.pyplot as plt

MIN_POSITION = 16
MAX_POSITION = 169
AMOUNT_OF_ENVIRONMENTS = 10
ANGLE_SPEED = 0.01

environments = []
neuralNetworks = []
results = []

def getDistanceToCenter(placement): #placement [0, 1]
    center = 0.5
    return abs(placement - center)

def removeNetworks(newtworks, results, amountRemove):
    for _ in range(amountRemove):
        index = np.argmax(results)
        results.pop(index)
        newtworks.pop(index)

def runAgents(steps):
    for _ in range(steps):
        for i in range(len(environments)):
            env = environments[i]
            dist = (env.gap - MIN_POSITION) / (MAX_POSITION - MIN_POSITION) 
            angle = (env.box.angle - math.pi * 5 / 6) / (2 * math.pi / 6)
            # print(dist, angle)
            action = (np.argmax(neuralNetworks[i].calcOutput(np.matrix([[angle],[dist]]))) - 1) * ANGLE_SPEED
            # print(action)
            env.run(action)
            results[i] = getDistanceToCenter(dist) #Remove max 

for i in range(AMOUNT_OF_ENVIRONMENTS):
    environments.append(Environment())
    tempN = NeuralNetwork()
    tempN.randInit(2, 3, 10, 1)
    neuralNetworks.append(tempN)
    results.append(MAX_POSITION)
    
bestResults = []
addSteps = 0
for nr in range(20):
    runAgents(100)
    # addSteps += 100
    print(f"nr: {nr}, min: {min(results)}")
    # print(environments[0].ball.position)
    # print(results)
    bestResults.append(min(results))
    removeNetworks(neuralNetworks, results, int(AMOUNT_OF_ENVIRONMENTS/2))
        
    #Create children
    startLen = len(neuralNetworks)
    for i, agent in enumerate(neuralNetworks):
        newAgent = NeuralNetwork()
        newAgent.init(agent.layers, agent.biases, 0.5, 0.5)
        neuralNetworks.append(newAgent)
        results.append(MAX_POSITION)
        if i == startLen - 1:
            break

    environments = []
    for i in range(AMOUNT_OF_ENVIRONMENTS):
        environments.append(Environment())
    # print(len(neuralNetworks))

indexBest = np.argmin(results)
# print(neuralNetworks[indexBest].layers)
for i, layer in enumerate(neuralNetworks[indexBest].layers):
    np.save(f"layers/bestLayer{i}.npy", layer)
    np.save(f"biases/bestBiases{i}.npy", neuralNetworks[indexBest].biases[i])

xbestResults = np.arange(len(bestResults))
plt.plot(xbestResults, bestResults, marker='o', linestyle='-')
plt.show()


# np.save("bestLayer.npy", neuralNetworks[indexBest].layers)
# np.save("bestBiases.npy", neuralNetworks[indexBest].biases)