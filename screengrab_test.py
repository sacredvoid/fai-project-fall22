from screengrab import grab_screen
import cv2

for i in range(0,200):
    screen = grab_screen(region=(0,0,1920,1080))  # region will vary depending on game resolution and monitor resolution
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB) # because default will be BGR
    screen = cv2.resize(screen, (960,540))
    x_split = int(960/3)
    y_split = int(540/3)
    region1 = screen[0:y_split,0:x_split]
    region2 = screen[0:y_split,x_split:x_split*2]
    region3 = screen[0:y_split,x_split*2:x_split*3]
    region4 = screen[y_split:y_split*2,0:x_split]
    region5 = screen[y_split:y_split*2,x_split:x_split*2]
    region6 = screen[y_split:y_split*2,x_split*2:x_split*3]
    region7 = screen[y_split*2:y_split*3,0:x_split]
    region8 = screen[y_split*2:y_split*3,x_split:x_split*2]
    region9 = screen[y_split*2:y_split*3,x_split*2:x_split*3]
    screen_split = 1
    cv2.imshow("window",region8)
    cv2.waitKey(10)