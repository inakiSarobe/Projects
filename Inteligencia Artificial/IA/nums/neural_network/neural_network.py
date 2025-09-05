import time, math, h5py
import cupy as cp
from layer.layer import Layer

class NeuralNetwork:
    def __init__(self):
        self.layers = []           # Lista vacía de capas
        self.loss_list = []        # Evolución de la pérdida
        self.epoch_offset = 0      # Para reanudar el entrenamiento
        self.current_lr = None 

    def add_layer(self, num_neurons, input_size, is_output=False):
        layer = Layer(num_neurons, input_size)
        if is_output:
            for neuron in layer.neurons:
                neuron.is_output = True
        self.layers.append(layer)

    def softmax(self, x):
        exp_x = cp.exp(x - cp.max(x, axis=1, keepdims=True))
        return exp_x / cp.sum(exp_x, axis=1, keepdims=True)

    def categorical_crossentropy(self, y_true, y_pred):
        y_pred = cp.clip(y_pred, 1e-8, 1 - 1e-8)  # Evita valores extremos
        return -cp.mean(cp.sum(y_true * cp.log(y_pred), axis=1))

    def forward(self, inputs):
        for i, layer in enumerate(self.layers):
            inputs = layer.forward(inputs)
            if i == len(self.layers) - 1:  # Softmax en la última capa
                inputs = self.softmax(inputs)
        return inputs



    @staticmethod
    def adjust_learning_rate_cosine(initial_lr, eta_min, current_epoch, T_max):
        """
        Calcula el learning rate usando Cosine Annealing,
        partiendo del valor inicial y disminuyendo hasta eta_min a lo largo de T_max épocas.
        """
        return eta_min + 0.5 * (initial_lr - eta_min) * (1 + cp.cos(cp.pi * current_epoch / T_max))

    def train(self, X, y, epochs, initial_lr, batch_size, eta_min):
        num_samples = X.shape[0]
        total_start = time.time()

        if self.current_lr is None:
            self.current_lr = initial_lr

        T_max = epochs + self.epoch_offset
        best_loss = min(self.loss_list) if self.loss_list else float('inf')
        best_weights = None  

        for epoch in range(epochs):
            current_epoch = epoch + self.epoch_offset
            permutation = cp.random.permutation(num_samples)
            X_shuffled = X[permutation]
            y_shuffled = y[permutation]
            epoch_loss = 0

            # Ajustar el learning rate con Cosine Annealing
            lr_t = self.adjust_learning_rate_cosine(self.current_lr, eta_min, current_epoch, T_max)

            for i in range(0, num_samples, batch_size):
                X_batch = X_shuffled[i:i+batch_size]
                y_batch = y_shuffled[i:i+batch_size]

                output = self.forward(X_batch)
                loss = self.categorical_crossentropy(y_batch, output)
                epoch_loss += loss.item() * X_batch.shape[0]

                loss_gradient = output - y_batch
                self.backward(loss_gradient, lr_t)

            cp.cuda.Device(0).synchronize()
            epoch_loss /= num_samples
            self.loss_list.append(epoch_loss)

            # Ajustar el learning rate dinámicamente
            if epoch_loss < best_loss:
                best_loss = epoch_loss
                best_weights = [cp.copy(layer.weights) for layer in self.layers]
                self.current_lr *= 1.05  # Pequeño aumento si mejora
            else:
                self.current_lr *= 0.7  # Reducir si empeora

            print(f"Época {current_epoch+1}, Pérdida: {epoch_loss*100:.4f}%, Learning Rate: {lr_t:.6f}")

        # Restaurar los mejores pesos si la pérdida empeoró
        if best_weights is not None:
            for layer, best_w in zip(self.layers, best_weights):
                layer.weights = best_w

        total_end = time.time()
        print(f"Tiempo total de entrenamiento: {total_end - total_start:.2f} segundos")
        self.epoch_offset += epochs
        self.current_lr = lr_t





    def backward(self, loss_gradient, learning_rate):
        d_inputs = loss_gradient
        for layer in reversed(self.layers):
            d_inputs = layer.backward(d_inputs, learning_rate)


    def predict(self, X):
        return self.forward(X)






    def save(self, filename="model.h5"):
        with h5py.File(filename, "w") as f:
            for i, layer in enumerate(self.layers):
                grp = f.create_group(f"layer_{i}")
                weights_list = [cp.asnumpy(neuron.weights) for neuron in layer.neurons]
                bias_list = [float(neuron.bias) for neuron in layer.neurons]
                is_output_list = [bool(neuron.is_output) for neuron in layer.neurons]
                grp.create_dataset("weights", data=weights_list)
                grp.create_dataset("biases", data=bias_list)
                grp.create_dataset("is_output", data=cp.array(is_output_list).get().astype(bool))
            if self.loss_list:
                f.create_dataset("loss_list", data=self.loss_list)
            # Guardamos el estado de reanudación: epoch_offset y current_lr
            f.attrs["epoch_offset"] = self.epoch_offset
            f.attrs["current_lr"] = float(cp.asnumpy(self.current_lr))  # Convierte a float
        print(f"Modelo guardado en {filename}")

    def load(self, filename="model.h5"):
        with h5py.File(filename, "r") as f:
            temp_loss_list = f["loss_list"][()].tolist() if "loss_list" in f else []
            last_loss = temp_loss_list[-1] if temp_loss_list else float('inf')

            # Solo carga el modelo si su pérdida es menor que el actual
            if self.loss_list and last_loss > min(self.loss_list):
                print("⚠ El modelo guardado tiene una pérdida mayor. No se cargará.")
                return

            self.layers = []
            i = 0
            while f.get(f"layer_{i}") is not None:
                grp = f[f"layer_{i}"]
                weights = grp["weights"][()]
                biases = grp["biases"][()]
                is_output = grp.get("is_output", [False] * len(biases))

                num_neurons, input_size = weights.shape
                layer = Layer(num_neurons, input_size)
                for j, neuron in enumerate(layer.neurons):
                    neuron.weights = cp.array(weights[j])
                    neuron.bias = biases[j]
                    neuron.is_output = bool(is_output[j])
                self.layers.append(layer)
                i += 1

            self.loss_list = temp_loss_list
            self.epoch_offset = f.attrs.get("epoch_offset", 0)
            self.current_lr = f.attrs.get("current_lr", 0.01)

        print(f"Modelo cargado desde {filename}, última pérdida: {last_loss:.4f}")

