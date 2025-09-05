from ursina import *
from ursina.shaders import lit_with_shadows_shader
from PIL import Image
#numpy
import random
import math

app = Ursina()

# Game settings
GRID_SIZE = 20
SEGMENT_SPACING = 0.7  # Space between segments
MOVE_SPEED = 5
STARTING_LENGTH = 5
GROUND_SIZE = 20

# Game state
score = 0
game_over = False

# Create a window title
window.title = '3D Snake Game'
window.borderless = False
window.exit_button.visible = True

# Create skybox and lighting
Sky()
pivot = Entity()
DirectionalLight(parent=pivot, y=2, z=3, shadows=True, rotation=(45, -45, 45))

# Create the ground with checkered pattern
ground = Entity(
    model='plane',
    scale=GROUND_SIZE,
    texture='white_cube',
    collider='box',
    shader=lit_with_shadows_shader
)

# Crear una imagen de 2x2 píxeles con un patrón de ajedrez
image = Image.new('RGB', (2, 2), color=(0, 0, 0))
pixels = image.load()

# Game UI elements
score_text = Text(text="Score: 0", position=(-0.85, 0.45), scale=2)
game_over_text = Text(
    text="Game Over!\nClick to restart",
    origin=(0, 0),
    position=(0, 0),
    scale=3,
    color=color.red,
    visible=False
)

class SnakeSegment(Entity):
    def __init__(self, position, is_head=False):
        super().__init__(
            model='cube' if not is_head else 'sphere',
            color=color.lime if not is_head else color.green,
            position=position,
            scale=(0.8, 0.8, 0.8),
            shader=lit_with_shadows_shader
        )
        self.is_head = is_head
        self.target_position = position
        self.speed_multiplier = 1.0
        self.collider = 'box' if is_head else None  # Only head has collider for performance

class Food(Entity):
    def __init__(self):
        super().__init__(
            model='sphere',
            color=color.red,
            scale=0.8,
            shader=lit_with_shadows_shader,
            collider='sphere'
        )
        self.respawn()
    
    def respawn(self):
        # Position food randomly on the grid
        x = random.randint(-GRID_SIZE//2 + 2, GRID_SIZE//2 - 2)
        z = random.randint(-GRID_SIZE//2 + 2, GRID_SIZE//2 - 2)
        self.position = (x, 0.5, z)
        # Add a small animation
        self.animate_scale((0.8, 0.8, 0.8), duration=0.2, curve=curve.out_bounce)

class Snake:
    def __init__(self):
        self.segments = []
        self.positions_history = []
        self.direction = Vec3(1, 0, 0)
        self.speed = MOVE_SPEED
        self.growing = STARTING_LENGTH - 1  # Start with segments to grow
        self.create_head()
        self.last_position = self.head.position
        
        # Store positions for smooth following
        for i in range(100):  # History buffer
            self.positions_history.append(self.head.position)
    
    def create_head(self):
        self.head = SnakeSegment(Vec3(0, 0.5, 0), is_head=True)
        self.segments.append(self.head)
    
    def grow(self):
        # If already growing, increase counter
        self.growing += 1
    
    def add_segment(self):
        # Add a new segment at the end of the snake
        if len(self.segments) > 0:
            last_pos = self.segments[-1].position
            new_segment = SnakeSegment(Vec3(last_pos))
            self.segments.append(new_segment)
    
    def update(self):
        global game_over
        if game_over:
            return
        
        # Get direction from mouse position
        mouse_world_pos = mouse.position
        mouse_world_pos = Vec3(mouse_world_pos.x * GRID_SIZE/2, 0, mouse_world_pos.y * GRID_SIZE/2)
        
        target_direction = mouse_world_pos - self.head.position
        if target_direction.length() > 0.1:
            target_direction = target_direction.normalized()
            
            # Smooth direction change - interpolate current with target
            self.direction = lerp(self.direction, target_direction, time.dt * 5)
            self.direction = self.direction.normalized()
        
        # Move head
        new_pos = self.head.position + self.direction * time.dt * self.speed
        
        # Keep snake within boundaries
        boundary = GRID_SIZE/2 - 1
        new_pos.x = max(min(new_pos.x, boundary), -boundary)
        new_pos.z = max(min(new_pos.z, boundary), -boundary)
        new_pos.y = 0.5  # Keep y position constant
        
        # Update head position
        self.head.position = new_pos
        self.head.look_at(self.head.position + self.direction)
        
        # Update position history
        if (self.head.position - self.last_position).length() > 0.05:
            self.positions_history.insert(0, Vec3(self.head.position))
            self.positions_history.pop()
            self.last_position = Vec3(self.head.position)
            
        # Update body segments with smooth following and bending
        history_spacing = max(1, int(SEGMENT_SPACING * 10))  # Convert to indices in history
        
        for i, segment in enumerate(self.segments[1:], 1):
            history_index = min(i * history_spacing, len(self.positions_history) - 1)
            target_pos = self.positions_history[history_index]
            
            # Smooth movement toward target position
            segment.position = lerp(segment.position, target_pos, time.dt * 10 * segment.speed_multiplier)
            
            # Calculate direction to next segment for orientation
            if i < len(self.segments) - 1:
                look_dir = self.segments[i-1].position - segment.position
                if look_dir.length() > 0.1:
                    segment.look_at(self.segments[i-1].position)
            else:  # Last segment looks toward the segment in front
                look_dir = self.segments[i-1].position - segment.position
                if look_dir.length() > 0.1:
                    segment.look_at(self.segments[i-1].position)
        
        # Add new segment if growing
        if self.growing > 0 and len(self.segments) < 100:  # Limit max length
            self.add_segment()
            self.growing -= 1
        
        # Check for self-collision (head hitting body)
        for segment in self.segments[3:]:  # Skip first few segments to avoid false collisions
            if (self.head.position - segment.position).length() < 0.6:
                game_over = True
                game_over_text.visible = True
                break
    
    def reset(self):
        # Clear existing segments
        for segment in self.segments:
            destroy(segment)
        self.segments = []
        self.positions_history = []
        self.direction = Vec3(1, 0, 0)
        self.growing = STARTING_LENGTH - 1
        self.create_head()
        self.last_position = self.head.position
        
        # Reset position history
        for i in range(100):
            self.positions_history.append(self.head.position)

def reset_game():
    global game_over, score
    snake.reset()
    food.respawn()
    score = 0
    score_text.text = f"Score: {score}"
    game_over_text.visible = False
    game_over = False

def check_food_collision():
    global score
    if (snake.head.position - food.position).length() < 1.2:
        score += 1
        score_text.text = f"Score: {score}"
        food.respawn()
        snake.grow()
        # Speed up slightly with each food eaten
        snake.speed = min(MOVE_SPEED + score * 0.1, MOVE_SPEED * 2)

def update():
    if not game_over:
        snake.update()
        check_food_collision()
    
    # Game restart on click when game over
    if game_over and mouse.left:
        reset_game()

def input(key):
    if key == 'escape':
        application.quit()

# Create the snake and food
snake = Snake()
food = Food()

# Set up camera
camera.position = (0, 20, 0)
camera.rotation_x = 90
camera.orthographic = True
camera.fov = 20

# Optional: Uncomment to use custom model for snake
# To use a custom OBJ model, replace 'cube' with load_model('path/to/your/snake_model.obj')
# in the SnakeSegment class initialization

# Add instructions
instruction_text = Text(
    text="Move the snake with your mouse\nEat the red apples to grow",
    position=(0, -0.4),
    origin=(0, 0),
    color=color.white
)

# Instructions will fade out after a few seconds
instruction_text.animate_color(color.rgba(1, 1, 1, 0), duration=3, delay=5, curve=curve.linear)

app.run()