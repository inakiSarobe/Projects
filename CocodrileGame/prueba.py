from ursina import *

app = Ursina()

# Cargar la mano como una entidad principal
hand = Entity(model=load_model("Models/hand"), position=(0, 0, 0))


# Cargar un dedo como entidad separada
index_finger = Entity(model="Models/index_finger", parent=hand, position=(0.2, 0.5, 0), rotation=(0, 0, 0))

def update():
    # Rotar el dedo índice al presionar una tecla
    if held_keys["space"]:
        index_finger.rotation_x += 1

app.run()
