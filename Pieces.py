from PIL import Image
import pyautogui
import cv2
import numpy as np
import os




def Load_buttons(path):
    red_button_array = None
    play_button_array = None
    collect_button_array = None
    retreat_button_array = None
    turn1next_button_array = None
    target_list = os.listdir(path)
    print(target_list)
    button_paths = []
    for target in target_list:
        if 'Red' in target:
            Red_button_array = cv2.imread(path + "/" + target, cv2.IMREAD_GRAYSCALE)
        if 'Play' in target:
            print("Play found.")
            Play_array = cv2.imread(path + "/" + target, cv2.IMREAD_GRAYSCALE)
        if 'Reconnect' in target:
            Reconnect_array = cv2.imread(path + "/" + target, cv2.IMREAD_GRAYSCALE)
        if 'Collect' in target:
            Collect_array = cv2.imread(path + "/" + target, cv2.IMREAD_GRAYSCALE)
        if 'Next' in target:
            Next_array = cv2.imread(path + "/" + target, cv2.IMREAD_GRAYSCALE)

        if 'Turn1' in target:
            Turn1_tupo = (1, cv2.imread(path + "/" + target, cv2.IMREAD_GRAYSCALE))
        if 'Turn2' in target:
            Turn2_tupo = (2, cv2.imread(path + "/" + target, cv2.IMREAD_GRAYSCALE))
        if 'Turn3' in target:
            Turn3_tupo = (3, cv2.imread(path + "/" + target, cv2.IMREAD_GRAYSCALE))
        if 'Turn4' in target:
            Turn4_tupo = (4, cv2.imread(path + "/" + target, cv2.IMREAD_GRAYSCALE))
        if 'Turn5' in target:
            Turn5_tupo = (5, cv2.imread(path + "/" + target, cv2.IMREAD_GRAYSCALE))
        if 'End' in target:
            Final_turn_tupo = (6, cv2.imread(path + "/" + target, cv2.IMREAD_GRAYSCALE))
    Turn_tupo = [Turn1_tupo, Turn2_tupo, Turn3_tupo, Turn4_tupo, Turn5_tupo, Final_turn_tupo]
    return Red_button_array, Play_array, Reconnect_array, Collect_array, Next_array, Turn_tupo



def Read_deck(path):
    target_list = os.listdir(path)
    image_list = []
    for filename in target_list:
        image_path = path + "/" + filename
        image_array = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        image_list.append((filename, image_array))
    print("Load images: ")
    print([x[0] for x in image_list])
    return image_list


def if_red_button_appear005(height, width):
    screenshot = pyautogui.screenshot(region=(0, height // 3 * 2, width, height // 3)).convert("L")
    screenshot_array = np.asarray(screenshot)
    result = cv2.matchTemplate(screenshot_array, Red_button_array, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val > 0.8:
        pyautogui.click(max_loc)
        time.sleep(1)
        print("Red_button clicked")

def if_collect_rewards_3s():
    screenshot = pyautogui.screenshot().convert("L")
    screenshot_array = np.asarray(screenshot)

    result = cv2.matchTemplate(screenshot_array, Reconnect_array, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val > 0.8:
        print("Reconnct button found")
        pyautogui.click(max_loc)
        time.sleep(0.4)
        pyautogui.click(max_loc)
        time.sleep(5)
        return 11

    result = cv2.matchTemplate(screenshot_array, Play_button_array, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val > 0.8:
        print("Directly Play button found")
        return 00

    result = cv2.matchTemplate(screenshot_array, Next_button_array, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val > 0.8:
        print("Directly found Next.")
        pyautogui.click(max_loc)
        pyautogui.click(max_loc)
        return 00
    result = cv2.matchTemplate(screenshot_array, Collect_button_array, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val > 0.8:
        print("Found collect.")
        pyautogui.click(max_loc)
        pyautogui.click(max_loc)
        time.sleep(1)
        for second in range(15):
            time.sleep(1)
            screenshot = pyautogui.screenshot().convert("L")
            screenshot_array = np.asarray(screenshot)
            result = cv2.matchTemplate(screenshot_array, Next_button_array, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if max_val > threshold:
                print("Found Next.")
                pyautogui.click(max_loc)
                return 00

    return "No collect Found."

def detect_turn(turn_tupo, threshold, height, width):
    count = 0
    while True:
        screenshot = pyautogui.screenshot().convert("L")
        screenshot_array = np.array(screenshot)
        count += 1
        time.sleep(0.1)
        if count > 90:
            image = Image.fromarray(screenshot_array)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            image.save(f"faliure recongize: {timestamp}.png")
            return "Turn found failure, screenshot saved."

        result = cv2.matchTemplate(screenshot_array, turn_tupo[1], cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val > threshold:
            if turn_tupo[0] == 1:
                time.sleep(6)
                print("Turn 1 found.")
                return True
            else:
                print(f'Turn {str(turn_tupo[0])} found.')
                print('Sleep 1s.')
                time.sleep(3)
                return True

        value = if_collect_rewards_3s()
        if value == 00:
            print("Found value 0000000 detect_turn returning Next button Clicked and need to go out loop ")
            return 00
        if value == 11:
            print("Reconnecting to the game. Wait 5s.")
            return 11
        if_red_button_appear005(height, width)


def card_founction(card_turn_list_tupo, card_threshold, height, width, right_x, right_y):
    screenshot = pyautogui.screenshot(region=(0, height // 3 * 2, width, height // 3)).convert("L")
    screenshot_array = np.asarray(screenshot)
    for cardname in card_turn_list_tupo[1]:
        for image_name_tupo in image_list:
            if cardname in image_name_tupo[0]:
                if_red_button_appear005(height, width)
                result = cv2.matchTemplate(screenshot_array, image_name_tupo[1], cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                if max_val > threshold:
                    print("Found card " + cardname + " at " + str(card_turn_list_tupo[0]))
                    max_top_left_coordinates = max_loc
                    max_top_left_coordinates_full_screen = (
                    max_top_left_coordinates[0], max_top_left_coordinates[1] + 2 * height // 3)
                    pyautogui.moveTo(max_top_left_coordinates_full_screen[0], max_top_left_coordinates_full_screen[1])
                    pyautogui.mouseDown(button='left')
                    coordinates = random.choice(Location_coordinates)
                    time.sleep(0.5)
                    pyautogui.moveTo(coordinates[0], coordinates[1])
                    pyautogui.mouseUp()
                    time.sleep(1)
                    print(cardname + " being put out.")

    pyautogui.click(right_x, right_y)
    time.sleep(0.4)
    pyautogui.click(right_x, right_y)
    print("Cards round finished.")
    time.sleep(3)


def handler(turn_tupo_list, card_tupo_list, height, width, right_x, right_y):
    for x in range(1, 20):
        if x > 6:
            x = 6

        for turn_tupo in turn_tupo_list:
            if x == turn_tupo[0]:
                value = detect_turn(turn_tupo, 0.9, height, width)
                if value == True:
                    print("True, breaking to get to card reconginition")
                    break
                if value == 00:
                    print(
                        "this is value from handler and returining to to top of the program mean the next button is clicked")
                    return 00
                if value == "Turn found failure, screenshot saved.":
                    print("Turn image capture failure. Continue cards detect and play after 8s. Screenshot saved.")
                if value == 11:
                    break
        for card_tupo in card_tupo_list:
            if x == card_tupo[0]:
                card_founction(card_tupo, 0.7, height, width, right_x, right_y)

    return "Finished"