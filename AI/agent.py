import torch
import random
import numpy as np
from collections import deque
from game import BalanceGame

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.numberOfgames = 0
        self.epsilon = 0 #randomness
        self.gamma = 0 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        # model, trainer


        
        
    def getState(self, game):
        pass

    def remeber(slef, state, action, reward, next_state, gameOver):
        pass

    def trainLongMemory(self):
        pass

    def trainShortMemory(self):
        pass

    def getAction(self, state):
        pass

def train():
    plotScores = []
    plotMeanScores = []
    totalScore = 0
    record = 0
    agent = Agent()
    game = BalanceGame()

    while True:
        # get old state
        stateOld = agent.getState(game)

        # get move
        finalMove = agent.getAction(stateOld)

        
    

if __name__ == "__main__":
    train()