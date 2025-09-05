from ursina import *

app = Ursina()

# Clase base para el cocodrilo y su cara.
class Cocodriles:
    cocodrile_Entity = Entity(model="Models/cocodrilo", position=(0, 0, 0), rotation_y=-90)
    cocodrile_Face_Entity = Entity(model="Models/cocodriloboca", position=(-0.78, -0.2, -1.2), rotation_y=-90)

# Clase para los dientes, hereda de Cocodriles.
class Tooths(Cocodriles):
    def __init__(self, x, y, z):
        self.entity = Entity(model="Models/cocodrilodiente", position=(x, y, z), rotation_y=-90)

# Lista para almacenar los dientes creados.
tooth_list = []

# Creamos un plano con collider para poder obtener la posición del mouse sobre él.
plane = Entity(model='plane', scale=(10,10,15), collider='box', visible=False)

def input(key):
    # Al presionar el click izquierdo.
    if key == 'left mouse down':
        # mouse.world_point devuelve la posición en el mundo donde el mouse intersecta un collider.
        pos = mouse.world_point
        if pos is not None:
            new_tooth = Tooths(pos.x, pos.y, pos.z)
            tooth_list.append(new_tooth)
            print(f"Diente colocado en: {pos}")
        else:
            print("No se pudo obtener la posición del mouse.")
    
    # Al presionar la tecla 'g' se guardan las posiciones en un archivo.
    if key == 'g':
        with open('tooth_positions.txt', 'w') as f:
            for tooth in tooth_list:
                p = tooth.entity.position
                f.write(f"{p.x}, {p.y}, {p.z}\n")
        print("Posiciones guardadas en 'tooth_positions.txt'.")

# Configuración de la cámara.
EditorCamera()
camera.position = Vec3(0, 0, 10)

app.run()
