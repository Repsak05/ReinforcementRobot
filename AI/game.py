# Reset
# Reward
# play(action) -> direction
# gameIteration
# isDead
isDead = False

class BalanceGame:
    def runGame(self):
        self.play_step(0)
        reward = 0
        if isDead:
            reward = -10

    def reset(self):
        print("RESET")
        print("RESET")
        print("RESET")

    def play_step(self, action):
        # action = {-1, 0, 1}
        self.updateAngle(action)

    def updateAngle(self,action):
        pass