RubikGame is a game developed using the Ursina Engine, marking my first experience with this library. The controls are as follows:

Left Click (hold): Dragging the mouse left or right moves the face in which the pointer is located, in the direction of the pointer's movement.
Right Click: Allows camera movement using a fixed point.
Middle Mouse Button (mouse wheel button): Enables free camera movement.
Mouse Wheel: Zooms the camera in or out.
The current implementation contains some issues, including:

Incorrect calculation of the proximity between the Cubie faces and the pointer.
Some faces rotate in the opposite direction of the pointer/mouse movement.
There is no RESET key implemented.
Planned improvements include:

Randomization: Implementing a randomization feature to scramble the Rubik's Cube.
Help and Solution Buttons: Adding "Help" and "Solution" buttons.
The Help button will display a single 3D arrow, indicating which direction to rotate the face.
The Solution button will display a 3D arrow that updates after each move, guiding the player step-by-step until the Rubik’s Cube is solved.

# Ursina Setup Instructions

RECOMMEND:

// 1. Open CMD (Windows) or Terminal (macOS).

// 2. Navigate to the 'RubikGame' directory:
cd /path/to/RubikGame

// 3. Create a virtual environment (Works for both Windows and macOS):
python -m venv venv

// 4. Activate the environment: - Windows:
venv\Scripts\activate

    - macOS:
    source venv/bin/activate

// 5. Install Ursina Engine:
pip install ursina

// 6. Deactivate the environment when done:
deactivate
