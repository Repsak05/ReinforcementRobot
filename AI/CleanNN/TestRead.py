import numpy as np
from NeuralNetwork import NeuralNetwork
from Environment import Environment
import math
# from Train import realDistanceToCenter, normalizeAngle, ANGLE_SPEED, CENTER_BOX

MAX_POSITION = 90
MIN_POSITION = 0

ANGLE_SPEED = 0.05
MIN_ANGLE = math.pi - math.pi / 18
MAX_ANGLE = math.pi + math.pi / 18

CENTER_BOX = [400, 450]

def normalizeDist(value):
    return (value - MIN_POSITION) / (MAX_POSITION - MIN_POSITION)

def normalizeAngle(angle):
    return (angle - MIN_ANGLE) / (MAX_ANGLE - MIN_POSITION)

def realDistanceToCenter(ballX, ballY, floorX, floorY):
    distance = math.sqrt(pow((ballX - floorX), 2) + pow((ballY - floorY), 2))
    nDist = normalizeDist(distance)
    
    if(nDist < 0 or nDist > 1): print("INVALID: ", nDist, " must be within bounds [0, 1]")
    return nDist

layers = []
biases = []
for i in range(3):
    layers.append(np.load(f"AIParams/Layers/Layer{i}.npy"))
    biases.append(np.load(f"AIParams/Biases/Bias{i}.npy"))

network = NeuralNetwork()
network.init(layers, biases, 0, 0, 0)

print(network.biases)

env = Environment()
env.init(True)

while True:
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
    print(abs(0.5 - dist)*2)
    
    # possibleMoves = neuralNetworks[i].calcOutput(np.matrix([[angle],[dist]]))
    possibleMoves = network.calcOutput(env.steps)

    # print(possibleMoves)

    

    dir =  np.argmax(possibleMoves) - 1
    action = dir * possibleMoves[dir + 1, 0] * ANGLE_SPEED
    env.runDraw(action)

