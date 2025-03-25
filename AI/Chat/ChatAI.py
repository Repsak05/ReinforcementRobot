import numpy as np
import random
import matplotlib.pyplot as plt
import serial
import time
import csv
import json 


# Q-learning parameters
alpha = 0.05  # Lower learning rate for more stable learning
gamma = 0.95  # Higher discount factor to value future rewards more
epsilon = 1.0  # Start with full exploration
epsilon_decay = 0.99  # Gradually reduce exploration
min_epsilon = 0.01  # Minimum exploration threshold
num_episodes = 150

# Initialize Q-table
Q = {}
rewards_per_episode = []

COM = "COM5"
BAUD = 115200
s = serial.Serial(COM, BAUD, timeout=1)

def writeToArduino(position):
	if(s.is_open):
		s.write(bytes([position]))

def readSerial():
	distance = 0
	if(s.is_open):
		distance = s.readline().decode().strip()
		# print(distance)
	if distance == '':
		return 0.26

	return float(distance)

def current_milli_time():
    return round(time.time() * 1000)
# Define the environment
class BalancingEnv:
    def __init__(self):
        self.angle = 0  # Initial plate angle
        self.position = readSerial()  # Cylinder's initial position (distance from one side)
        self.dt = 0.1  # Time step
        self.max_angle = 30  # Maximum tilt angle in degrees
        self.max_position = 235  # Maximum cylinder position
        self.min_position = 45
        self.steps = 0
        self.failures = 0
        self.centrum = 140
        self.startingTime = current_milli_time()
    
    def reset(self):
        self.failures = 0
        self.angle = 0
        writeToArduino(90)
        self.position = readSerial()
        time.sleep(0.5)
        self.startingTime = current_milli_time()
        return self.get_state()
    
    def get_state(self):
        return (round(self.angle), round(self.position / 20) * 20)
    
    def getReward(self, action):
        currentTime = current_milli_time()
        reward = 0
        while(current_milli_time() < currentTime + 300):
            # print(self.position)
            writeToArduino(90 + self.angle)
            self.position = readSerial() 
            
            if not failure and self.position >= 40 and self.position <= 230:
                reward += pow(self.centrum - (abs(self.centrum - self.position)), 1)
            
            if self.position >= self.max_position and action > 0:
                reward += 1000
            if self.position <= self.min_position and action < 0:
                reward += 1000
            
            if self.position >= self.max_position and action < 0:
                reward -= 1000
            if self.position <= self.min_position and action > 0:
                reward -= 1000
                
        return reward
                
            
    
    def step(self, action):
        # Convert action into an angle change (-1, 0, 1 degrees)
        self.angle += action * 5
        self.angle = max(-self.max_angle, min(self.max_angle, self.angle)) #? Should it not be self.min_angle?
        writeToArduino(90 + self.angle)
        
        # Update position randomly to simulate unknown velocity dynamics
        # self.position += random.uniform(-0.5, 0.5)
        self.position = readSerial()

        global done
        global failure
        failure = False
        # Check if the cylinder is out of bounds
        invincibilityTime = 4000
        if self.position >= self.max_position or self.position <= self.min_position:
            if self.startingTime + invincibilityTime < current_milli_time():
                print("FAIL")
                done = True
            # failure = True
        #     self.failures += 1
        # if self.failures >= 20:
        #     done = True
        # done = self.position > self.max_position or self.position <= 40
        # done = False
        reward = self.getReward(action)
        # if not failure:
        #     reward = pow(self.centrum - (abs(self.centrum - self.position) + 30), 2)
        
        # reward = 0 if failure else pow(self.centrum - abs(self.centrum - self.position),2)  # Give higher penalty for falling off
        
        

        print(f"Reward {reward} :    action: {action}")
        # global epsilon
        # if self.steps%500 == 0:
        #      epsilon *= 0.8
        #      print("epsilon:", epsilon)

        if done: print("Done:", self.position)
        # else: print("Dist:",self.position)

        self.steps += 1
        return self.get_state(), reward, done

def get_q(state):
    if state not in Q:
        Q[state] = [0, 0, 0]  # Actions: tilt left (-1), stay (0), tilt right (+1)
    return Q[state]

def choose_action(state):
    if random.uniform(0, 1) < epsilon:
        print("IS  Random")
        return random.choice([-1, 0, 1])  # Explore
    else:
        print("NOT Random")
        return np.argmax(get_q(state)) - 1  # Exploit

env = BalancingEnv()

epsilon_values = []
for episode in range(num_episodes):
    # print("Start new episode? (y/n)\n")
    # wait = input()
    # if wait == "n":
    #      break

    print("Episode:", episode)
    state = env.reset()
    done = False
    total_reward = 0
    
    while not done:
        action = choose_action(state)
        next_state, reward, done = env.step(action)
        # time.sleep(1)
        total_reward += reward
        
        # Q-learning update
        q_values = get_q(state)
        q_next = max(get_q(next_state))
        q_values[action + 1] += alpha * (reward + gamma * q_next - q_values[action + 1])
        
        state = next_state
        if env.steps == 50:
            break

    rewards_per_episode.append(total_reward)
    epsilon = max(min_epsilon, epsilon * epsilon_decay)  # Decay epsilon
    epsilon_values.append(epsilon)

print("Training complete!")
print(Q)



data = []
for key in Q:
    data.append([key[0],key[1],np.argmax(Q[key]) - 1])
    # newDict[key] = np.argmax(Q[key]) - 1

print(data)
csv_filename = "test1.csv"
fieldnames = ["Angle", "Distance", "Action"]

with open(csv_filename, 'w', newline='') as f:
     
    # using csv.writer method from CSV package
    write = csv.writer(f)
     
    write.writerow(fieldnames)
    write.writerows(data)


# Plot training results

window = 5

average_data = []
for ind in range(len(rewards_per_episode)):
    average_data.append(np.mean(rewards_per_episode[0:ind]))

fig, axs = plt.subplots(2, 1, figsize=(10, 8))
axs[0].plot(rewards_per_episode)
axs[0].plot(average_data)
axs[0].set_xlabel('Episode')
axs[0].set_ylabel('Total Reward')
axs[0].set_title('Q-learning Training Progress')

axs[1].plot(epsilon_values)
axs[1].set_xlabel('Episode')
axs[1].set_ylabel('Epsilon')
axs[1].set_title('Epsilon Decay Over Time')

plt.tight_layout()
plt.show()
print("\n\n\n\n")

newQ = {}
for key in Q:
     newQ[str(key)] = str(Q[key])

with open("Agent.json", "w") as outfile: 
    Kasper = json.dumps(newQ)
    outfile.write(Kasper)