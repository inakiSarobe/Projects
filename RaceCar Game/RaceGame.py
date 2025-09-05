from ursina import *
import math, time

app = Ursina()

path_points = []
camera.position = (0, 300, 0)
camera.rotation_x = 90

# Variables de movimiento y estado

current_lap_start = 0
off_track_penalty = 0
game_over = False

# HUD
class Hud:
    speed_text = Text(text="", position=(-0.7, 0.45), scale=2)
    status_text = Text(text="", position=(-0.7, 0.4), scale=2, color=color.green)
    lap_text = Text(text="Lap: 0", position=(-0.7, 0.35), scale=2)
    time_text = Text(text="Time: 0.0s", position=(-0.7, 0.3), scale=2)
    best_lap_text = Text(text="", position=(-0.7, 0.25), scale=2)
    corner_text = Text(text="", position=(0, 0.45), scale=2, origin=(0, 0))

    instructions = Text(
        text="W = Acelerar\nS = Frenar\nSi doblas muy rápido, presiona R para reiniciar",
        position=(0.6, 0.4),
        scale=2
    )

    section_names = [
        "Start/Finish", "Sainte Devote", "Beau Rivage", "Massenet", "Casino",
        "Mirabeau Haute", "Grand Hotel Hairpin", "Portier", "Tunnel", 
        "Nouvelle Chicane", "Tabac", "Swimming Pool", "La Rascasse", 
        "Anthony Noghes", "Final Straight"
    ]
HudObj = Hud()
HudObj.speed_text.text = "Speed: Normal"

# Load models with error handling
track = Entity(model='Models/monaco', texture='white_cube')

class Car_Class:
        try:
            car = Entity(model='Models/indy_car', y=2.5, scale=1.5)
        except Exception as e:
            print(f"Error loading car model: {e}")
            car = Entity(model='cube', scale=(4.5, 1.5, 7.25), color=color.red, y=2.5)
        car_normal_speed = 60
        car_progress = 0
        car_fast_speed = 100
        car_low_speed = 30
        lap_count = 0

carObj = Car_Class()
car_speed = carObj.car_normal_speed


def initialize_monaco_path():
    global path_points
    # Definición de puntos clave (2D: x y z se representa en (x, z))
# Puntos colocados manualmente
    track_points = [
        (-45.86, -32.23),
        (-46.18, -30.00),
        (-46.20, -28.75),
        (-45.94, -27.35),
        (-45.54, -25.68),
        (-45.43, -23.72),
        (-44.77, -21.20),
        (-43.58, -15.87),
        (-42.81, -11.22),
        (-42.29, -8.26),
        (-41.64, -4.16),
        (-40.70, -0.61),
        (-39.32, 2.37),
        (-37.95, 5.37),
        (-35.72, 8.51),
        (-33.62, 10.94),
        (-31.94, 12.94),
        (-31.10, 14.52),
        (-29.69, 15.24),
        (-27.99, 15.38),
        (-26.70, 14.66),
        (-25.41, 13.51),
        (-22.57, 12.80),
        (-20.15, 12.51),
        (-18.02, 12.08),
        (-16.32, 11.94),
        (-13.90, 11.22),
        (-11.77, 10.65),
        (-9.08, 9.93),
        (-7.09, 9.65),
        (-3.54, 9.08),
        (0.85, 9.08),
        (2.27, 8.93),
        (4.54, 8.36),
        (7.23, 8.08),
        (9.92, 7.79),
        (12.90, 7.65),
        (17.00, 7.08),
        (19.27, 6.65),
        (22.24, 6.36),
        (25.07, 6.79),
        (26.65, 8.65),
        (27.23, 10.08),
        (28.38, 12.22),
        (29.25, 13.94),
        (28.98, 15.24),
        (28.00, 16.81),
        (27.31, 18.54),
        (27.90, 21.13),
        (29.49, 24.01),
        (30.95, 26.90),
        (31.67, 28.06),
        (33.54, 29.51),
        (35.11, 29.51),
        (36.54, 29.80),
        (37.99, 30.96),
        (39.00, 31.98),
        (40.02, 33.28),
        (41.74, 33.86),
        (45.03, 34.44),
        (46.74, 33.72),
        (48.14, 32.12),
        (49.96, 29.80),
        (51.07, 27.92),
        (51.06, 26.90),
        (50.33, 26.04),
        (49.73, 24.16),
        (49.13, 22.43),
        (49.81, 20.70),
        (50.50, 19.11),
        (51.63, 18.97),
        (52.77, 18.97),
        (53.63, 19.55),
        (54.93, 20.27),
        (56.94, 21.13),
        (59.94, 21.71),
        (61.50, 21.71),
        (62.76, 20.55),
        (63.28, 18.40),
        (63.24, 16.24),
        (62.77, 14.09),
        (62.03, 12.51),
        (61.00, 11.08),
        (59.27, 9.51),
        (57.83, 8.22),
        (55.95, 6.65),
        (54.37, 4.94),
        (52.93, 3.94),
        (51.21, 2.66),
        (49.21, 1.09),
        (47.35, 0.24),
        (45.08, -0.89),
        (41.95, -2.17),
        (38.12, -3.31),
        (35.72, -3.73),
        (33.04, -3.45),
        (28.94, -3.31),
        (25.84, -3.16),
        (21.75, -2.88),
        (18.64, -2.74),
        (15.82, -2.88),
        (13.70, -2.88),
        (11.72, -2.17),
        (9.60, -2.17),
        (8.33, -2.46),
        (7.48, -3.02),
        (6.07, -3.16),
        (4.09, -3.31),
        (3.11, -2.46),
        (2.40, -1.04),
        (0.71, -0.04),
        (0.00, 0.10),
        (-2.12, 1.09),
        (-4.95, 1.81),
        (-7.92, 2.23),
        (-10.33, 2.37),
        (-13.72, 2.37),
        (-16.55, 1.95),
        (-19.51, 1.38),
        (-21.35, 1.24),
        (-24.31, -0.04),
        (-25.01, -0.75),
        (-27.54, -2.60),
        (-28.65, -4.44),
        (-29.33, -6.85),
        (-28.75, -8.82),
        (-27.47, -9.53),
        (-27.75, -10.38),
        (-28.30, -11.65),
        (-28.42, -13.90),
        (-28.82, -16.01),
        (-29.07, -19.24),
        (-29.06, -20.50),
        (-29.18, -22.60),
        (-29.72, -24.98),
        (-31.10, -26.79),
        (-32.49, -27.21),
        (-34.45, -27.77),
        (-35.42, -28.47),
        (-36.65, -30.56),
        (-37.46, -33.34),
        (-36.73, -36.11),
        (-35.45, -38.05),
        (-33.89, -39.71),
        (-31.77, -42.06),
        (-32.04, -43.58),
        (-34.39, -44.96),
        (-37.03, -45.24),
        (-40.37, -45.51),
        (-44.83, -45.10),
        (-45.97, -43.17),
        (-46.85, -40.54),
        (-47.02, -38.47),
        (-47.06, -35.84),
        (-46.13, -32.78),
    ]

    
    # Interpolación para suavizar la curva (20 puntos entre cada par clave)
    for i in range(len(track_points)-1):
        p1 = track_points[i]
        p2 = track_points[i+1]
        steps = 20
        for j in range(steps):
            t = j / steps
            x = p1[0] + (p2[0] - p1[0]) * t
            z = p1[1] + (p2[1] - p1[1]) * t
            path_points.append((x, z))

# Funciones de cálculo de dirección y curvatura (sin cambios)
def get_path_direction(progress):
    idx = int(progress) % len(path_points)
    next_idx = (idx + 1) % len(path_points)
    current = path_points[idx]
    next_point = path_points[next_idx]
    dx = next_point[0] - current[0]
    dz = next_point[1] - current[1]
    length = math.sqrt(dx*dx + dz*dz)
    if length > 0:
        return dx/length, dz/length
    return 0, 0

def calculate_curvature(progress):
    idx = int(progress) % len(path_points)
    prev_idx = (idx - 5) % len(path_points)
    next_idx = (idx + 5) % len(path_points)
    p1 = path_points[prev_idx]
    p2 = path_points[idx]
    p3 = path_points[next_idx]
    v1 = (p2[0] - p1[0], p2[1] - p1[1])
    v2 = (p3[0] - p2[0], p3[1] - p2[1])
    dot_product = v1[0]*v2[0] + v1[1]*v2[1]
    mag1 = math.sqrt(v1[0]**2 + v1[1]**2)
    mag2 = math.sqrt(v2[0]**2 + v2[1]**2)
    if mag1 * mag2 == 0:
        return 0
    cos_angle = dot_product / (mag1 * mag2)
    cos_angle = max(-1, min(1, cos_angle))
    curvature = 1 - abs(cos_angle)
    return curvature

def is_speed_safe_for_curve(speed, curve_sharpness):
    # Definí límites seguros según la curvatura:
    # Si la curva es muy cerrada (>0.7), la velocidad segura es baja (p.ej. 50)
    # Curvas moderadas y suaves se pueden recorrer a mayor velocidad.
    if curve_sharpness > 0.7 and speed > carObj.car_low_speed:
        return False
    if curve_sharpness > 0.5 and speed > carObj.car_normal_speed:
        return False
    if curve_sharpness > 0.3 and speed > carObj.car_fast_speed:
        return False
    return True

def get_current_section(progress):
    section_idx = int((progress / len(path_points)) * len(HudObj.section_names))
    return HudObj.section_names[min(section_idx, len(HudObj.section_names)-1)]

# Función para reiniciar el juego
def reset_game():
    global car_speed, current_lap_start, off_track_penalty, game_over
    game_over = False
    carObj.car_progress = 0
    car_speed = carObj.car_normal_speed
    carObj.lap_count = 0
    current_lap_start = time.time()
    off_track_penalty = 0
    HudObj.speed_text.text = "Speed: Normal"
    HudObj.status_text.text = "On track"
    HudObj.lap_text.text = "Lap: 0"
    HudObj.time_text.text = "Time: 0.0s"
    HudObj.best_lap_text.text = "Best: ---"

"""
# Opcional: dibujar la ruta para debug
def draw_debug_path():
    path_parent = Entity()
    for i in range(len(path_points)):
        p = path_points[i]
        if i % 20 == 0:
            marker_color = color.yellow
            marker_size = 1.5
        else:
            marker_color = color.rgba(255, 255, 0, 100)
            marker_size = 0.8
        Entity(model='sphere', scale=marker_size, position=(p[0], 0.5, p[1]),
               color=marker_color, parent=path_parent)
    # Marcas de texto para puntos importantes
    corners = [
        ((0, 0, 0), "Start"),
        ((-50, 0, -15), "Sainte Devote"),
        ((-140, 0, 50), "Massenet"),
        ((-110, 0, 80), "Casino"),
        ((-10, 0, 50), "Hairpin"),
        ((30, 0, -30), "Tunnel"),
        ((0, 0, -80), "Chicane"),
        ((-90, 0, -80), "Pool"),
        ((-120, 0, -60), "Rascasse")
    ]
    for pos, txt in corners:
        Text(text=txt, parent=path_parent, scale=10, position=pos, billboard=True)
"""

def input(key):
    print("Tecla presionada:", key)
    global car_speed, game_over
    
    # Lógica de aceleración y frenado (solo si el juego está activo)
    if not game_over:
        if key == 'w':
            print(car_speed)
            if car_speed == carObj.car_normal_speed:
                car_speed = carObj.car_fast_speed
                print(HudObj.speed_text.text)
                HudObj.speed_text.text = "Speed: Fast"
                print(HudObj.speed_text.text)
            elif car_speed == carObj.car_low_speed:
                car_speed = carObj.car_normal_speed
                print(HudObj.speed_text.text)
                HudObj.speed_text.text = "Speed: Normal"
                print(HudObj.speed_text.text)
            elif car_speed == carObj.car_fast_speed:
                print(HudObj.speed_text.text)
                HudObj.speed_text.text = "Speed: Fast"
                print(HudObj.speed_text.text)
                pass
            print("usuario apreta W")
        if key == 's':
            print("usuario apreta S")
            if car_speed == carObj.car_normal_speed:
                car_speed = carObj.car_low_speed
                print(HudObj.speed_text.text)
                HudObj.speed_text.text = "Speed: Slow"
                print(HudObj.speed_text.text)
            elif car_speed == carObj.car_fast_speed:
                car_speed = carObj.car_normal_speed
                print(HudObj.speed_text.text)
                HudObj.speed_text.text = "Speed: Normal"
                print(HudObj.speed_text.text)
            elif car_speed == carObj.car_low_speed:
                print(HudObj.speed_text.text)
                HudObj.speed_text.text = "Speed: Slow"
                print(HudObj.speed_text.text)
                pass
    
    # Lógica de reinicio
    if game_over and key == 'r':
        reset_game()
        HudObj.status_text.color = color.green

# Función de actualización (update)
def update():
    global car_speed, current_lap_start, off_track_penalty, game_over
    
    # Si se activó game_over, no se actualiza nada
    if game_over:
        return
    
    # Avanzar el progreso a lo largo del camino
    old_progress = carObj.car_progress
    carObj.car_progress += car_speed * time.dt  # Factor ajustable para la escala del trazado

    # Verificar final de vuelta
    if int(old_progress) < len(path_points) and int(carObj.car_progress) >= len(path_points):
        carObj.lap_count += 1
        lap_time = time.time() - current_lap_start
        current_lap_start = time.time()
        HudObj.lap_text.text = f"Lap: {carObj.lap_count}"

    while carObj.car_progress >= len(path_points):
        carObj.car_progress -= len(path_points)
    
    # Actualizar tiempo de vuelta
    current_time = time.time() - current_lap_start
    HudObj.time_text.text = f"Time: {current_time:.2f}s"
    
    # Obtener posición actual a partir del camino
    idx = int(carObj.car_progress) % len(path_points)
    next_idx = (idx + 1) % len(path_points)
    fraction = carObj.car_progress - int(carObj.car_progress)
    current = path_points[idx]
    next_point = path_points[next_idx]
    
    carObj.car.x = current[0] + (next_point[0] - current[0]) * fraction
    carObj.car.z = current[1] + (next_point[1] - current[1]) * fraction
    #car.y = 2.5  # Mantener el auto sobre el circuito

    direction = get_path_direction(carObj.car_progress)
    carObj.car.look_at(Vec3(carObj.car.x + direction[0], carObj.car.y, carObj.car.z + direction[1]))
    carObj.car.rotation_z = 0

    current_section = get_current_section(carObj.car_progress)
    HudObj.corner_text.text = f"Section: {current_section}"
    
    # Verificar si el auto va demasiado rápido para la curva actual
    curvature = calculate_curvature(carObj.car_progress)
    if not is_speed_safe_for_curve(car_speed, curvature):
        # Si el usuario no reduce la velocidad, se activa game_over
        game_over = True
        HudObj.status_text.text = "Too fast on curve! You crashed!\nPress R to restart."
        HudObj.status_text.color = color.red

# Inicializar la ruta y dibujar la pista de debug (opcional)
initialize_monaco_path()
current_lap_start = time.time()

app.run()
