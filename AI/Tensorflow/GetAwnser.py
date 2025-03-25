import gym
import keras
# from keras.models import Model
# from keras.callbacks import TensorBoard
# from keras.layers import Input, Dense, Activation, Reshape
# from keras.optimizers import Adam
# from rl.memory import SequentialMemory
# from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy
# from rl.agents.dqn import DQNAgent

env = gym.make('CartPole-v1')
env._max_episode_steps = 500  # Correct attribute name
num_actions = env.action_space.n

# Creating a simple NN model
observation = keras.layers.Input(shape=(1,) + env.observation_space.shape)
x = keras.layers.Dense(16, activation='relu')(observation)
x = keras.layers.Dense(16, activation='relu')(x)
x = keras.layers.Dense(16, activation='relu')(x)
output = keras.layers.Dense(num_actions, activation='linear')(x) 
output = keras.layers.Reshape((num_actions,))(output)

model = keras.models.Model(inputs=observation, outputs=output)
print(model.summary())


