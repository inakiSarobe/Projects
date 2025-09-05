from ursina import *
import random

app = Ursina()

tooth_list_from_file = []
game_over_text = None
restart_button = None
exit_button = None

#class Hand:
#    hand_Entity = Entity(model="Models/hand", position=(0, 0, 0))
#hand = Hand()

class Cocodriles:
    cocodrile_Entity = Entity(model="Models/cocodrilo", position=(0, 0, 0), rotation_y=-90)
    cocodrile_Face_Entity = Entity(model="Models/cocodriloboca", position=(-0.78, -0.2, -1.2), rotation_y=-90)

cocodrile = Cocodriles()

class Tooths(Cocodriles):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.corrupto = False
        self.entity = Entity(model="Models/cocodrilodiente", position=(self.x, self.y, self.z), rotation_y=-90, collider='box')

    def corromper(self):
        self.corrupto = True

with open('tooth_positions.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if line:
            x, y, z = map(lambda s: float(s.strip()), line.split(','))
            tooth = Tooths(x, y, z)
            tooth_list_from_file.append(tooth)

def corromp_tooth():
    if tooth_list_from_file:
        numero_aleatorio = random.randint(0, len(tooth_list_from_file) - 1)
        tooth_list_from_file[numero_aleatorio].corromper()

def game_over():
    global game_over_text, restart_button, exit_button

    game_over_text = Text(
        text="Game Over!",
        position=(0, 0.3),
        scale=2,
        color=color.red,
        origin=(0, 0),
        background=True
    )

    restart_button = Button(
        text="Restart",
        color=color.green,
        position=(0, -0.1),
        scale=(0.2, 0.1),
        on_click=restart_game
    )

    exit_button = Button(
        text="Exit",
        color=color.red,
        position=(0, -0.25),
        scale=(0.2, 0.1),
        on_click=application.quit
    )

def restart_game():
    global game_over_text, restart_button, exit_button, tooth_list_from_file

    if game_over_text:
        destroy(game_over_text)
    if restart_button:
        destroy(restart_button)
    if exit_button:
        destroy(exit_button)

    for tooth in tooth_list_from_file:
        tooth.corrupto = False
        if tooth.entity is None:
            tooth.entity = Entity(model="Models/cocodrilodiente", position=(tooth.x, tooth.y, tooth.z), rotation_y=-90, collider='box')

def action(tooth):
    if tooth.corrupto:
        game_over()
    else:
        pass

def User_Touch():
    if mouse.hovered_entity:
        for tooth in tooth_list_from_file:
            if tooth.entity == mouse.hovered_entity:
                destroy(tooth.entity)
                tooth.entity = None
                action(tooth)
                break

def input(key):
    if key == 'left mouse down':
        User_Touch()
        corromp_tooth()

EditorCamera()
camera.position = Vec3(0, 0, 10)

app.run()
