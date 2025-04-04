import math
import numpy as np
import matplotlib.pyplot as plt
import time

from NeuralNetwork import NeuralNetwork
from Environment import Environment

MAX_POSITION = 90
MIN_POSITION = 0

ANGLE_SPEED = 0.05
MIN_ANGLE = math.pi - math.pi / 18
MAX_ANGLE = math.pi + math.pi / 18

AMOUNT_OF_ENVIRONMENTS = 50 #Must be an even number 
DRAW_ENV = True

REMOVE_TOP = 9       #Fraction of how many is being removed REMOVE_TOP / REMOVE_BOTTOM
REMOVE_BOTTOM = 10   # e.g. 9 / 10, then 9/10th's is being removed

CENTER_BOX = [400, 450]

environments = []
neuralNetworks = []
results = []

def normalize(val, min, max):
    return (val - min) / (max - min)

def normalizeDist(value):
    return (value - MIN_POSITION) / (MAX_POSITION - MIN_POSITION)

def normalizeAngle(angle):
    return (angle - MIN_ANGLE) / (MAX_ANGLE - MIN_POSITION)

def realDistanceToCenter(ballX, ballY, floorX, floorY):
    distance = math.sqrt(pow((ballX - floorX), 2) + pow((ballY - floorY), 2))
    nDist = normalizeDist(distance)
    
    if(nDist < 0 or nDist > 1): print("INVALID: ", nDist, " must be within bounds [0, 1]")
    return nDist

# def distToCenterFromPos(sideDist, max, min):
#     center = (max-min) / 2



def initialize():
    global environments
    global neuralNetworks
    global results
    
    for i in range(AMOUNT_OF_ENVIRONMENTS):
        env = Environment()
        env.init(DRAW_ENV)
        environments.append(env)
        
        # results.append(MAX_POSITION)
        results.append([])
        
        network = NeuralNetwork()
        network.randInit(6, 3, 20, 1)
        neuralNetworks.append(network)
    
        
def removeNetworks(amount):
    global environments
    global neuralNetworks
    global results

    meanRes = []
    for res in results:
        meanRes.append(np.mean(res))
    
    for _ in range(amount):
        index = np.argmax(meanRes)
        
        meanRes.pop(index)
        results.pop(index)
        environments.pop(index)
        neuralNetworks.pop(index)
      
        
def addNetworks(amount):
    global environments
    global neuralNetworks
    global results
    
    startLen = len(neuralNetworks)
    
    for i, agent in enumerate(neuralNetworks):
        for j in range(amount):
            newNet = NeuralNetwork()
            newNet.init(agent.layers, agent.biases, 0.1, 1) #Change apropriately
            neuralNetworks.append(newNet)
            # results.append(MAX_POSITION) #Initialize position
            results.append([])
        
        if i == startLen - 1:
            break
        
    # Reset environments
    environments = []
    for i in range(len(neuralNetworks)):
        env = Environment()
        env.init(DRAW_ENV)
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

            env.steps[4][0] = env.steps[2][0]
            env.steps[5][0] = env.steps[3][0]

            env.steps[2][0] = env.steps[0][0]
            env.steps[3][0] = env.steps[1][0]
            
            # calc dist, dir, angle, newAngle etc.
            # dist = realDistanceToCenter(env.ball.position[0], env.ball.position[1], CENTER_BOX[0], CENTER_BOX[1])
            dist = env.realDistFromSide()
            angle = normalizeAngle(env.plane.angle)

            env.steps[0][0] = angle
            env.steps[1][0] = dist
            
            # possibleMoves = neuralNetworks[i].calcOutput(np.matrix([[angle],[dist]]))
            possibleMoves = neuralNetworks[i].calcOutput(env.steps)

            

            dir =  np.argmax(possibleMoves) - 1
            action = dir * possibleMoves[dir + 1, 0] * ANGLE_SPEED
            
            #Insert distance
            if(i == 0 and DRAW_ENV and totalIterations == thisIteration): 
                if (TimeCheck): 
                    print("Time:",time.time() - startTime)
                    TimeCheck = False
                env.runDraw(action) #Draw 

            # if(): env.runDraw(action)
            else: env.run(action)
            # env.runDraw(action)
            # results[i].append(dist)
            results[i].append(abs(0.5 - dist))
    

STEPS = 30
INTERATIONS = 50
TimeCheck = True

initialize()
bestResults = []

startTime = time.time()

for i in range(INTERATIONS):
    run(STEPS, INTERATIONS, i + 1)
    STEPS += 4
    
    # Calc best result
    # print(results)
    meanRes = []
    for res in results:
        meanRes.append(np.mean(res))
        
    # Print res
    if(i < 10): print(f"Iteration: 0{i}, score: {min(meanRes)}")
    else: print(f"Iteration: {i}, score: {min(meanRes)}")

    if i == INTERATIONS - 1: break
    bestResults.append(min(meanRes))
    removeNetworks(int(AMOUNT_OF_ENVIRONMENTS / REMOVE_BOTTOM) * REMOVE_TOP)
    addNetworks(REMOVE_TOP)
    
    
    errorHandler()
    
for env in environments:
    env.stop()

#Draw score
# indexBest = np.argmin(meanRes)

xbestResults = np.arange(len(bestResults))
plt.plot(xbestResults, bestResults, marker='o', linestyle='-')
plt.show()