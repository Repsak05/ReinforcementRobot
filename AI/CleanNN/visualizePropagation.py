import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def sigmoid(x):
    """Compute the sigmoid function."""
    return 1 / (1 + np.exp(-x))

def load_network():
    """
    Loads the weights and biases from the local AIParams folders.
    Returns lists of weight matrices and bias vectors.
    """
    base_path = os.path.dirname(__file__)
    layer_path = os.path.join(base_path, "AIParams", "Layers")
    bias_path  = os.path.join(base_path, "AIParams", "Biases")

    layer_files = sorted(
        [f for f in os.listdir(layer_path) if f.startswith("Layer")],
        key=lambda x: int(x.replace("Layer", "").replace(".npy", ""))
    )
    bias_files = sorted(
        [f for f in os.listdir(bias_path) if f.startswith("Bias")],
        key=lambda x: int(x.replace("Bias", "").replace(".npy", ""))
    )

    weights = [np.load(os.path.join(layer_path, f)) for f in layer_files]
    biases = [np.load(os.path.join(bias_path, f)) for f in bias_files]
    return weights, biases

def forward_propagate(weights, biases, input_vector):
    """
    Propagates the input_vector through the network using the sigmoid activation.
    Returns a list of activations (one per layer).
    """
    a = input_vector.reshape(-1, 1)  # Ensure column vector
    activations = [a]
    for W, b in zip(weights, biases):
        z = np.dot(W, a) + b
        a = sigmoid(z)
        activations.append(a)
    return activations

def show_activation_flow(input_values):
    weights, biases = load_network()
    activations = forward_propagate(weights, biases, np.array(input_values))
    
    # Determine layer sizes and number of layers.
    layer_sizes = [a.shape[0] for a in activations]
    n_layers = len(layer_sizes)
    max_neurons = max(layer_sizes)
    
    # Drawing settings.
    x_spacing = 2.0
    neuron_radius = 0.2
    layer_positions = {}
    layer_x = {i: i * x_spacing for i in range(n_layers)}
    
    # Compute vertical positions for each layer (neurons arranged bottom-to-top)
    for i, size in enumerate(layer_sizes):
        offset = (max_neurons - size) / 2.0
        layer_positions[i] = np.linspace(offset, offset + size - 1, size)
    
    # Using sigmoid, maximum activation is 1.
    max_activation = 1.0
    
    # Identify the output neuron with the highest activation.
    output_layer_index = n_layers - 1
    output_activations = activations[output_layer_index]
    max_output_index = int(np.argmax(output_activations))
    
    # Create the figure.
    fig, ax = plt.subplots(figsize=(n_layers * 2.5, max_neurons))
    fig.suptitle("Forward Propagation Visualization (Sigmoid)", fontsize=16, y=0.98)
    ax.set_xlim(-1, (n_layers - 1) * x_spacing + 1)
    ax.set_ylim(-1, max_neurons)
    ax.axis('off')
    
    # Draw connections between layers.
    # Connections use green for positive weights, red for negative.
    for i in range(n_layers - 1):
        for j, y1 in enumerate(layer_positions[i]):
            for k, y2 in enumerate(layer_positions[i+1]):
                w = weights[i][k, j]
                # Determine color: green for positive, red for negative.
                if w >= 0:
                    color = (0, 1, 0, 0.1 + 0.9 * abs(w) / np.max(np.abs(weights[i])) / 2)
                else:
                    color = (1, 0, 0, 0.1 + 0.9 * abs(w) / np.max(np.abs(weights[i])) / 2)
                ax.plot([layer_x[i], layer_x[i+1]],
                        [y1, y2],
                        color=color,
                        linewidth=1.5,
                        zorder=1)
    
    # Draw neurons and label their activation values.
    for i in range(n_layers):
        for j, y in enumerate(layer_positions[i]):
            a_val = activations[i][j, 0]
            # Set neuron fill opacity based on activation value.
            opacity = 1 #0.3 + 0.7 * a_val 
            facecolor = (1, 1, 1, opacity)
            
            # If this is the output layer and it's the max activated neuron, highlight it.
            if i == output_layer_index and j == max_output_index:
                edgecolor = 'gold'
                lw = 3.0
            else:
                edgecolor = 'black'
                lw = 1.5
            
            circle = mpatches.Circle((layer_x[i], y), neuron_radius, ec=edgecolor, fc=facecolor, lw=lw, zorder=2)
            ax.add_patch(circle)
            ax.text(layer_x[i], y, f"{a_val:.2f}", fontsize=8, ha='center', va='center', zorder=3)
    
    # Add layer labels below each column.
    for i in range(n_layers):
        if i == 0:
            label = "Input"
        elif i == output_layer_index:
            label = "Output"
        else:
            label = f"Hidden {i}"
        ax.text(layer_x[i], -0.8, f"{label}\n({layer_sizes[i]})", ha="center", va="center", fontsize=11)
    
    # Place a legend (explanation box) outside the network, to the right.
    legend_text = (
        "Legend:\n"
        "Weights: Green = positive, Red = negative\n"
        "Neuron fill: Activation level (0 - 1 using sigmoid)\n"
        "Connection opacity = weight strength\n"
        "Values inside neurons: Activation outputs\n"
        "Gold border: Output neuron with highest activation"
    )
    fig.text(.7, 0.8, legend_text, transform=fig.transFigure,
             bbox=dict(facecolor='white', edgecolor='black', alpha=0.9),
             fontsize=10, va='center', ha='left')
    
    plt.tight_layout(rect=[0, 0, 0.95, 0.95])
    plt.show()

if __name__ == "__main__":
    # Replace with your actual input vector matching your network's input size, e.g., 6 values.
    example_input = [
        .1, .5,
        .2, .2,
        .4, .1
    ]
    show_activation_flow(example_input)
