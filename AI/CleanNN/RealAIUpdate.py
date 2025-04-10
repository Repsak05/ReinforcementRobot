from functions import *
import numpy as np
from NeuralNetwork import NeuralNetwork
import math
import time
import matplotlib.pyplot as plt

ANGLE_SPEED = 0.05
MIN_ANGLE = math.pi - math.pi / 18
MAX_ANGLE = math.pi + math.pi / 18

RELOAD_TIME = 6
PATH_NAME = "AIParams"

global layers
global biases

# # Load Netværk
layers = []
biases = []
time.sleep(1)
loadNetwork(PATH_NAME, 3, layers, biases)

PREVIOUS_STATES = int(len(layers[0][0])/2)


angle = math.pi/2

time.sleep(2)

print(math.degrees(angle))

writeToArduino(math.degrees(angle))

distNorm = readSerial()

startTime = time.time()

steps = np.array([[0.5],[distNorm]])

for _ in range(PREVIOUS_STATES - 1):
    steps = np.append(steps, [[0.5],[distNorm]], axis=0)

network = NeuralNetwork()
# network.init(layers, biases, 0, 0, 0)
network.randInit(PREVIOUS_STATES*2,3,20,1)

distances = []
distancesMean = []
xVals = []
# plt.ion()
# plt.plot(xVals, distancesMean, color='red')
# plt.show(block=False)

UpdateNetwork = True

i = 0
while(1):
    steps = np.append(steps, [[normalizeAngle(angle)],[distNorm]], axis=0)
    steps = steps[2:]
    # print("LENGTH:",len(steps))
    possibleMoves = network.calcOutput(steps)

    distances.append(abs(0.5 - distNorm)*2)

    dir =  np.argmax(possibleMoves) - 1
    action = dir * possibleMoves[dir + 1, 0] * ANGLE_SPEED

    angle += action
    angle = min(angle, (math.pi/2) + (math.pi / 18))
    angle = max(angle, (math.pi/2) - (math.pi / 18))

    writeToArduino(math.degrees(angle))
    distNorm = readSerial()

    if startTime + RELOAD_TIME < time.time() and UpdateNetwork:
        print("Start Load")
        oldLayers = layers
        layers = []
        biases = []
        loadNetwork(PATH_NAME, 3, layers, biases)
        network.init(layers, biases, 0, 0, 0)
        writeToArduino(90)
        time.sleep(1)
        startTime = time.time()
        print("Stop Load")
