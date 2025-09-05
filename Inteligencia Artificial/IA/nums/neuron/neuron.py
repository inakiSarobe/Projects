import cupy as np

class Neuron:
    def __init__(self, input_size):
        self.weights = np.random.randn(input_size) * np.sqrt(1 / input_size)
        self.bias = 0.001
        self.output = None
        self.input = None
        self.is_output = False  

    def activate(self, x):
        return np.maximum(0, x)
    
    def forward(self, inputs):
        if inputs.ndim == 1:
            inputs = inputs[np.newaxis, :]
        self.input = inputs
        weighted_sum = np.dot(inputs, self.weights) + self.bias
        if self.is_output:
            self.output = weighted_sum  # Sin activación
        else:
            self.output = self.activate(weighted_sum)  # Sigmoid para capas ocultas
        return self.output
    
    def backward(self, d_outputs, learning_rate):
        batch_size = self.input.shape[0]

        if self.is_output:
            dE_dz = d_outputs
        else:
            dy_dz = (self.output > 0).astype(np.float32)  # Derivada de ReLU
            dE_dz = d_outputs * dy_dz  

        
        dE_dw = np.dot(self.input.T, dE_dz) / batch_size
        dE_db = np.sum(dE_dz, axis=0) / batch_size
        
        self.weights -= learning_rate * dE_dw
        self.bias -= learning_rate * dE_db
        
        dE_dinput = np.outer(dE_dz, self.weights)
        return dE_dinput
