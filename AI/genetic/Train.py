from neuralnet import NeuralNetwork
from Envrioment import Environment
import math
import numpy as np

MIN_POSITION = 16
MAX_POSITION = 169
AMOUNT_OF_ENVIRONMENTS = 10
ANGLE_SPEED = 0.003

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
            env.run(action)
            results[i] = getDistanceToCenter(dist) #Remove max 

for i in range(AMOUNT_OF_ENVIRONMENTS):
    environments.append(Environment())
    tempN = NeuralNetwork()
    tempN.randInit(2, 3, 20, 1)
    neuralNetworks.append(tempN)
    results.append(MAX_POSITION)
    
while True:
    runAgents(100)
    removeNetworks(neuralNetworks, results, 5)
    
    #Create children
    
# print(len(neuralNetworks))

