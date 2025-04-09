import serial #Pakken hedder pyserial
import math
import numpy as np

COM = "COM1"
BAUD = 115200
SERIAL = serial.Serial(COM, BAUD, timeout=1)

MIN_ANGLE = math.pi / 2 - math.pi / 18
MAX_ANGLE = math.pi / 2 + math.pi / 18

def normalizeAngle(angle):
    return (angle - MIN_ANGLE) / (MAX_ANGLE - MIN_ANGLE)

def loadNetwork(path, layerCount, layers, biases):
    for i in range(layerCount):
        layers.append(np.load(f"{path}/Layers/Layer{i}.npy"))
        biases.append(np.load(f"{path}/Biases/Bias{i}.npy"))

def writeToArduino(position):
    # print(position)
    if(SERIAL.is_open):
        SERIAL.write(bytes([int(position)]))

   
def readSerial():
    distance = 0
    if(SERIAL.is_open):
        distance = SERIAL.readline().decode().strip()
        # print("dist:",distance)
        while (distance == ''):
            distance = SERIAL.readline().decode().strip()
            # print("dist:",distance)
    
    # return int(distance)
    return (int(distance)-40)/(205-40)

# def normalizeAngle(angle):
#     return (angle - MIN_ANGLE) / (MAX_ANGLE - 0)  # -MIN_POSITION ??????????