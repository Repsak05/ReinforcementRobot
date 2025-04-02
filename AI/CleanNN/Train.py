import math
import numpy as np
import matplotlib.pyplot as plt


from NeuralNetwork import NeuralNetwork
from Environment import Environment

MAX_POSITION = 80 # 90
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

previousStates = [] #2D
PREVIOUS_STATES = 3

def normalize(val, min, max):
    return (val - min) / (max - min)

def normalizeDist(value):
    return (value - MIN_POSITION) / (MAX_POSITION - MIN_POSITION)

def normalizeAngle(angle):
    return (angle - MIN_ANGLE) / (MAX_ANGLE - MIN_POSITION)

def realDistanceToCenter(ballX, ballY, floorX, floorY):
    distance = math.sqrt(pow((ballX - floorX), 2) + pow((ballY - floorY), 2))
    nDist = normalizeDist(distance)
    
    # if(nDist < 0 or nDist > 1): print("INVALID: ", nDist, " must be within bounds [0, 1]")
    return max(min(1, nDist), 0)


def initialize():
    global environments, neuralNetworks, results, previousStates
    
    for i in range(AMOUNT_OF_ENVIRONMENTS):
        env = Environment()
        env.init(DRAW_ENV)
        environments.append(env)
        
        # results.append(MAX_POSITION)
        previousStates.append([])
        results.append([])
        
        network = NeuralNetwork()
        network.randInit(2 * PREVIOUS_STATES, 3, 20, 2)
        neuralNetworks.append(network)
    
        
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
            newNet.init(agent.layers, agent.biases, changeThresHold, randChange) #Change apropriately
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
        env.init(DRAW_ENV)
        environments.append(env)



def errorHandler(): #Print any errors which made cause an the program to malfunction
    if AMOUNT_OF_ENVIRONMENTS % 2 != 0:             print("ISSUE: AMOUNT_OF_ENVIRONMENTS must be even. It's currently ", AMOUNT_OF_ENVIRONMENTS)
    if AMOUNT_OF_ENVIRONMENTS % REMOVE_BOTTOM != 0: print("ISSUE: AMOUNT_OF_ENVIRONMENTS must be divisible by ", REMOVE_BOTTOM)
    
    # if (AMOUNT_OF_ENVIRONMENTS - int(AMOUNT_OF_ENVIRONMENTS / REMOVE_BOTTOM) * REMOVE_TOP) * REMOVE_TOP != AMOUNT_OF_ENVIRONMENTS: print("ISSUE")
    if REMOVE_TOP >= REMOVE_BOTTOM: print(f"REMOVE_TOP {REMOVE_TOP} must be smaller than REMOVE_BOTTOM {REMOVE_BOTTOM}")

def run(steps, totalIterations = 0, thisIteration = 0):
    global environments, neuralNetworks, results, previousStates
    
    for _ in range(steps):
        for i in range(AMOUNT_OF_ENVIRONMENTS):
            env = environments[i]
            
            #Get current
            dist = realDistanceToCenter(env.ball.position[0], env.ball.position[1], CENTER_BOX[0], CENTER_BOX[1])
            angle = normalizeAngle(env.plane.angle)
            
            currentState = [[angle], [dist]]
            previousStates[i].append(currentState)
            
            # Correct previousStates
            if len(previousStates[i]) < PREVIOUS_STATES:
                amount = PREVIOUS_STATES - len(previousStates[i])
                rightsize = [currentState] * amount + previousStates[i]
            else:
                rightsize = previousStates[i][-PREVIOUS_STATES:]

            # Keep only the most recent PREVIOUS_STATES
            if len(rightsize) > PREVIOUS_STATES:
                rightsize = rightsize[-PREVIOUS_STATES:]
                previousStates[i] = rightsize 
                
            #Convert to (2 * PREVIOUS_STATES, 1)
            input_vector = np.vstack(rightsize)
            
            if len(input_vector) != 2 * PREVIOUS_STATES: print(f"ISSUE len(input_vector) {len(input_vector)} SHOULD BE 2 * PREVIOUS_STATES {2 * PREVIOUS_STATES} ")
            
            # possibleMoves = neuralNetworks[i].calcOutput(np.matrix([[angle],[dist]]))
            possibleMoves = neuralNetworks[i].calcOutput(input_vector)
            dir =  np.argmax(possibleMoves) - 1
            action = dir * possibleMoves[dir + 1, 0] * ANGLE_SPEED
            
            #Insert distance
            if(i == 0 and DRAW_ENV and totalIterations == thisIteration): env.runDraw(action) #Draw 
            # if(): env.runDraw(action)
            else: env.run(action)
            
            results[i].append(dist)
    

STEPS = 5
INTERATIONS = 100

initialize()
bestResults = []
allSteps = []

for i in range(INTERATIONS):
    run(STEPS, INTERATIONS, i + 1)
    
    STEPS += 1
    
    # Calc best result
    meanRes = []
    for res in results:
        meanRes.append(np.mean(res))
        
    # Print res
    if(i < 10): print(f"Iteration: 0{i}, score: {min(meanRes)}")
    else: print(f"Iteration: {i}, score: {min(meanRes)}")

    if i == INTERATIONS - 1: break
    allSteps.append(STEPS * 0.001) #amount of steps / 1000
    bestResults.append(round(min(meanRes), 4))
    
    removeNetworks(int(AMOUNT_OF_ENVIRONMENTS / REMOVE_BOTTOM) * REMOVE_TOP)
    addNetworks(REMOVE_TOP, 0.9, 1)
    
    
    errorHandler()
    
    
#Draw score
# indexBest = np.argmin(meanRes)

xbestResults = np.arange(len(bestResults))

print(xbestResults, bestResults)
plt.plot(xbestResults, bestResults, marker='o', linestyle='-')
plt.plot(xbestResults, allSteps, marker='o', linestyle='-')
plt.show()