from neuralnet import NeuralNetwork
from Envrioment import Environment
import math
import numpy as np
import matplotlib.pyplot as plt

MIN_POSITION = 0 # 16
MAX_POSITION = 80 # 169
AMOUNT_OF_ENVIRONMENTS = 50
ANGLE_SPEED = 0.01

environments = []
neuralNetworks = []
results = []

def realDistanceToCenter(ballX, ballY, floorX, floorY):
    distance = math.sqrt(pow((ballX - floorX), 2) + pow((ballY - floorY), 2))
    # distance = math.sqrt(pow(ballX - floorX, 2))
    #Normalize distance
    normalDist = (distance - MIN_POSITION) / (MAX_POSITION - MIN_POSITION) 
    # print(ballX)
    # print(normalDist, " [0, 1]")
    return normalDist
    

def getDistanceToCenter(placement): #placement [0, 1]
    placement = max(0, placement)
    placement = min(1, placement)
    center = 0.5
    return abs(placement - center)

def removeNetworks(newtworks, results, amountRemove):
    # print(results)
    for _ in range(amountRemove):
        index = np.argmax(results)
        # print(results[index])
        results.pop(index)
        newtworks.pop(index)
        
def addNetwork(networks, amount):
    global results
    global environments
    
    startLen = len(networks)
    
    for i, agent in enumerate(networks):
        for j in range(amount):
            newNet = NeuralNetwork()
            newNet.init(agent.layers, agent.biases, 0.9, 1)
            neuralNetworks.append(newNet)
            results.append(MAX_POSITION) #Initialize position
        
        if i == startLen - 1:
            break

    environments = []
    # results = []
    for i in range(len(neuralNetworks)):
        environments.append(Environment())
    #     results.append(MAX_POSITION)

    # for i in range(amount * startLen):
        # environments.append(Environment())
        # results.append(MAX_POSITION)
        
        
    

def runAgents(steps):
    for _ in range(steps):
        # print(len(neuralNetworks), "should be: ", len(environments) )
        for i in range(len(environments)):
            env = environments[i]
            # dist = (env.gap - MIN_POSITION) / (MAX_POSITION - MIN_POSITION) 
            dist = realDistanceToCenter(env.ball.position[0], env.ball.position[1], 400, 450)
            angle = (env.box.angle - ((math.pi) - (math.pi / 18))) / (((math.pi) + (math.pi / 18)) - ((math.pi) - (math.pi / 18)))
            # print(dist, angle)
            retning = np.argmax(neuralNetworks[i].calcOutput(np.matrix([[angle],[dist]]))) - 1
            action = retning * neuralNetworks[i].calcOutput(np.matrix([[angle],[dist]]))[retning + 1, 0] * ANGLE_SPEED
            # print("Should be a value:", neuralNetworks[i].calcOutput(np.matrix([[angle],[dist]]))[retning + 1, 0])
            # print(retning, action[0][0])
            # print(action)
            env.run(action)
            # results[i] = getDistanceToCenter(dist) #Remove max 
            # print(env.ball.position[0], env.ball.position[1])
            results[i] = realDistanceToCenter(env.ball.position[0], env.ball.position[1], 400, 450)

for i in range(AMOUNT_OF_ENVIRONMENTS):
    environments.append(Environment())
    tempN = NeuralNetwork()
    tempN.randInit(2, 3, 50, 1)
    neuralNetworks.append(tempN)
    results.append(MAX_POSITION)
    
bestResults = []
addSteps = 0

INTERATIONS = 50
for nr in range(INTERATIONS):
    runAgents(30 + addSteps)
    addSteps += 0
    index = np.argmin(results)
    print(f"nr: {nr}, min: {min(results)},   index: {index}, value: {results[index]}")
    # print(environments[0].ball.position)
    # print(results)
    if nr == INTERATIONS - 1: break
    bestResults.append(min(results))
    removeNetworks(neuralNetworks, results, int(len(neuralNetworks)/10) * 9)
    addNetwork(neuralNetworks, 9)
        
    #Create children
    
    # startLen = len(neuralNetworks)
    # for i, agent in enumerate(neuralNetworks):
    #     newAgent = NeuralNetwork()
    #     newAgent.init(agent.layers, agent.biases, 0.9, 1)
    #     neuralNetworks.append(newAgent)
    #     results.append(MAX_POSITION) #Initialize position
    #     if i == startLen - 1:
    #         break

    # environments = []
    # for i in range(AMOUNT_OF_ENVIRONMENTS):
    #     environments.append(Environment())
    
    
    # print(len(neuralNetworks))
    
indexBest = np.argmin(results)

# print(neuralNetworks[indexBest].layers)
print("Ending pos: ", environments[indexBest].ball.position)
for i, layer in enumerate(neuralNetworks[indexBest].layers):
    np.save(f"layers/bestLayer{i}.npy", layer)
    np.save(f"biases/bestBiases{i}.npy", neuralNetworks[indexBest].biases[i])


xbestResults = np.arange(len(bestResults))
plt.plot(xbestResults, bestResults, marker='o', linestyle='-')
plt.show()


# np.save("bestLayer.npy", neuralNetworks[indexBest].layers)
# np.save("bestBiases.npy", neuralNetworks[indexBest].biases)