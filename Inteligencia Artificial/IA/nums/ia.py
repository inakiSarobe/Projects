import os
import random
import time, math
import h5py
import cupy as cp
import matplotlib.pyplot as plt
from PIL import Image
from neural_network.neural_network import NeuralNetwork

# CONFIGURACIÓN DE LA INTERFAZ DE IMÁGENES
IMAGES_PER_PAGE = 100
GRID_SIZE = (10, 10)

def show_images():
    """Muestra una página de imágenes con etiquetas reales y predicciones IA en la misma figura."""
    for ax in axes.flatten():
        ax.cla()  # Limpiar cada eje
    start = current_page * IMAGES_PER_PAGE
    end = min(start + IMAGES_PER_PAGE, total_images)
    for ax, idx in zip(axes.flatten(), range(start, end)):
        img_cpu = X[idx].get().reshape(28, 28)
        real_label = y[idx].get().argmax()
        ax.imshow(img_cpu, cmap="gray")
        ax.set_title(f"Real: {real_label} | IA: {predicted_digits[idx]}", fontsize=8)
        ax.axis("off")
    plt.suptitle(f"Página {current_page+1}/{pages}")
    plt.draw()
    plt.pause(0.1)

def on_key(event):
    """Permite cambiar de página con las flechas izquierda y derecha."""
    global current_page
    if event.key == "right":
        current_page = (current_page + 1) % pages
    elif event.key == "left":
        current_page = (current_page - 1) % pages
    show_images()

def load_images_and_labels(directory, samples_per_class):
    """Carga imágenes y etiquetas de forma aleatoria de cada carpeta."""
    images, labels = [], []
    for root, _, files in os.walk(directory):
        if not files:
            continue
        if len(files) >= samples_per_class:
            selected_files = random.sample(files, samples_per_class)
        else:
            selected_files = files
        label_str = os.path.basename(root)
        try:
            label = int(label_str)
        except ValueError:
            print(f"⚠ No se pudo extraer la etiqueta de {root}")
            continue
        for file in selected_files:
            if file.endswith('.png'):
                filepath = os.path.join(root, file)
                img = Image.open(filepath).convert('L')
                img_array = cp.array(img).reshape(-1) / 255.0  # Normalización usando cupy
                images.append(img_array)
                labels.append(label)
    return cp.array(images), cp.array(labels)

def one_hot_encode(labels, num_classes):
    return cp.eye(num_classes)[labels]

#############################################
# BLOQUE PRINCIPAL
#############################################
if __name__ == "__main__":
    train_directory = "C:/Programacion/Practica/Python/IA/nums/datasets/numbers/mnist_png/train"

    # Cargar imágenes y etiquetas
    X, y = load_images_and_labels(train_directory, samples_per_class=500)
    y = one_hot_encode(y, num_classes=10)

    # Variables de paginación (para visualización)
    total_images = int(X.shape[0])
    pages = (total_images + IMAGES_PER_PAGE - 1) // IMAGES_PER_PAGE
    current_page = 0

    # Cargar o crear modelo
    model_path = "models/modelV1.h5"
    nn = NeuralNetwork()
    if os.path.exists(model_path):
        print("Cargando modelo existente...")
        nn.load(model_path)
    else:
        print("Creando un nuevo modelo...")
        nn.add_layer(num_neurons=256, input_size=784)
        nn.add_layer(num_neurons=10, input_size=256, is_output=True)

    # Entrenar el modelo. Se reanuda desde el estado guardado.
    # Parámetros: epochs, initial_lr, batch_size, eta_min
    nn.train(X, y, epochs=100, initial_lr=1.0, batch_size=1000, eta_min=1e-5)
    nn.save(model_path)

    # Realizar predicciones
    predictions = nn.predict(X)
    predicted_digits = cp.asnumpy(cp.argmax(predictions, axis=1))
    true_digits = cp.asnumpy(cp.argmax(y, axis=1))

    # Mostrar imágenes en una sola figura que se actualiza
    fig, axes = plt.subplots(GRID_SIZE[0], GRID_SIZE[1], figsize=(12, 12), 
                             gridspec_kw={'hspace': 0.5, 'wspace': 0.5})
    fig.canvas.mpl_connect("key_press_event", on_key)
    show_images()
    plt.show()

    # Mostrar gráfica de pérdida
    plt.figure()
    plt.plot(nn.loss_list)
    plt.xlabel("Época")
    plt.ylabel("Pérdida")
    plt.title("Evolución de la pérdida durante el entrenamiento")
    plt.show()

    # Calcular tasa de error
    error_rate = cp.mean(cp.array(predicted_digits) != cp.array(true_digits))
    print(f"Tasa de error: {error_rate * 100:.2f}%")
