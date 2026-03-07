from pyray import *
from os.path import join
from pathlib import Path
from settings import *

THIS_DIR = Path(__file__).resolve().parent

class Picker():
    def __init__(self):
        self.pos = Vector2(640, GROUND)

    def update(self):
        if is_mouse_button_released(MOUSE_BUTTON_LEFT):
            self.pos = get_mouse_position()

    def draw(self):
        draw_circle_v(self.pos, 10, RED)

class Jump():
    def __init__(self):
        self.pos = Vector2(640, GROUND)
        self.speed = 200 # 200 pixels/sec
        self.grounded = True # would jump
        self.frame_rec = Rectangle(0.0, 0.0, float(SCARF_WIDTH)/6, float(SCARF_HEIGHT))
        self.velocity_y = 0.0 
        self.gravity = 0.0
        self.friction = 1.01
        self.calibrate_time = True
        self.calibrate_x = False
        self.time = 0.5

    def startup(self):
        # be careful path: how you run?>
        self.texture = load_texture(str(THIS_DIR/"resources/scarfy.png"))

    def update(self, picker):
        motion = Vector2(0, 0)

        draw_text(str(self.gravity), 20, 50, 20, BLACK)
        draw_text(str(self.velocity_y), 20, 80, 20, BLACK)

        if is_key_down(KeyboardKey.KEY_RIGHT):
            motion.x += 1
        if is_key_down(KeyboardKey.KEY_LEFT):
            motion.x += -1 
        
        if is_key_pressed(KeyboardKey.KEY_SPACE) and self.grounded:
            if self.calibrate_time:
                self.calculate_gravity_t(picker.pos.y)
                self.calculate_velocity_yt(picker.pos.y)
            if self.calibrate_x:
                self.calculate_velocity_x(picker.pos)
                self.calculate_gravity_yx(picker.pos)

            self.grounded = False
        
        if not self.grounded:
            self.velocity_y += self.gravity * get_frame_time()
            self.pos.y -= self.velocity_y * get_frame_time()
        
        if self.pos.y >= GROUND:
            self.pos.y = GROUND
            self.grounded = True
            self.velocity_y = 0.0
        else:
            self.grounded = False

        motion_this_frame = vector2_scale(motion, get_frame_time() * self.speed)
    
        self.pos = vector2_add(self.pos, motion_this_frame)

        if is_key_pressed(KeyboardKey.KEY_C):
            self.calibrate_time = not self.calibrate_time
            self.calibrate_x = False
        if is_key_pressed(KeyboardKey.KEY_X):
            self.calibrate_x = not self.calibrate_x
            self.calibrate_time = False
        
        if self.calibrate_time:
            if is_key_pressed(KeyboardKey.KEY_LEFT_BRACKET) and self.time > 0.1:
                self.time -= 0.1
            if is_key_pressed(KeyboardKey.KEY_RIGHT_BRACKET):
                self.time += 0.1
 
   
    def draw(self):
        draw_texture_rec(self.texture, self.frame_rec, self.pos, WHITE)

        if self.calibrate_time:
            draw_text("Time: " + str(self.time), 60, 60, 20, BLACK)
    
    def shutdown(self):
        unload_texture(self.texture)

    def calculate_velocity_yt(self, height):
        self.velocity_y = (2 * (WINDOW_HEIGHT - height)) / self.time

    def calculate_gravity_t(self, height):
        self.gravity = -(2 * (WINDOW_HEIGHT - height)) / (self.time ** 2)

    def calculate_velocity_x(self, pos):
        #is 12 because the texture is 6 frames long and need to find the x position in the middle of one of them
        self.velocity_y = 2 * (WINDOW_HEIGHT - pos.y) * (self.speed) / abs(pos.x - (self.pos.x + self.texture.width/12))

    def calculate_gravity_yx(self, pos):
        self.gravity = -2 * (WINDOW_HEIGHT - pos.y) * ( self.speed ** 2) / (pos.x - (self.pos.x + self.texture.width/12)) ** 2


class Game():
    def __init__(self):
        self.jump = Jump()
        self.picker = Picker()

    def startup(self):
        self.jump.startup()
        
    def update(self):
        self.picker.update()
        self.jump.update(self.picker)
 
    def draw(self):
        draw_fps(20, 20)
        self.jump.draw()
        self.picker.draw()

    def shutdown(self):
        self.jump.shutdown()