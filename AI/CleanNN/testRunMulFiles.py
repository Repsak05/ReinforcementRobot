import subprocess
import serial #Pakken hedder pyserial


COM = "COM6"
BAUD = 115200
SERIAL = serial.Serial(COM, BAUD, timeout=1)

initialValues = {
    "iterations" : 50,
    "steps" : 250,
    "previousStates" : 3,
    "environments" : 50,
    "mutationRate" : 90, #Should be devided by 100
    "start" : 0,
}

def readSerial():
    allInput = ''

    if(SERIAL.is_open):
        
        while (allInput == ''):
            allInput = SERIAL.readline().decode().strip()
            both = allInput.split(":")
            
            if(len(both) == 2):
                    typeName = both[0]
                    value = both[1]
                    
                    initialValues[typeName] = value



while initialValues["start"] == 0: 
    readSerial()
    
# Convert to correct format
valuesStr = ""
for key in initialValues:
    valuesStr += f"{initialValues[key]},"
valuesStr = valuesStr[:-1]

print(valuesStr)

train = subprocess.Popen(["python", "Train.py", valuesStr])
runnerUpdate = subprocess.Popen(["python", "RealAIUpdate.py"])

while(1):
    # stop = input()
    if train.poll() != None:
        train.terminate()
        runnerUpdate.terminate()
        break

runner = subprocess.Popen(["python", "RealAI.py"])

while(1):
    stop = input()
    if stop == "stop":
        runner.terminate()
        break