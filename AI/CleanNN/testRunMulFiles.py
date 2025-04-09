import subprocess
import serial #Pakken hedder pyserial


COM = "COM6"
BAUD = 115200
SERIAL = serial.Serial(COM, BAUD, timeout=1)

initialValues = {
    "hiddenLayers" : 1, 
    "neuronsInHiddenLayer" : 20, 
    "previousStates" : 3, 
    "steps" : 200, 
    "angleSpeed" : 5, #Should be devided by 100
    "antalIterationer" : 50, 
    "malPlacering" : 50, #Should be devided by 100
    "start" : 0
}

def readSerial():
    allInput = ''
    typeName = ""
    value = 0

    if(SERIAL.is_open):
        
        while (allInput == ''):
            allInput = SERIAL.readline().decode().strip()
            both = allInput.split(":")
            
            if(len(both) == 2):
                    typeName = both[0]
                    value = both[1]
                    
                    initialValues[typeName] = value
    
    print({"type" : typeName, "value" : value})
    return {"type" : typeName, "value" : value}



while initialValues["start"] == 0: 
    readSerial()
    
# Convert to correct format
valuesStr = ""
for key in initialValues:
    valuesStr += f"{initialValues[key]},"
valuesStr = valuesStr[:-1]

train = subprocess.Popen(["python", "Train.py", valuesStr])
runnerUpdate = subprocess.Popen(["python", "RealAIUpdate.py"])

while(1):
    stop = input()
    if stop == "stop":
        train.terminate()
        runnerUpdate.terminate()
        break

runner = subprocess.Popen(["python", "RealAI.py"])

while(1):
    stop = input()
    if stop == "stop":
        runner.terminate()
        break