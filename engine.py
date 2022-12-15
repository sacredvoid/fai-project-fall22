# Method to pass keyboard inputs to the game (sentdex)
# Method to pass mouse inputs to the game (sentdex)
# Method to calculate where in the screen is the bounding box (generated from aakash) and calculate corrective outputs
# Method to calculate corrective action to take from Jack's outputs
# Method to keep the player on track for a global path goal - Jack
# Method to keep player on track for local path goal - Aakash
from capture_frame import CaptureFrame
from game_input import Keys
import time
from navigation import calculate_navigation_error
import math
from yolo_object_detection import getDetectedObjectsBox

class Engine:

    def __init__(self,width,height) -> None:
        self.width = width
        self.height = height
        self.screen_capture = CaptureFrame((0,0,width,height))
        self.input_controller = Keys()
        self.mouse_movement_steps = 100
        self.error_list = []
        self.region_split_coordinates()

    def region_split_coordinates(self):
        x_split = self.width / 3
        y_split = self.height / 3
        self.regions = []
        for i in range(0,3):
            current_y = y_split * i
            for j in range(0,3):
                current_x = x_split * j
                self.regions.append((current_x,current_y))
        
        print(self.regions)


    def _calculate_movement_steps(self, x:float,y:float) -> tuple:
        movement_time = 1 # in seconds
        dt = movement_time/self.mouse_movement_steps
        dx = x/self.mouse_movement_steps
        dy = y/self.mouse_movement_steps
        return dx,dy,dt

    def move_mouse(self, mouse_button=None, mouse_movement=None, duration:float = 0.5) -> None:
        if mouse_button is not None:
            self.input_controller.directMouse(buttons=mouse_button[0])
            time.sleep(duration)
            self.input_controller.directMouse(buttons=mouse_button[1])
        
        if mouse_movement is not None:
            move_x, move_y, move_t = self._calculate_movement_steps(mouse_movement[0],mouse_movement[1])
            for i in range(0,self.mouse_movement_steps):
                self.input_controller.directMouse(int(move_x), int(move_y))
                time.sleep(move_t)

    def keyboard_press(self, keyboard_button:str) -> None:
        self.input_controller.directKey(keyboard_button)
    
    def keyboard_release(self, keyboard_button:str) -> None:
        self.input_controller.directKey(keyboard_button, self.input_controller.key_release)


    def get_navigation_error(self):
        current_error = calculate_navigation_error(self.screen_capture.get_current_frame(),True)
        return current_error

    def runner(self):
        self.keyboard_press("w")
        for i in range(0,1000):
            total_correction = self.get_object_box_error()
            if(len(total_correction) == 0):
                total_correction = 0
            else:
                total_correction = sum(total_correction)
            current_nav_error = self.get_navigation_error()
            # for item in total_correction:
            #     self.error_list.append(item)
            # self.navigation_error_list.append(current_nav_error)
            # current_move = self.error_list.pop(0)
            total_correction += current_nav_error
            if(not math.isnan(current_nav_error)):
                if(current_nav_error > 0):
                    self.keyboard_release("w")
                    self.keyboard_press("s")
                    self.keyboard_press("a")
                    time.sleep(current_nav_error/100)
                    self.keyboard_release("a")
                    print("Key Pressed: A")
                    self.keyboard_release("s")
                    self.keyboard_press("w")
                
                else:
                    self.keyboard_release("w")
                    self.keyboard_press("s")
                    self.keyboard_press("d")
                    time.sleep(-current_nav_error/100)
                    self.keyboard_release("d")
                    self.keyboard_release("s")
                    self.keyboard_press("w")
                    print("Key Pressed: D")

                # elif(current_nav_error < -2):
                #     # self.keyboard_press("s")
                #     self.keyboard_press("d")
                #     time.sleep(-current_nav_error/100)
                #     self.keyboard_release("d")
                #     print("Key Pressed: D")
                #     # self.keyboard_release("s")

        self.keyboard_release("w")
    
    
    def isInsideBox(self,point):
        # self.region2_cords = (640,360,1280,0)
        self.region5_coords = (640,540,1280,0)
        
        if(point[0] > self.region5_coords[0] and point[0] < self.region5_coords[2] and point[1] < self.region5_coords[1] and point[1] > self.region5_coords[3]):
            return True
            
        else:
            return False

    def get_object_box_error(self):
        confidence, _, boxes = getDetectedObjectsBox(self.screen_capture.get_current_frame())
        # Region 2 and 5 are of importance
        # |_|x|_|
        # |_|x|_|
        # |_|_|_|
        
        total_correction = []
        print(confidence)
        print("Boxes***:",boxes)
        if (len(boxes) > 0):
            for box in boxes:
                overlap = self.isInsideBox(box[0:2])
                print(overlap)
                if(overlap):
                    overlap_extent = box[0] - 320 # x2-x1/2 = 1280-640/2 = 320
                    correction = overlap_extent/320 # normalizing
                    print(correction)
                    total_correction.append(correction)
        return total_correction