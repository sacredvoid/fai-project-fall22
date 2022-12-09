from screengrab import grab_screen
import cv2

for i in range(0,200):
    screen = grab_screen(region=(0,0,1920,1080))  # region will vary depending on game resolution and monitor resolution
    # print(screen)
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB) # because default will be BGR
    
    screen = cv2.resize(screen, (960,540))
    print(screen.argmax())
    cv2.imshow("window",screen)
    cv2.waitKey(10)