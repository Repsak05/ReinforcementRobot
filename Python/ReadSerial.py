import serial #Pakken hedder pyserial
import sys
import glob
import time

COM = "COM9"
BAUD = 115200
s = serial.Serial(COM, BAUD, timeout=1)

def writeToArduino(position):
	if(s.is_open):
		s.write(bytes([position]))

   
def readSerial():
	distance = 0
	if(s.is_open):
		distance = s.readline().decode().strip()
		print(distance)
    
	return distance
   
while(1):
	angle = int(input())
	writeToArduino(angle)
	distance = readSerial()
