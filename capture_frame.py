from screengrab import grab_screen
from collections import deque

class CaptureFrame():

    def __init__(self, screen_region) -> None:
        self.screen_region = screen_region
        # self.frame_queue = deque(maxlen=2);
        
    def get_current_frame(self):
        # current_frame_data = grab_screen(self.screen_region)
        return grab_screen(self.screen_region)