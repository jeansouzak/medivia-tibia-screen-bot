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
    def dragRuneToHand(blank, hand):        
        if not blank:
            return False

        pyautogui.moveTo(blank)
        if Action.DRAG_DURATION > 0:
            pyautogui.dragTo(hand, button='left', duration=Action.DRAG_DURATION)
            time.sleep(Action.DRAG_DURATION)
        else:
            pyautogui.mouseDown(button='left')
            pyautogui.moveTo(hand)
            pyautogui.mouseUp(button='left')
        return True
    
    @staticmethod
    def openInsideBackpack(inside_bp):        
        if not inside_bp:
            return False      
        
        pyautogui.rightClick(inside_bp)
        return True

    
    @staticmethod
    def conjureSpell(spell_name):        
        pyautogui.typewrite(spell_name)        
        keyboard.press_and_release('enter')
        

    @staticmethod
    def dragBackRune(blank, hand):        
        pyautogui.moveTo(hand)        
        if Action.DRAG_DURATION > 0:
            pyautogui.dragTo(blank, button='left', duration=Action.DRAG_DURATION)
            time.sleep(Action.DRAG_DURATION)
        else:
            pyautogui.mouseDown(button='left')
            pyautogui.moveTo(blank)
            pyautogui.mouseUp(button='left')                       

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