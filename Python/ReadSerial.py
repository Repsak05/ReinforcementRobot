import serial #Pakken hedder pyserial
import sys
import glob
import time

COM = "COM5"
BAUD = 115200
SERIAL = serial.Serial(COM, BAUD, timeout=1)

def writeToArduino(position):
	if(SERIAL.is_open):
		SERIAL.write(bytes([position]))

   
def readSerial():
	distance = 0
	if(SERIAL.is_open):
		distance = SERIAL.readline().decode().strip()
		print(distance)
    
	return distance


while(1):
	angle = int(input())

	# angle = int(100)

	writeToArduino(angle)
	distance = readSerial()
