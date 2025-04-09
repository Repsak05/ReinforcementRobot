from functions import *
import numpy as np
from NeuralNetwork import NeuralNetwork
import math
import time
import matplotlib.pyplot as plt

ANGLE_SPEED = 0.05
MIN_ANGLE = math.pi/2 - math.pi / 18
MAX_ANGLE = math.pi/2 + math.pi / 18

RELOAD_TIME = 3
PATH_NAME = "AIParams"

global layers
global biases

# # Load Netværk
layers = []
biases = []
loadNetwork(PATH_NAME, 3, layers, biases)

PREVIOUS_STATES = int(len(layers[0][0])/2)
steps = np.array([[math.pi],[1]])

for _ in range(PREVIOUS_STATES - 1):
    steps = np.append(steps, [[math.pi],[1]], axis=0)

network = NeuralNetwork()
network.init(layers, biases, 0, 0, 0)

angle = math.pi/2

time.sleep(2)

print(math.degrees(angle))

writeToArduino(math.degrees(angle))

distNorm = readSerial()

# step = np.array([
#     [normalizeAngle(math.pi/2)],[distNorm],
#     [normalizeAngle(math.pi/2)],[distNorm],
#     [normalizeAngle(math.pi/2)],[distNorm]
#     ])

startTime = time.time()

distances = []
distancesMean = []
xVals = []
# plt.ion()
# plt.plot(xVals, distancesMean, color='red')
# plt.show(block=False)

UpdateNetwork = True

i = 0
while(1):
    steps = np.append(steps, [[angle],[distNorm]], axis=0)
    steps = steps[2:]


    possibleMoves = network.calcOutput(steps)


    distances.append(abs(0.5 - distNorm)*2)

    # print(normalizeAngle(angle))

    # print("Angle:",step[0][0], "      Dist:", step[1][0])

    dir =  np.argmax(possibleMoves) - 1
    action = dir * possibleMoves[dir + 1, 0] * ANGLE_SPEED
    # print(action)
    angle += action
    angle = min(angle, (math.pi/2) + (math.pi / 18))
    angle = max(angle, (math.pi/2) - (math.pi / 18))

    writeToArduino(math.degrees(angle))
    distNorm = readSerial()

    # if startTime + RELOAD_TIME < time.time() and UpdateNetwork:
    # #     distancesMean.append(np.mean(distances))
    # #     xVals.append(i)
    # #     i += 1
    # #     distances = []
    # #     plt.plot(xVals, distancesMean, color='red')
    # #     plt.pause(0.01)

        # print("Start Load")
        # oldLayers = layers
        # layers = []
        # biases = []
        # loadNetwork(PATH_NAME, 3, layers, biases)
        # network.init(layers, biases, 0, 0, 0)
        # writeToArduino(90)
        # time.sleep(1)
        # startTime = time.time()
        # print("Stop Load")
