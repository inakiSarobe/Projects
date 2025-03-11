from ursina import *

def load_game():
    global rubik_entity
    rubik_entity = Entity()
    for x in range(3):
        for y in range(3):
            for z in range(3):
                cubie = Entity(
                    model='Model/Rubik',
                    texture='Textures/CubeAll',
                    rotation_x=-90,
                    rotation_y=-90,
                    rotation_z=0,
                    scale=0.95,
                    position=(x, y, z),
                    collider='box'
                )
                cubies.append(cubie)

def detectar_caras(cubie):
    x, y, z = cubie.position
    faces = []

    if x == 0:
        faces.append('izquierda')
    if x == 2:
        faces.append('derecha')
    if y == 0:
        faces.append('abajo')
    if y == 2:
        faces.append('arriba')
    if z == 0:
        faces.append('frente')
    if z == 2:
        faces.append('atras')
    return faces

def movimiento(cara, direccion):
    if direccion == 'izquierda':
        angulo = -90
    elif direccion == 'derecha':
        angulo = 90
    else:
        return

    if 'frente' in (cara if isinstance(cara, list) else [cara]):
        piezas = [c for c in cubies if round(c.position.z) == 0]
        pivot = Entity(parent=rubik_entity, position=Vec3(1, 1, 2))
        
        for pieza in piezas:
            pieza.world_parent = pivot
        pivot.animate('rotation_z', pivot.rotation_z + angulo, duration=0.5)

        def finish_rotation():
            for pieza in piezas:
                pieza.world_parent = rubik_entity
                pieza.position = Vec3(round(pieza.x), round(pieza.y), round(pieza.z))
            destroy(pivot)
        invoke(finish_rotation, delay=0.6)

    elif 'atras' in (cara if isinstance(cara, list) else [cara]):
        piezas = [c for c in cubies if round(c.position.z) == 2]
        pivot = Entity(parent=rubik_entity, position=Vec3(1, 1, 0))

        for pieza in piezas:
            pieza.world_parent = pivot
        pivot.animate('rotation_z', pivot.rotation_z + angulo, duration=0.5)

        def finish_rotation():
            for pieza in piezas:
                pieza.world_parent = rubik_entity
                pieza.position = Vec3(round(pieza.x), round(pieza.y), round(pieza.z))
            destroy(pivot)
        invoke(finish_rotation, delay=0.6)

    elif 'arriba' in (cara if isinstance(cara, list) else [cara]):
        piezas = [c for c in cubies if round(c.position.y) == 2]
        pivot = Entity(parent=rubik_entity, position=Vec3(1, 2, 1))
        
        for pieza in piezas:
            pieza.world_parent = pivot
        pivot.animate('rotation_y', pivot.rotation_y + angulo, duration=0.5)

        def finish_rotation():
            for pieza in piezas:
                pieza.world_parent = rubik_entity
                pieza.position = Vec3(round(pieza.x), round(pieza.y), round(pieza.z))
            destroy(pivot)
        invoke(finish_rotation, delay=0.6)

    elif 'abajo' in (cara if isinstance(cara, list) else [cara]):
        piezas = [c for c in cubies if round(c.position.y) == 0]
        pivot = Entity(parent=rubik_entity, position=Vec3(1, 0, 1))

        for pieza in piezas:
            pieza.world_parent = pivot
        pivot.animate('rotation_y', pivot.rotation_y + angulo, duration=0.5)

        def finish_rotation():
            for pieza in piezas:
                pieza.world_parent = rubik_entity
                pieza.position = Vec3(round(pieza.x), round(pieza.y), round(pieza.z))
            destroy(pivot)
        invoke(finish_rotation, delay=0.6)

    elif 'izquierda' in (cara if isinstance(cara, list) else [cara]):
        piezas = [c for c in cubies if round(c.position.x) == 0]
        pivot = Entity(parent=rubik_entity, position=Vec3(0, 1, 1))
        
        for pieza in piezas:
            pieza.world_parent = pivot
        pivot.animate('rotation_x', pivot.rotation_x + angulo, duration=0.5)

        def finish_rotation():
            for pieza in piezas:
                pieza.world_parent = rubik_entity
                pieza.position = Vec3(round(pieza.x), round(pieza.y), round(pieza.z))
            destroy(pivot)
        invoke(finish_rotation, delay=0.6)

    elif 'derecha' in (cara if isinstance(cara, list) else [cara]):
        piezas = [c for c in cubies if round(c.position.x) == 2]
        pivot = Entity(parent=rubik_entity, position=Vec3(2, 1, 1))
        
        for pieza in piezas:
            pieza.world_parent = pivot
        pivot.animate('rotation_x', pivot.rotation_x + angulo, duration=0.5)

        def finish_rotation():
            for pieza in piezas:
                pieza.world_parent = rubik_entity
                pieza.position = Vec3(round(pieza.x), round(pieza.y), round(pieza.z))
            destroy(pivot)
        invoke(finish_rotation, delay=0.6)

def determinar_cara_Seleccionada(cubie):
    x, y, z = cubie.position
    faces = detectar_caras(cubie)

    if 'frente' in faces and mouse.world_point[2] < z:
        return 'frente'
    elif 'atras' in faces and mouse.world_point[2] > z:
        return 'atras'
    elif 'arriba' in faces and mouse.world_point[1] > y:
        return 'arriba'
    elif 'abajo' in faces and mouse.world_point[1] < y:
        return 'abajo'
    elif 'izquierda' in faces and mouse.world_point[0] < x:
        return 'izquierda'
    elif 'derecha' in faces and mouse.world_point[0] > x:
        return 'derecha'
    
    return faces[0]

def input(key):
    global cara_seleccionada, posicion_inicial_mouse

    if key == 'left mouse down':
        if mouse.hovered_entity:
            caras = detectar_caras(mouse.hovered_entity)
            if caras:
                cara_seleccionada = determinar_cara_Seleccionada(mouse.hovered_entity)
                posicion_inicial_mouse = mouse.position

    elif key == 'left mouse up':
        if cara_seleccionada:
            delta_x = mouse.position[0] - posicion_inicial_mouse[0]
            delta_y = mouse.position[1] - posicion_inicial_mouse[1]

            if abs(delta_x) > abs(delta_y):
                direccion = 'derecha' if delta_x > 0 else 'izquierda'
            else:
                direccion = 'derecha' if delta_y > 0 else 'izquierda'
            movimiento(cara_seleccionada, direccion)
        cara_seleccionada = None

app = Ursina()
window.fullscreen = True
window.borderless = False
EditorCamera()
cara_seleccionada = None
posicion_inicial_mouse = None
camera.world_position = (0, 0, -15)
model, texture = 'Model/Rubik', 'Textures/CubeAll'
cubies = []
load_game()

if __name__ == "__main__":
    app.run()

