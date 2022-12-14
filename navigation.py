# Press ⌃R to execute it or replace it with your code.

import cv2 as cv
import numpy as np
import pyautogui


def navigate_gta(minimap):
    lower = np.array([130, 150, 0])
    upper = np.array([140, 200, 255])

    hsv = cv.cvtColor(minimap, cv.COLOR_RGB2HSV)
    mask = cv.inRange(hsv, lower, upper)

    # matches = np.argwhere(mask == 255)
    # mean_y = np.mean(matches[:, 1])
    # target = minimap.shape[1] / 2
    # error = target - mean_y

    # pyautogui.press('w')
    # if error > 0:
    #    pyautogui.press('a')
    # if error < 0:
    #    pyautogui.press('d')

    cv.imshow("Mask", mask)
    cv.waitKey(5)


def navigate_witcher(minimap):
    lower = np.array([100, 0, 215])
    upper = np.array([130, 150, 255])

    hsv = cv.cvtColor(minimap, cv.COLOR_RGB2HSV)
    mask = cv.inRange(hsv, lower, upper)

    matches = np.argwhere(mask == 255)
    mean_y = np.mean(matches[:, 1])
    target = minimap.shape[1] / 2
    error = target - mean_y

    # if error > .5:
    #    pyautogui.press('a')
    # if error < .5:
    #    pyautogui.press('d')
    # pyautogui.press('w')

    cv.imshow("Mask", mask)
    cv.waitKey(5)


def grab_map():
    gta = True

    if gta:
        capture = cv.VideoCapture('GTA-V_trimmed.mp4')
    else:
        capture = cv.VideoCapture('Witcher3-FAI.mp4')

    while True:
        # screen = pyautogui.screenshot()
        # screen = np.array(screen)
        success, frame = capture.read()
        if gta:
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            minimap = frame[850:1100, 0:320]
            player_location = minimap[120:180, 155:175]
            navigate_gta(player_location)
        else:
            minimap = frame[40:320, 1600:1880]
            player_location = minimap[100:180, 110:170]
            navigate_witcher(player_location)

        if cv.waitKey(20) & 0xFF == ord('q'):
            break

    capture.release()
    cv.destroyAllWindows()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    grab_map()
