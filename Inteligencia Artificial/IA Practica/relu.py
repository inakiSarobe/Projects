import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import time

# --- Definir la red neuronal ---
class NeuralNetwork:
    def __init__(self, layers):
        self.layers = layers
        self.weights = [np.random.randn(layers[i], layers[i-1]) * 0.1 for i in range(1, len(layers))]
        self.biases = [np.random.randn(layers[i], 1) * 0.1 for i in range(1, len(layers))]
        self.activations = [np.zeros((l, 1)) for l in layers]  # Guardar activaciones

    def relu(self, x):
        return np.maximum(0, x)

    def forward(self, x):
        self.activations[0] = x
        for i in range(len(self.weights)):
            z = self.weights[i] @ self.activations[i] + self.biases[i]
            self.activations[i+1] = self.relu(z)
        return self.activations[-1]

# --- Crear la red y el gráfico ---
layers = [5, 10, 6, 3]  # Ejemplo: 5 entradas, 10 en capa oculta, 6 en otra capa oculta, 3 salida
nn = NeuralNetwork(layers)

def visualize_network(nn, dead_neurons):
    plt.clf()
    G = nx.DiGraph()
    positions = {}
    node_colors = []

    # Crear nodos
    y_spacing = 1.5
    for layer_idx, num_nodes in enumerate(nn.layers):
        for node_idx in range(num_nodes):
            pos = (layer_idx, -node_idx * y_spacing)
            positions[f"L{layer_idx}N{node_idx}"] = pos
            is_dead = (layer_idx > 0 and dead_neurons[layer_idx-1][node_idx])
            node_colors.append("red" if is_dead else "blue")  # Neuronas muertas en rojo

    # Crear conexiones
    for layer_idx in range(len(nn.layers) - 1):
        for n1 in range(nn.layers[layer_idx]):
            for n2 in range(nn.layers[layer_idx+1]):
                G.add_edge(f"L{layer_idx}N{n1}", f"L{layer_idx+1}N{n2}")

    # Dibujar el grafo
    nx.draw(G, positions, with_labels=False, node_color=node_colors, edge_color="gray", node_size=500)
    plt.pause(0.1)

# --- Entrenamiento y detección de neuronas muertas ---
plt.ion()  # Activar modo interactivo
dead_neurons_history = []

for epoch in range(100):
    x = np.random.randn(layers[0], 1)  # Entrada aleatoria
    nn.forward(x)

    # Detectar neuronas muertas
    dead_neurons = [np.all(a == 0, axis=1) for a in nn.activations[1:]]
    dead_neurons_history.append(dead_neurons)
    
    # Actualizar gráfico
    visualize_network(nn, dead_neurons)
    time.sleep(0.05)

plt.ioff()
plt.show()
