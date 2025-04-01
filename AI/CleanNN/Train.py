import math
import numpy as np
import matplotlib.pyplot as plt


from NeuralNetwork import NeuralNetwork
from Environment import Environment

MAX_POSITION = 90
MIN_POSITION = 0

ANGLE_SPEED = 0.01
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


def initialize():
    global environments
    global neuralNetworks
    global results
    
    for i in range(AMOUNT_OF_ENVIRONMENTS):
        env = Environment()
        env.init(DRAW_ENV)
        environments.append(env)
        
        results.append(MAX_POSITION)
        
        network = NeuralNetwork()
        network.randInit(2, 3, 20, 1)
        neuralNetworks.append(network)
    
        
def removeNetworks(amount):
    global environments
    global neuralNetworks
    global results
    
    for _ in range(amount):
        index = np.argmax(results)
        
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
            newNet.init(agent.layers, agent.biases, 0.5, 1) #Change apropriately
            neuralNetworks.append(newNet)
            results.append(MAX_POSITION) #Initialize position
        
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

def run(steps):
    global environments
    global neuralNetworks
    global results
    
    for _ in range(steps):
        for i in range(AMOUNT_OF_ENVIRONMENTS):
            env = environments[i]
            
            # calc dist, dir, angle, newAngle etc.
            dist = realDistanceToCenter(env.ball.position[0], env.ball.position[1], CENTER_BOX[0], CENTER_BOX[1])
            angle = normalizeAngle(env.plane.angle)
            
            possibleMoves = neuralNetworks[i].calcOutput(np.matrix([[angle],[dist]]))
            dir =  np.argmax(possibleMoves) - 1
            action = dir * possibleMoves[dir + 1, 0] * ANGLE_SPEED
            
            #Insert distance
            if(i == 0): env.runDraw(action)
            else: env.run(action)
            
            results[i] = dist
    

STEPS = 20
INTERATIONS = 10

initialize()
bestResults = []

for i in range(INTERATIONS):
    run(STEPS)
    STEPS += 5
    if(i < 10): print(f"Iteration: 0{i}, score: {min(results)}")
    else: print(f"Iteration: {i}, score: {min(results)}")

    if i == INTERATIONS - 1: break
    bestResults.append(min(results))
    removeNetworks(int(AMOUNT_OF_ENVIRONMENTS / REMOVE_BOTTOM) * REMOVE_TOP)
    addNetworks(REMOVE_TOP)
    
    
    errorHandler()
    
    
#Draw score
indexBest = np.argmin(results)

xbestResults = np.arange(len(bestResults))
plt.plot(xbestResults, bestResults, marker='o', linestyle='-')
plt.show()