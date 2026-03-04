"""raylib [textures] example - Sprite animation
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 1.3, last time updated with raylib 1.3
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2014-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

from pyray import *
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

MAX_FRAME_SPEED = 15
MIN_FRAME_SPEED = 1
SCARFY = "resources/scarfy.png"
GIRL_RUNNING = "resources/girl_running.png"
HAMSTER = "resources/hamster.png"
SCARFY_FRAMES = 6
GIRL_RUNNING_FRAMES = 8
HAMSTER_FRAMES = 5


# Initialization
screenWidth = 800
screenHeight = 450

init_window(screenWidth, screenHeight, "raylib [texture] example - sprite anim")

# Important NOTE: Textures MUST be loaded after Window initialization 
# (OpenGL context is required)
# Texture loading: one step vs. two steps (see other example)
selected_sprite = load_texture(str(THIS_DIR/GIRL_RUNNING)) # change if need to load another sprite
sprite_frames = GIRL_RUNNING_FRAMES # change if need to load another sprite
scale = 1.0
if selected_sprite.width == 1024: scale = 0.75
if selected_sprite.width == 134: scale = 5.0
pos_x = 15 * scale
pos_y = 40


position = Vector2(350.0, 280.0)
frameRec = Rectangle(0.0, 0.0, float(selected_sprite.width)/sprite_frames, float(selected_sprite.height))
currentFrame = 0

framesCounter = 0
framesSpeed = 8  # Number of spritesheet frames shown by second

set_target_fps(60)  # Set our game to run at 60 frames-per-second

# Main game loop
while not window_should_close():  # Detect window close button or ESC key
    # Update
    framesCounter += 1

    if framesCounter >= (60/framesSpeed):
        framesCounter = 0
        currentFrame += 1

        if currentFrame > sprite_frames - 1:
            currentFrame = 0

        frameRec.x = float(currentFrame) * float(selected_sprite.width)/sprite_frames

    # Control frames speed
    if is_key_pressed(KeyboardKey.KEY_RIGHT):
        framesSpeed += 1
    elif is_key_pressed(KeyboardKey.KEY_LEFT):
        framesSpeed -= 1

    if framesSpeed > MAX_FRAME_SPEED:
        framesSpeed = MAX_FRAME_SPEED
    elif framesSpeed < MIN_FRAME_SPEED:
        framesSpeed = MIN_FRAME_SPEED

    # Draw
    begin_drawing()
    
    clear_background(RAYWHITE)
    
    draw_texture_ex(selected_sprite, Vector2(pos_x, pos_y), 0.0, scale, WHITE)
    draw_rectangle_lines(int(pos_x), pos_y, int(selected_sprite.width * scale), int(selected_sprite.height * scale), LIME)
    draw_rectangle_lines(int(pos_x + frameRec.x * scale), int(pos_y + frameRec.y * scale), 
                           int(frameRec.width * scale), int(frameRec.height * scale), RED)
    
    draw_text("FRAME SPEED: ", 165, 210, 10, DARKGRAY)
    draw_text(f"{framesSpeed:02d} FPS", 575, 210, 10, DARKGRAY)
    draw_text("PRESS RIGHT/LEFT KEYS to CHANGE SPEED!", 290, 240, 10, 
    DARKGRAY)
    
    for i in range(MAX_FRAME_SPEED):
        if i < framesSpeed:
            draw_rectangle(250 + 21*i, 205, 20, 20, RED)

    # Draw part of the texture
    draw_texture_pro(selected_sprite, frameRec, Rectangle(position.x, position.y, frameRec.width*scale, frameRec.height*scale), Vector2(0.0, 0.0), 0.0, WHITE)
    
    draw_text("(c) Scarfy sprite by Eiden Marsal", screenWidth - 200,
               screenHeight - 20, 10, GRAY)
    end_drawing()

# De-Initialization
unload_texture(selected_sprite)  # Texture unloading
close_window()  # Close window and OpenGL context