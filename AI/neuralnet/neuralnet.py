import numpy as np
import matplotlib.pyplot as plt

# inpN = (inp - inp.min()) / (inp.max() - inp.min())

wih = np.random.uniform(-0.5, 0.5, (20,2))
who = np.random.uniform(-0.5, 0.5, (3,20))

bih = np.zeros((20,1))
bho = np.zeros((3,1))

learnRate = 0.1

inp = np.zeros((2,1))

while True:
    curAngle = float(input("Angle: "))
    curDist = float(input("Dist: "))
    inp[0][0] = curAngle/180
    inp[1][0] = (curDist-40)/(240-40)

    hPre = bih + wih @ inp
    h = 1/ (1 + np.exp(-hPre))

    oPre = bho + who @ h
    output = 1 / (1 + np.exp(-oPre))
    print(output)
