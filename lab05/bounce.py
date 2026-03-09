from pyray import *
from os.path import join
from pathlib import Path
from settings import *

THIS_DIR = Path(__file__).resolve().parent

class Jump():
    def __init__(self):
        self.pos = Vector2(200, GROUND)
        self.speed = 200 # 200 pixels/sec
        self.frame_rec = Rectangle(0.0, 0.0, float(SCARF_WIDTH)/6, float(SCARF_HEIGHT))

    def startup(self):
        self.texture = load_texture(str(THIS_DIR/"resources/scarfy.png"))

    def update(self):
        motion = Vector2(0, 0)

        if is_key_down(KeyboardKey.KEY_RIGHT):
            motion.x += 1
        if is_key_down(KeyboardKey.KEY_LEFT):
            motion.x += -1 

        motion_this_frame = vector2_scale(motion, get_frame_time() * self.speed) 
        self.pos = vector2_add(self.pos, motion_this_frame)

   
    def draw(self):
        draw_texture_rec(self.texture, self.frame_rec, self.pos, WHITE)
    
    def shutdown(self):
        unload_texture(self.texture)


class Ball():
    def __init__(self):
        self.position = Vector2(WINDOW_WIDTH * 7/8, 100)
        self.radius = 10
        self.gravity = 0.0
        self.velocity_y = 0.0
        self.time = 1.0
        self.elastic = 0.8

    def startup(self):
        self.gravity = -(2 * (WINDOW_HEIGHT - self.position.y)) / (self.time ** 2)

    def update(self):
        dt = get_frame_time()

        self.velocity_y += self.gravity * dt

        if self.position.y + self.radius >= WINDOW_HEIGHT:
            self.position.y = WINDOW_HEIGHT - self.radius
            self.velocity_y *= -self.elastic 

        self.position.y -= self.velocity_y * dt

        if is_key_pressed(KeyboardKey.KEY_UP) and self.elastic < 1.0:
            self.elastic += 0.05

        if is_key_pressed(KeyboardKey.KEY_DOWN) and self.elastic > 0.0:
            self.elastic -= 0.05

        if is_key_pressed(KeyboardKey.KEY_R):
            self.position.y = 100
            self.velocity_y = 0.0


    def draw(self):
        draw_circle_v(self.position, self.radius, PURPLE)
        draw_text(f"The coefficient e = {self.elastic}", 100, 200, 30, BLACK)
        draw_text("Press R to reset ball", 100, 300, 25, BLACK)

class Game():
    def __init__(self):
        self.jump = Jump()
        self.ball = Ball()

    def startup(self):
        self.jump.startup()
        self.ball.startup()
        
    def update(self):
        self.jump.update()
        self.ball.update()
 
    def draw(self):
        draw_fps(20, 20)
        self.jump.draw()
        self.ball.draw()

    def shutdown(self):
        self.jump.shutdown()