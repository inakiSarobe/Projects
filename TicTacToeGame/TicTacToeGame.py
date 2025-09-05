from ursina import *

app = Ursina()

center_position = Vec3(0, 1, 0)

game_over_text = None
restart_button = None
exit_button = None
cell_width = 8.5
cell_depth = 7.95
hitboxes = []
piecesO = [] 
piecesX = []
pieceX = 0
pieceO = 0
boolean = False
selected_piece = None 
turno_actual = True
movimiento_realizado = False

def mostrar_game_over(winner):
    global game_over_text, restart_button, exit_button

    game_over_text = Text(
        text=f"Game Over. {winner} wins!",
        position=(0, 0.3),
        scale=2,
        color=color.white,
        origin=(0, 0),
        background=True,
        background_color=color.black
    )

    restart_button = Button(
        text="Restart",
        color=color.green,
        position=(0, -0.1),
        scale=(0.2, 0.1),
        on_click=reiniciar_juego
    )

    exit_button = Button(
        text="Exit",
        color=color.red,
        position=(0, -0.25),
        scale=(0.2, 0.1),
        on_click=application.quit
    )

def reiniciar_juego():
    global game_over_text, restart_button, exit_button
    global pieceX, pieceO, selected_piece, turno_actual, movimiento_realizado
    global hitboxes, piecesX, piecesO

    destroy(game_over_text)
    destroy(restart_button)
    destroy(exit_button)

    for hitbox in hitboxes:
        destroy(hitbox)
    for piece, _ in piecesX:
        destroy(piece)
    for piece, _ in piecesO:
        destroy(piece)

    pieceX = 0
    pieceO = 0
    selected_piece = None
    turno_actual = True
    movimiento_realizado = False

    hitboxes.clear()
    piecesX.clear()
    piecesO.clear()

    for i in range(3):
        for j in range(3):
            offset = Vec3((i - 1) * cell_width, 0, (j - 1) * cell_depth)
            hitbox = Entity(
                model='quad',
                scale=(8.5, 7.95),
                position=center_position + offset,
                color=color.rgba(255, 255, 255, 0.1),
                rotation_x=90,
                collider='box'
            )
            hitbox.occupied = False
            hitboxes.append(hitbox)

base = Entity(
    model='Models/base',
    texture='Textures/wood',
    rotation_x=-0,
    rotation_y=-0,
    rotation_z=0,
    scale=1,
    position=(0, 0, 0),
    collider='box'
)

supp = Entity(
    model='Models/supp',
    texture='Textures/black',
    rotation_x=-0,
    rotation_y=-0,
    rotation_z=0,
    scale=1,
    position=(0, 1.2, 0),
    collider='box'
)

center_position = base.world_position + Vec3(-0.95, 1.5, 0.05)
cell_width = 8.5
cell_depth = 7.95

for i in range(3):
    for j in range(3):
        offset = Vec3((i - 1) * cell_width, 0, (j - 1) * cell_depth)
        hitbox = Entity(
            model='quad',
            scale=(8.5, 7.95),
            position=center_position + offset,
            color=color.rgba(255, 255, 255, 0),
            rotation_x=90,
            collider='box'
        )
        hitboxes.append(hitbox)

        hitbox.occupied = False

def verificar_ganador():
    combinaciones_ganadoras = [
        [hitboxes[0], hitboxes[1], hitboxes[2]],
        [hitboxes[3], hitboxes[4], hitboxes[5]],
        [hitboxes[6], hitboxes[7], hitboxes[8]],
        [hitboxes[0], hitboxes[3], hitboxes[6]],
        [hitboxes[1], hitboxes[4], hitboxes[7]],
        [hitboxes[2], hitboxes[5], hitboxes[8]],
        [hitboxes[0], hitboxes[4], hitboxes[8]],
        [hitboxes[2], hitboxes[4], hitboxes[6]],
    ]

    for combinacion in combinaciones_ganadoras:
        jugadores = [obtener_jugador_de_hitbox(hitbox) for hitbox in combinacion]
        if None not in jugadores and jugadores.count(jugadores[0]) == len(jugadores):
            mostrar_game_over(jugadores[0])
            return True
    return False


def obtener_jugador_de_hitbox(hitbox):
    for piece, piece_hitbox in piecesX:
        if piece_hitbox == hitbox:
            return "X"
    for piece, piece_hitbox in piecesO:
        if piece_hitbox == hitbox:
            return "O"
    return None

def interruptor(turno_actual):
    return not turno_actual



def input(key):
    global pieceX, pieceO, selected_piece, turno_actual, movimiento_realizado
    
    if key == "left mouse down":
        if movimiento_realizado:
            turno_actual = interruptor(turno_actual)
            movimiento_realizado = False
        
        if turno_actual == False:
            for piece, piece_hitbox in piecesO:
                if piece.hovered:
                    selected_piece = piece
                    return

            for hitbox in hitboxes:
                if hitbox.hovered:
                    if hitbox.occupied:
                        for piece, piece_hitbox in piecesO:
                            if piece_hitbox == hitbox:
                                selected_piece = piece
                                return
                    
                    elif selected_piece:
                        selected_piece.position = hitbox.position + Vec3(0, 0, 0.1)
                        for i, (p, h) in enumerate(piecesO):
                            if p == selected_piece:
                                piecesO[i] = (selected_piece, hitbox)
                        
                        for old_hitbox in hitboxes:
                            if old_hitbox.occupied and old_hitbox != hitbox:
                                if any(p[1] == old_hitbox for p in piecesO):
                                    continue
                                old_hitbox.occupied = False
                        hitbox.occupied = True
                        hitbox.jugador = "O"
                        selected_piece = None
                        movimiento_realizado = True
                        if verificar_ganador():
                            return
                        return

                    elif pieceO < 3:
                        pieceO += 1
                        piece = Entity(model='Models/o', texture='Textures/wood', scale=1, position=hitbox.position + Vec3(0, 0, 0.1), collider='box')
                        hitbox.occupied = True
                        hitbox.jugador = "O"
                        piecesO.append((piece, hitbox))
                        movimiento_realizado = True
                        if verificar_ganador():
                            return
                        return
        else:
            for piece, piece_hitbox in piecesX:
                if piece.hovered:
                    selected_piece = piece
                    return

            for hitbox in hitboxes:
                if hitbox.hovered:
                    if hitbox.occupied:
                        for piece, piece_hitbox in piecesX:
                            if piece_hitbox == hitbox:
                                selected_piece = piece
                                return
                    
                    elif selected_piece:
                        selected_piece.position = hitbox.position + Vec3(0, 0, 0.1)
                        for i, (p, h) in enumerate(piecesX):
                            if p == selected_piece:
                                piecesX[i] = (selected_piece, hitbox)
                        
                        for old_hitbox in hitboxes:
                            if old_hitbox.occupied and old_hitbox != hitbox:
                                if any(p[1] == old_hitbox for p in piecesX):
                                    continue
                                old_hitbox.occupied = False
                        hitbox.occupied = True
                        hitbox.jugador = "X"
                        selected_piece = None
                        movimiento_realizado = True
                        if verificar_ganador():
                            return
                        return

                    elif pieceX < 3:
                        pieceX += 1
                        piece = Entity(model='Models/x', texture='Textures/wood', scale=1, position=hitbox.position + Vec3(0, 0, 0.1), collider='box')
                        hitbox.occupied = True
                        hitbox.jugador = "X"
                        piecesX.append((piece, hitbox))
                        movimiento_realizado = True
                        if verificar_ganador():
                            return
                        return

window.fullscreen = False
window.borderless = False
camera.position = center_position + Vec3(0, 90, 80)
camera.look_at(center_position)
app.run()