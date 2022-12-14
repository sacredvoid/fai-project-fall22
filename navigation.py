# Press ⌃R to execute it or replace it with your code.

import cv2 as cv
import numpy as np


def navigate_gta(minimap):
    lower = np.array([130, 150, 0])
    upper = np.array([140, 200, 255])

    hsv = cv.cvtColor(minimap, cv.COLOR_RGB2HSV)
    mask = cv.inRange(hsv, lower, upper)

    matches = np.argwhere(mask == 255)
    mean_y = np.mean(matches[:, 1])
    target = minimap.shape[1] / 2
    error = target - mean_y
    cv.imshow("Mask", mask)
    cv.waitKey(5)
    return error

    # pyautogui.press('w')
    # if error > 0:
    #    pyautogui.press('a')
    # if error < 0:
    #    pyautogui.press('d')


def navigate_witcher(minimap):
    lower = np.array([100, 0, 215])
    upper = np.array([130, 150, 255])

    hsv = cv.cvtColor(minimap, cv.COLOR_RGB2HSV)
    mask = cv.inRange(hsv, lower, upper)

    matches = np.argwhere(mask == 255)
    mean_y = np.mean(matches[:, 1])
    target = minimap.shape[1] / 2
    error = target - mean_y
    cv.imshow("Mask", mask)
    cv.waitKey(5)
    return error
    # if error > .5:
    #    pyautogui.press('a')
    # if error < .5:
    #    pyautogui.press('d')
    # pyautogui.press('w')


def calculate_navigation_error(incoming_frame, game_flag):
    gta = game_flag
    frame = incoming_frame
    if gta:
        minimap = frame[850:1100, 0:320]
        player_location = minimap[120:180, 155:175]
        return navigate_gta(player_location)
    else:
        minimap = frame[40:320, 1600:1880]
        player_location = minimap[100:180, 110:170]
        return navigate_witcher(player_location)