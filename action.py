import pyautogui
import keyboard
import os
import time

pyautogui.PAUSE = 1.4
pyautogui.FAILSAFE = False


class Action:
   
    DRAG_DURATION = float(os.getenv('DRAG_TIME'))
    TIME_SLEEP = float(os.getenv('SLEEP_ACTION'))

    
    @staticmethod
    def conjureSpell(spell_name):        
        pyautogui.typewrite(spell_name)        
        keyboard.press_and_release('enter')
        
    @staticmethod
    def eatFood(food):        
        pyautogui.moveTo(food)        
        pyautogui.click(button='right', clicks=6, interval=0.30)        

    @staticmethod
    def logout():
        keyboard.press_and_release('ctrl+q')
    
    @staticmethod
    def login():
        keyboard.press_and_release('enter')