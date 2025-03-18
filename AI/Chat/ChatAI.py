import numpy as np
import random
import matplotlib.pyplot as plt
import serial
import time

# Q-learning parameters
alpha = 0.05  # Lower learning rate for more stable learning
gamma = 0.95  # Higher discount factor to value future rewards more
epsilon = 1.0  # Start with full exploration
epsilon_decay = 0.999  # Gradually reduce exploration
min_epsilon = 0.01  # Minimum exploration threshold
num_episodes = 1

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
		print(distance)
	if distance == '':
		return 0.26

	return float(distance)

# Define the environment
class BalancingEnv:
    def __init__(self):
        self.angle = 0  # Initial plate angle
        self.position = 0.25  # Cylinder's initial position (distance from one side)
        self.dt = 0.1  # Time step
        self.max_angle = 30  # Maximum tilt angle in degrees
        self.max_position = 0.26  # Maximum cylinder position
        self.steps = 0
    
    def reset(self):
        self.angle = 0
        self.position = random.uniform(-5, 5)
        return self.get_state()
    
    def get_state(self):
        return (round(self.angle, 1), round(self.position, 1))
    
    def step(self, action):
        # Convert action into an angle change (-1, 0, 1 degrees)
        self.angle += action*10
        self.angle = max(-self.max_angle, min(self.max_angle, self.angle))
        writeToArduino(90+self.angle)
        
        # Update position randomly to simulate unknown velocity dynamics
        # self.position += random.uniform(-0.5, 0.5)
        time.sleep(0.1)
        self.position = readSerial()

        
        # Check if the cylinder is out of bounds
        done = self.position > self.max_position or self.position <= 0.01
        reward = -10 if done else 1 - (5 * abs(0.14 - self.position))  # Give higher penalty for falling off
        global epsilon
        if self.steps%500 == 0:
             epsilon *= 0.8
             print("epsilon:", epsilon)

        if self.steps == 49:
             print(Q)

        if done: print("Done:",self.position)
        # else: print("Dist:",self.position)

        self.steps += 1
        return self.get_state(), reward, done

def get_q(state):
    if state not in Q:
        Q[state] = [0, 0, 0]  # Actions: tilt left (-1), stay (0), tilt right (+1)
    return Q[state]

def choose_action(state):
    if random.uniform(0, 1) < epsilon:
        return random.choice([-1, 0, 1])  # Explore
    else:
        return np.argmax(get_q(state)) - 1  # Exploit

env = BalancingEnv()

epsilon_values = []
for episode in range(num_episodes):
    state = env.reset()
    done = False
    total_reward = 0
    
    while not done:
        action = choose_action(state)
        next_state, reward, done = env.step(action)
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

# Plot training results
fig, axs = plt.subplots(2, 1, figsize=(10, 8))
axs[0].plot(rewards_per_episode)
axs[0].set_xlabel('Episode')
axs[0].set_ylabel('Total Reward')
axs[0].set_title('Q-learning Training Progress')

axs[1].plot(epsilon_values)
axs[1].set_xlabel('Episode')
axs[1].set_ylabel('Epsilon')
axs[1].set_title('Epsilon Decay Over Time')

plt.tight_layout()
plt.show()

