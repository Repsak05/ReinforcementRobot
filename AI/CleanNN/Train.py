import math
import numpy as np
import matplotlib.pyplot as plt
import time
import sys

from NeuralNetwork import NeuralNetwork
from Environment import Environment







AMOUNT_OF_ENVIRONMENTS = 50 # Antal AI's der kører på samme tid (Skal gå op i 10)

INTERATIONS = 100          # Antal omgange der skal laves nye generationer

MIN_STEPS = 30              # Antal setps i begyndelsen
MAX_STEPS = 250            # Maks antal steps der kan køres
INC_STEPS = 4               # Hvor mange steps der tilføjes per iteration

ANGLE_SPEED = 0.05          # Hvor hurtigt AI'en kan rotere

AMOUNT_HIDDEN_LAYERS = 1

NEURONS_HIDDENLAYER = 20

MAL_PLACERING = 0.5

PREVIOUS_STATES = 6




INTERATIONS = 100
MAX_STEPS = 250
PREVIOUS_STATES = 3
AMOUNT_OF_ENVIRONMENTS = 50
MUTATION_RATE = 0.9





MIN_ANGLE = math.pi - math.pi / 18
MAX_ANGLE = math.pi + math.pi / 18

MAX_POSITION = 90
MIN_POSITION = 0

DRAW_ENV = False

REMOVE_TOP = 9       #Fraction of how many is being removed REMOVE_TOP / REMOVE_BOTTOM
REMOVE_BOTTOM = 10   # e.g. 9 / 10, then 9/10th's is being removed

CENTER_BOX = [400, 450]
TimeCheck = True

environments = []
neuralNetworks = []
results = []
preStates = []

previousStates = [] #2D
PREVIOUS_STATES = 3

def normalize(val, min, max):
    return (val - min) / (max - min)

def normalizeDist(value):
    return (value - MIN_POSITION) / (MAX_POSITION - MIN_POSITION)

def normalizeAngle(angle):
    return (angle - MIN_ANGLE) / (MAX_ANGLE - MIN_ANGLE)  # -MIN_POSITION ??????????

def realDistanceToCenter(ballX, ballY, floorX, floorY):
    distance = math.sqrt(pow((ballX - floorX), 2) + pow((ballY - floorY), 2))
    nDist = normalizeDist(distance)
    
    # if(nDist < 0 or nDist > 1): print("INVALID: ", nDist, " must be within bounds [0, 1]")
    return max(min(1, nDist), 0)


def initialize():
    global environments, neuralNetworks, results, previousStates
    
    for i in range(AMOUNT_OF_ENVIRONMENTS):
        env = Environment()
        env.init(DRAW_ENV, PREVIOUS_STATES)
        environments.append(env)
        
        # results.append(MAX_POSITION)
        previousStates.append([])
        results.append([])
        
        network = NeuralNetwork()
        network.randInit(PREVIOUS_STATES * 2, 3, NEURONS_HIDDENLAYER, AMOUNT_HIDDEN_LAYERS)
        neuralNetworks.append(network)
    
    for j, layer in enumerate(neuralNetworks[0].layers):
        np.save(f"AIParams/Layers/Layer{j}", layer)
    for j, bias in enumerate(neuralNetworks[0].biases):
        np.save(f"AIParams/Biases/Bias{j}", bias)
        
def removeNetworks(amount):
    global environments, neuralNetworks, results, previousStates

    meanRes = []
    for res in results:
        meanRes.append(np.mean(res))
    
    for _ in range(amount):
        index = np.argmax(meanRes)
        
        meanRes.pop(index)
        results.pop(index)
        environments.pop(index)
        neuralNetworks.pop(index)
        previousStates.pop(index)
      
        
def addNetworks(amount, changeThresHold = 0.9, randChange = 1):
    global environments, neuralNetworks, results, previousStates
    
    startLen = len(neuralNetworks)
    
    for i, agent in enumerate(neuralNetworks):
        for j in range(amount):
            newNet = NeuralNetwork()
            newNet.init(agent.layers, agent.biases, MUTATION_RATE, 0.9, 1) #Change apropriately
            neuralNetworks.append(newNet)
            # results.append(MAX_POSITION) #Initialize position
            results.append([])
            previousStates.append([])
        
        if i == startLen - 1:
            break
        
    # Reset environments
    environments = []
    for i in range(len(neuralNetworks)):
        env = Environment()
        env.init(DRAW_ENV, PREVIOUS_STATES)
        environments.append(env)



def errorHandler(): #Print any errors which made cause an the program to malfunction
    if AMOUNT_OF_ENVIRONMENTS % 2 != 0:             print("ISSUE: AMOUNT_OF_ENVIRONMENTS must be even. It's currently ", AMOUNT_OF_ENVIRONMENTS)
    if AMOUNT_OF_ENVIRONMENTS % REMOVE_BOTTOM != 0: print("ISSUE: AMOUNT_OF_ENVIRONMENTS must be divisible by ", REMOVE_BOTTOM)
    
    # if (AMOUNT_OF_ENVIRONMENTS - int(AMOUNT_OF_ENVIRONMENTS / REMOVE_BOTTOM) * REMOVE_TOP) * REMOVE_TOP != AMOUNT_OF_ENVIRONMENTS: print("ISSUE")
    if REMOVE_TOP >= REMOVE_BOTTOM: print(f"REMOVE_TOP {REMOVE_TOP} must be smaller than REMOVE_BOTTOM {REMOVE_BOTTOM}")

def run(steps, totalIterations = 0, thisIteration = 0):
    global environments
    global neuralNetworks
    global results
    global TimeCheck

    for _ in range(steps):
        for i in range(AMOUNT_OF_ENVIRONMENTS):
            env = environments[i]
            
            # calc dist, dir, angle, newAngle etc.
            # dist = realDistanceToCenter(env.ball.position[0], env.ball.position[1], CENTER_BOX[0], CENTER_BOX[1])
            dist = env.realDistFromSide()
            angle = normalizeAngle(env.plane.angle)

            env.steps = np.append(env.steps, [[angle],[dist]], axis=0)
            env.steps = env.steps[2:]
            # print(env.steps)
            
            # possibleMoves = neuralNetworks[i].calcOutput(np.matrix([[angle],[dist]]))
            possibleMoves = neuralNetworks[i].calcOutput(env.steps)

            dir =  np.argmax(possibleMoves) - 1
            action = dir * possibleMoves[dir + 1, 0] * ANGLE_SPEED
            
            #Insert distance
            # if(i == 0 and DRAW_ENV and totalIterations == thisIteration): 
            #     if (TimeCheck): 
            #         print("Time:",time.time() - startTime)
            #         TimeCheck = False
            #     env.runDraw(action) #Draw 

            # if(DRAW_ENV): env.runDraw(action)
            # else: env.run(action)
            # env.runDraw(action)
            env.run(action)

            # if dist > 0.8: results[i].append(1)
            # else: results[i].append(dist)
            results[i].append(abs(MAL_PLACERING - dist)*2)
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Please provide 2 arguments. Not {len(sys.argv)} arguments")
        sys.exit(1)

    values = np.fromstring(sys.argv[1], dtype=int, sep=',')

    INTERATIONS = values[0]
    MAX_STEPS = values[1]
    PREVIOUS_STATES = values[2]
    AMOUNT_OF_ENVIRONMENTS = values[3]
    MUTATION_RATE = values[4]/100

    



initialize()
bestResults = []
allSteps = []

for j, layer in enumerate(neuralNetworks[0].layers):
    np.save(f"AIParams/Layers/Layer{j}", layer)
for j, bias in enumerate(neuralNetworks[0].biases):
    np.save(f"AIParams/Biases/Bias{j}", bias)

startTime = time.time()
itersPerSave = 10

global curBestNet

for i in range(INTERATIONS):
    run(MIN_STEPS, INTERATIONS, i + 1)
    
    if MIN_STEPS < MAX_STEPS: MIN_STEPS += INC_STEPS
    
    # Calc best result
    meanRes = []
    for res in results:
        meanRes.append(np.mean(res))

    bestIndex = np.argmin(meanRes)
    curBestNet = neuralNetworks[bestIndex]

    if i == itersPerSave:
        itersPerSave += 10
        # print("New Network Run")
        for j, layer in enumerate(curBestNet.layers):
            np.save(f"AIParams/Layers/Layer{j}", layer)
        for j, bias in enumerate(curBestNet.biases):
            np.save(f"AIParams/Biases/Bias{j}", bias)

        
    # Print res
    if(i < 10): print(f"Iteration: 0{i}, score: {min(meanRes)}")
    else: print(f"Iteration: {i}, score: {min(meanRes)}")

    if i == INTERATIONS - 1: break
    allSteps.append(STEPS * 0.001) #amount of steps / 1000
    bestResults.append(round(min(meanRes), 4))
    
    removeNetworks(int(AMOUNT_OF_ENVIRONMENTS / REMOVE_BOTTOM) * REMOVE_TOP)
    addNetworks(REMOVE_TOP, 0.9, 1)
    
    
    errorHandler()
    
for env in environments:
    env.stop()

#Draw score
# indexBest = np.argmin(meanRes)

for i, layer in enumerate(curBestNet.layers):
    np.save(f"AIParams/Layers/Layer{i}", layer)
for i, bias in enumerate(curBestNet.biases):
    np.save(f"AIParams/Biases/Bias{i}", bias)

print("\n\nSAVED SAVED SAVED\n\n")
# print(curBestNet.biases)

# xbestResults = np.arange(len(bestResults))
# plt.plot(xbestResults, bestResults, marker='o', linestyle='-')
# plt.show()

