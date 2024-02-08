import time
import pyautogui
import cv2
import numpy as np
from Pieces import Load_buttons, Read_deck, handler


#     '''From left to right'''
Location_coordinates = [(793, 654), (956, 654), (1150, 654)]
width, height = pyautogui.size()
print("screen resolution: " + str(width) + "x " + str(height))
Red_button_array, Play_button_array, Reconnect_array, Collect_button_array, Next_button_array, turn_tupo_list = Load_buttons(
    'C:/Users/acer/Pictures/Snap/Snap button')
image_list = Read_deck("C:/Users/acer/Pictures/Snap/Discard deck/Cards")

Turn1_card_tupo = (1, ['Sunspot', 'Blade'])
Turn2_card_tupo = (2, ['Sunspot', 'Blade', 'Wolverine'])
Turn3_card_tupo = (3, ['Lady', 'Sunspot', 'Blade', 'Wolverine'])
Turn4_card_tupo = (4, ['Jubilee', 'Dracula', 'Ghost', 'Sunspot', 'Blade', 'Wolverine'])
Turn5_card_tupo = (5, ['Spider Woman', 'Jubilee', 'Dracula', 'Ghost Rider', 'Sunspot', 'Blade', 'Wolverine'])
Turn6_card_tupo = (6, ['Hela', 'Hulk', 'AmericaChavez', 'Spider Woman', 'Jubilee', 'Dracula', 'Ghost Rider', 'Sunspot',
                       'Blade', 'Wolverine'])
card_tupo_list = [Turn1_card_tupo, Turn2_card_tupo, Turn3_card_tupo, Turn4_card_tupo, Turn5_card_tupo, Turn6_card_tupo]

right_x, right_y = 1267, 957

while True:
    for times in range(10):
        time.sleep(1)
        screenshot_gray = pyautogui.screenshot().convert("L")
        screenshot_gray_array = np.array(screenshot_gray)
        result = cv2.matchTemplate(screenshot_gray_array, Play_button_array, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        threshold = 0.8
        if max_val > 0.8:
            pyautogui.click(max_loc)
            print("Play button found, match started.")
            time.sleep(8)
            break

    value = handler(turn_tupo_list, card_tupo_list, height, width, right_x, right_y)
    if value == 00:
        print("At top loop ready to recontinue in 5.")
        time.sleep(2)
        continue

    if value == "Finished":
        time.sleep(2)
        continue


