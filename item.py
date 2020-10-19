import os
import pyautogui
pyautogui.FAILSAFE = False


class Item:

    image_path = os.getenv('IMAGES_PATH')