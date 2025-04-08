import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def load_network():
    """
    Loads the weights and biases from the local AIParams folders.
    Returns a list of weight matrices and a list of bias vectors.
    """
    base_path = os.path.dirname(__file__)
    layer_path = os.path.join(base_path, "AIParams", "Layers")
    bias_path  = os.path.join(base_path, "AIParams", "Biases")

    if not os.path.exists(layer_path):
        raise FileNotFoundError(f"Layer path not found: {layer_path}")
    if not os.path.exists(bias_path):
        raise FileNotFoundError(f"Bias path not found: {bias_path}")

    layer_files = sorted(
        [f for f in os.listdir(layer_path) if f.startswith("Layer") and f.endswith(".npy")],
        key=lambda x: int(x.replace("Layer", "").replace(".npy", ""))
    )
    bias_files = sorted(
        [f for f in os.listdir(bias_path) if f.startswith("Bias") and f.endswith(".npy")],
        key=lambda x: int(x.replace("Bias", "").replace(".npy", ""))
    )

    weights = [np.load(os.path.join(layer_path, f)) for f in layer_files]
    biases  = [np.load(os.path.join(bias_path, f)) for f in bias_files]
    
    print(weights)
    # print(biases)

    return weights, biases

def interpolate_sign_color(value, max_value, weak_positive, strong_positive, weak_negative, strong_negative):
    """
    Interpolates between two colors based on the sign of value.
    For positive values, interpolates from weak_positive to strong_positive.
    For negative values, interpolates from weak_negative to strong_negative.
    Returns an (r, g, b) tuple.
    """
    if max_value == 0:
        t = 0
    else:
        t = np.clip(abs(value) / max_value, 0, 1)
    
    if value >= 0:
        r = (1 - t) * weak_positive[0] + t * strong_positive[0]
        g = (1 - t) * weak_positive[1] + t * strong_positive[1]
        b = (1 - t) * weak_positive[2] + t * strong_positive[2]
    else:
        r = (1 - t) * weak_negative[0] + t * strong_negative[0]
        g = (1 - t) * weak_negative[1] + t * strong_negative[1]
        b = (1 - t) * weak_negative[2] + t * strong_negative[2]
    
    return (r, g, b)

def show_network_diagram():
    # Load network parameters.
    weights, biases = load_network()
    # Determine architecture.
    input_size = weights[0].shape[1]
    layer_sizes = [input_size] + [w.shape[0] for w in weights]
    n_layers = len(layer_sizes)
    
    # Use maximum layer size for vertical centering.
    max_neurons = max(layer_sizes)
    
    # Drawing settings.
    x_spacing = 2.0  
    neuron_radius = 0.2

    # Compute vertical positions for neurons in each layer (centered).
    layer_positions = {}
    for i, n_neurons in enumerate(layer_sizes):
        offset = (max_neurons - n_neurons) / 2.0
        # Positions are in increasing order (bottom to top).
        positions = np.linspace(offset, offset + n_neurons - 1, n_neurons)
        layer_positions[i] = positions

    # Pre-calculate x positions.
    layer_x = {i: i * x_spacing for i in range(n_layers)}

    # Global maximums for scaling.
    global_max_weight = max(np.max(np.abs(W)) for W in weights)
    global_max_bias = max(np.max(np.abs(b)) for b in biases) if biases else 0

    # Define color ranges.
    # For weights:
    #   Positive: green hues.
    weight_weak_positive = (0.8, 1.0, 0.8)
    weight_strong_positive = (0.0, 0.5, 0.0)
    #   Negative: red hues.
    weight_weak_negative = (1.0, 0.8, 0.8)
    weight_strong_negative = (0.5, 0.0, 0.0)

    # For biases:
    #   Positive: yellow hues.
    bias_weak_positive = (1.0, 1.0, 0.8)
    bias_strong_positive = (0.8, 0.8, 0.0)
    #   Negative: blue hues.
    bias_weak_negative = (0.8, 0.8, 1.0)
    bias_strong_negative = (0.0, 0.0, 0.5)

    # Calculate input neuron impact: sum of absolute weights from the first layer.
    first_layer = weights[0]  # shape: (hidden_size, input_size)
    input_impacts = np.sum(np.abs(first_layer), axis=0)  # one value per input neuron
    max_impact = np.max(input_impacts)
    
    # Group input neurons in pairs.
    pair_impacts = []
    pair_labels = []
    for i in range(0, input_size, 2):
        if i + 1 < input_size:
            impact = input_impacts[i] + input_impacts[i+1]
            pair_labels.append(f"({i+1}, {i+2})")
        else:
            impact = input_impacts[i]
            pair_labels.append(f"({i+1})")
        pair_impacts.append(impact)
    
    # Sort pairs by impact (descending).
    sorted_pairs = sorted(zip(pair_labels, pair_impacts), key=lambda x: x[1], reverse=True)
    sorted_pairs_text = "\n".join([f"Pair {pair}: Impact = {impact:.2f}" for pair, impact in sorted_pairs])
    
    # Define high-impact threshold for individual input neurons.
    high_impact_threshold = 0.95 * max_impact

    # Create figure and axis.
    fig, ax = plt.subplots(figsize=(n_layers * 2.5, max_neurons))
    # Place the title clearly at the top.
    fig.suptitle("Neural Network Diagram", fontsize=16, y=0.98)
    ax.set_xlim(-1, (n_layers - 1) * x_spacing + 1)
    ax.set_ylim(-1, max_neurons)
    ax.axis('off')

    # Draw connections (weights) between layers.
    for i in range(n_layers - 1):
        W = weights[i]  # shape: (layer_sizes[i+1], layer_sizes[i])
        for j, y1 in enumerate(layer_positions[i]):
            for k, y2 in enumerate(layer_positions[i+1]):
                w_val = W[k, j]
                color = interpolate_sign_color(w_val, global_max_weight,
                                               weight_weak_positive, weight_strong_positive,
                                               weight_weak_negative, weight_strong_negative)
                lw = 1.5 * abs(w_val) / global_max_weight if global_max_weight != 0 else 1
                alpha = 0.1 + 0.9 * (abs(w_val) / global_max_weight) if global_max_weight != 0 else 1
                ax.plot([layer_x[i], layer_x[i+1]],
                        [y1, y2],
                        color=color,
                        linewidth=lw,
                        alpha=alpha,
                        zorder=1)

    # Draw neurons.
    for i in range(n_layers):
        x = layer_x[i]
        for idx, y in enumerate(layer_positions[i]):
            if i == 0:
                base_color = (0.8, 0.8, 0.8)
                alpha_input = 0.3 + 0.7 * (input_impacts[idx] / max_impact) if max_impact != 0 else 1
                facecolor = (base_color[0], base_color[1], base_color[2], alpha_input)
                if input_impacts[idx] >= high_impact_threshold:
                    edge_width = 3
                    edge_color = "gold"
                else:
                    edge_width = 1
                    edge_color = "black"
            else:
                b_val = biases[i-1][idx, 0]
                facecolor_rgb = interpolate_sign_color(b_val, global_max_bias,
                                                       bias_weak_positive, bias_strong_positive,
                                                       bias_weak_negative, bias_strong_negative)
                alpha_bias = 0.1 + 0.9 * (abs(b_val) / global_max_bias) if global_max_bias != 0 else 1
                facecolor = (facecolor_rgb[0], facecolor_rgb[1], facecolor_rgb[2], alpha_bias)
                edge_width = 1
                edge_color = "black"
            circle = mpatches.Circle((x, y), neuron_radius, ec=edge_color, fc=facecolor, lw=edge_width, zorder=2)
            ax.add_patch(circle)

    # Add layer labels below each column.
    for i in range(n_layers):
        if i == 0:
            label = f"Input\n({layer_sizes[i]})"
        elif i == n_layers - 1:
            label = f"Output\n({layer_sizes[i]})"
        else:
            label = f"Hidden {i}\n({layer_sizes[i]})"
        ax.text(layer_x[i], -0.8, label, ha="center", va="center", fontsize=12)

    # Create an explanation box (legend) that will be placed outside the network.
    legend_text = (
        "Colors Explanation:\n"
        "Weights: Negative = red, Positive = green\n"
        "Biases: Negative = blue, Positive = yellow\n"
        "Opacity indicates strength.\n\n"
        "Neuron Numbering: Bottom neuron is neuron 1;\nnumbering increases upward.\n\n"
        "Input Neuron Pair Impact Order:\n" +
        sorted_pairs_text
    )
    # Place the legend outside the network (to the right).
    fig.text(0.7, 0.8, legend_text, transform=fig.transFigure,
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'),
             fontsize=10, va="center", ha="left")
    
    plt.tight_layout(rect=[0, 0, 0.95, 0.95])
    plt.show()

if __name__ == "__main__":
    show_network_diagram()
