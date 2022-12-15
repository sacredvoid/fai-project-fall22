from engine import Engine
import time

if __name__ == "__main__":
    engine = Engine(1920,1080)
    # First parameter is an array of button press and button release pair
    # Second parameter is an array of X,Y co-ordinate movement
    # engine.move_mouse([engine.input_controller.mouse_rb_press,engine.input_controller.mouse_rb_release],[300,300])
    time.sleep(4)
    engine.runner()