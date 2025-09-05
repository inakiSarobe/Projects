import cupy as np
from neuron.neuron import Neuron

class Layer:
    def __init__(self, num_neurons, input_size):
        self.neurons = [Neuron(input_size) for _ in range(num_neurons)]
    
    def forward(self, inputs):
        outputs = [neuron.forward(inputs) for neuron in self.neurons]
        return np.stack(outputs, axis=1)
    
    def backward(self, d_outputs, learning_rate):
        d_inputs_list = []
        for i, neuron in enumerate(self.neurons):
            d_output = d_outputs[:, i]
            d_input = neuron.backward(d_output, learning_rate)
            d_inputs_list.append(d_input)
        d_inputs = np.sum(np.stack(d_inputs_list, axis=0), axis=0)
        return d_inputs
    
    def to_dict(self):
        return [neuron.to_dict() for neuron in self.neurons]
    
    def from_dict(self, data):
        for neuron, neuron_data in zip(self.neurons, data):
            neuron.from_dict(neuron_data)
