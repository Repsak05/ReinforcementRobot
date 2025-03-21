import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

# Define the AI model
def create_model():
    model = keras.Sequential([
        layers.Dense(16, activation='relu', input_shape=(2,)),
        layers.Dense(16, activation='relu'),
        layers.Dense(1, activation='tanh')  # Output change in angle (-1 to 1 scaled)
    ])
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.01), loss='mse')
    return model

# Create the model
model = create_model()

# Example function to predict action
def get_action(distance_from_center, current_angle):
    input_data = np.array([[distance_from_center, current_angle]])
    delta_angle = model.predict(input_data, verbose=0)[0, 0]
    print("Change in angle:", delta_angle)
    return delta_angle

# Example usage
if __name__ == "__main__":
    # Example inputs
    distance_from_center = 0.5  # Change this dynamically in real environment
    current_angle = 0.1  # Change this dynamically in real environment
    
    get_action(distance_from_center, current_angle)