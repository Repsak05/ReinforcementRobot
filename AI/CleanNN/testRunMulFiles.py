import subprocess
import serial #Pakken hedder pyserial


COM = "COM9"
BAUD = 115200
SERIAL = serial.Serial(COM, BAUD, timeout=1)

initialValues = {
    "Iterationer" : 50,
    "Max Sim Tid" : 250,
    "Input Stadier" : 3,
    "Parallelle AI's" : 50,
    "Mutationsrate" : 90, #Should be devided by 100
    "Start" : 0,
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
                    print({"type" : typeName, "value" : value})


while(1):
    global finished
    finished = False
    
    while initialValues["Start"] == 0:
        readSerial()
    
    initialValues["Start"] == 0
    
    # Convert values
    valuesStr = ""
    for key in initialValues:
        valuesStr += f"{initialValues[key]},"
    valuesStr = valuesStr[:-1]
    
    train = subprocess.Popen(["python", "Train.py", valuesStr])
    runnerUpdate = subprocess.Popen(["python", "RealAIUpdate.py"])
    
    while(1):
        readSerial()
            
        # stop = input()
        if initialValues["Start"] == 1:
            finished = True
            
        if train.poll() != None or finished:
            train.terminate()
            runnerUpdate.terminate()
            break

    if not finished:
        runner = subprocess.Popen(["python", "RealAI.py"])

        while(1):
            readSerial()
            if initialValues["Start"] == 1:
                finished = True
                runner.terminate()
                break
                
            stop = input()
            if stop == "stop":
                runner.terminate()
                break
    

# while initialValues["Start"] == 0: 
#     # print(initialValues["start"])
#     readSerial()
    
# # Convert to correct format
# valuesStr = ""
# for key in initialValues:
#     valuesStr += f"{initialValues[key]},"
# valuesStr = valuesStr[:-1]

# print(f"\n\n\n{valuesStr}\n\n\n")

# train = subprocess.Popen(["python", "Train.py", valuesStr])
# runnerUpdate = subprocess.Popen(["python", "RealAIUpdate.py"])

# while(1):
#     # stop = input()
#     if train.poll() != None:
#         train.terminate()
#         runnerUpdate.terminate()
#         break

# runner = subprocess.Popen(["python", "RealAI.py"])

# while(1):
#     stop = input()
#     if stop == "stop":
#         runner.terminate()
#         break