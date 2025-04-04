from functions import *
import numpy as np
from NeuralNetwork import NeuralNetwork
import math

ANGLE_SPEED = 0.05 # IKKE DEN RIGTIGE ÆNDRER DEN
MIN_ANGLE = math.pi - math.pi / 18
MAX_ANGLE = math.pi + math.pi / 18

# # Load Netværk
# layers = []
# biases = []
# for i in range(3):
#     layers.append(np.load(f"AIParams/Layers/Layer{i}.npy"))
#     biases.append(np.load(f"AIParams/Biases/Bias{i}.npy"))

# network = NeuralNetwork()
# network.init(layers, biases, 0, 0, 0)
network = NeuralNetwork()
network.randInit(2,3,20,1)

angle = math.pi/2

input("Start:")

print(math.degrees(angle))

writeToArduino(math.degrees(angle))

distNorm = readSerial()

while(1):
    step = np.matrix([[normalizeAngle(angle)],[distNorm]])

    possibleMoves = network.calcOutput(step)

    dir =  np.argmax(possibleMoves) - 1
    action = dir * possibleMoves[dir + 1, 0] * ANGLE_SPEED
    print(action)
    angle += action
    angle = min(angle, (math.pi/2) + (math.pi / 18))
    angle = max(angle, (math.pi/2) - (math.pi / 18))

    writeToArduino(math.degrees(angle))
    distNorm = readSerial()