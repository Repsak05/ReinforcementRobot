import subprocess

train = subprocess.Popen(["python", "Train.py"])

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