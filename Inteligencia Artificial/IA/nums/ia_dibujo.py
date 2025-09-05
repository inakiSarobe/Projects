import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageDraw, ImageOps, ImageFilter
import cupy as np
import os
from neural_network.neural_network import NeuralNetwork  # Asegúrate de que la ruta de importación sea correcta

# Ruta base donde se almacenan las imágenes de entrenamiento
TRAINING_DIR = "C:/Programacion/Practica/Python/IA/nums/datasets/numbers/mnist_png/train"

# Instancia de la red neuronal y carga del modelo
model = NeuralNetwork()
model.load("models/modelV1.h5")

class DrawingApp:
    def __init__(self, master):
        self.master = master
        master.title("Dibuja y predice")

        # Tamaño del lienzo
        self.canvas_width = 200
        self.canvas_height = 200

        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack()

        # Botón para predecir
        self.button_predict = tk.Button(master, text="Predecir", command=self.predict)
        self.button_predict.pack(pady=5)

        # Botones para indicar si la predicción fue correcta o incorrecta
        frame = tk.Frame(master)
        frame.pack(pady=5)
        self.button_correct = tk.Button(frame, text="Correcto", command=self.guardar_correcto, state=tk.DISABLED)
        self.button_correct.pack(side=tk.LEFT, padx=10)
        self.button_incorrect = tk.Button(frame, text="Incorrecto", command=self.guardar_incorrecto, state=tk.DISABLED)
        self.button_incorrect.pack(side=tk.RIGHT, padx=10)

        # Label para mostrar el resultado
        self.label_result = tk.Label(master, text="Resultado:")
        self.label_result.pack(pady=5)

        # Configurar eventos del mouse para dibujar
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.last_x, self.last_y = None, None

        # Crear imagen en memoria para guardar el dibujo
        self.image1 = Image.new("L", (self.canvas_width, self.canvas_height), "white")
        self.draw_obj = ImageDraw.Draw(self.image1)

        # Variable para almacenar la imagen procesada (28x28) y el dígito predicho
        self.processed_image = None
        self.predicted_digit = None

    def start_draw(self, event):
        self.last_x, self.last_y = event.x, event.y

    def draw(self, event):
        x, y = event.x, event.y
        if self.last_x is not None and self.last_y is not None:
            # Dibuja en el canvas
            self.canvas.create_line(self.last_x, self.last_y, x, y, width=8, fill='black', capstyle=tk.ROUND, smooth=True)
            # Dibuja en la imagen en memoria
            self.draw_obj.line([self.last_x, self.last_y, x, y], fill="black", width=8)
        self.last_x, self.last_y = x, y

    def preprocesar_imagen(self):
        """
        Procesa la imagen actual para que se parezca a las imágenes de entrenamiento:
          - Inversión de colores: fondo oscuro, dígito en blanco.
          - Suavizado y recorte.
          - Redimensionado y centrado en un lienzo de 28x28.
        Devuelve la imagen procesada (PIL.Image) y su arreglo normalizado.
        """
        image = self.image1.copy()

        # 1. Invertir la imagen para que el fondo sea oscuro y el trazo blanco
        image = ImageOps.invert(image)

        # 2. Aplicar un ligero desenfoque para suavizar
        image = image.filter(ImageFilter.GaussianBlur(radius=1))

        # 3. Recortar la imagen al área del dibujo
        bbox = image.getbbox()
        if bbox:
            image = image.crop(bbox)
        # Si no se detecta dibujo, se usará la imagen completa

        # 4. Redimensionar manteniendo la relación de aspecto y centrar en un canvas de 28x28
        new_image = Image.new("L", (28, 28), "black")
        image.thumbnail((20, 20), Image.LANCZOS)
        x_offset = (28 - image.width) // 2
        y_offset = (28 - image.height) // 2
        new_image.paste(image, (x_offset, y_offset))

        # 5. Normalización para la red: valores en [0,1]
        image_array = np.array(new_image).astype(np.float16) / 255.0
        image_array = image_array.flatten().reshape(1, -1)  # Forma: (1,784)

        return new_image, image_array

    def predict(self):
        # Preprocesar la imagen para la predicción
        self.processed_image, image_array = self.preprocesar_imagen()

        # Realizar la predicción
        predictions = model.predict(image_array)
        self.predicted_digit = int(np.argmax(predictions))
        self.label_result.config(text=f"Predicción: {self.predicted_digit}")

        # Habilitar los botones para indicar si es correcto o incorrecto
        self.button_correct.config(state=tk.NORMAL)
        self.button_incorrect.config(state=tk.NORMAL)

    def guardar_imagen(self, digit):
        """
        Guarda la imagen procesada (28x28) en la carpeta de entrenamiento,
        dentro del subdirectorio correspondiente (ej. 0 para el dígito 0).
        """
        # Construir la ruta de destino
        folder = os.path.join(TRAINING_DIR, f"{digit}")
        os.makedirs(folder, exist_ok=True)

        # Generar un nombre de archivo único (por ejemplo, contando los archivos ya existentes)
        num_files = len([name for name in os.listdir(folder) if name.endswith(".png")])
        filename = os.path.join(folder, f"img_{num_files + 1}.png")
        self.processed_image.save(filename)
        print(f"Imagen guardada en {filename}")

    def online_training(self, image_array, correct_digit):
        """
        Realiza una actualización online de la red utilizando el ejemplo actual.
        Se construye la etiqueta one-hot a partir del dígito correcto y se entrena 1 época con ese único ejemplo.
        """
        # Construir la etiqueta one-hot
        label = np.eye(10)[correct_digit].reshape(1, -1)
        # Entrenamiento online: 1 época, batch_size=1, con un learning_rate moderado
        model.train(image_array, label, epochs=1, initial_lr=1.0, batch_size=1000, eta_min=1e-5)
        print("Entrenamiento online realizado con el ejemplo corregido.")

    def guardar_correcto(self):
        # Si la predicción fue correcta, se guarda la imagen en la carpeta del dígito predicho
        self.guardar_imagen(self.predicted_digit)
        messagebox.showinfo("Guardado", "Imagen guardada como correcta.")
        self.limpiar_canvas()

    def guardar_incorrecto(self):
        # Solicitar al usuario el dígito correcto (como entero)
        respuesta = simpledialog.askinteger("Entrada", "Ingresa el dígito correcto (0-9):", minvalue=0, maxvalue=9)
        if respuesta is None:
            return  # El usuario canceló
        correct_digit = int(respuesta)
        # Guardar la imagen en la carpeta correspondiente al dígito correcto
        self.guardar_imagen(correct_digit)
        # Realizar una actualización online de la red con este ejemplo
        _, image_array = self.preprocesar_imagen()
        self.online_training(image_array, correct_digit)
        messagebox.showinfo("Guardado", "Imagen guardada como incorrecta y la red fue actualizada.")
        self.limpiar_canvas()

    def limpiar_canvas(self):
        """Reinicia el canvas y la imagen en memoria para comenzar un nuevo dibujo."""
        self.canvas.delete("all")
        self.image1 = Image.new("L", (self.canvas_width, self.canvas_height), "white")
        self.draw_obj = ImageDraw.Draw(self.image1)
        self.label_result.config(text="Resultado:")
        self.button_correct.config(state=tk.DISABLED)
        self.button_incorrect.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
