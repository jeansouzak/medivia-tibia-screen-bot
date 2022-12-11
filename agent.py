import os
import datetime as dt
from action import Action
from item import Item
import pywinauto
import pyautogui
import time
pyautogui.FAILSAFE = False


class Agent:

    STOPPED = 0
    RUNNING = 1
    WAITING = 2
    FINISHED = 3
    hand = None
    food = None
    inside_backpack = None
    last_blank_pos = None
    #if client delay and rune not back to bp, try to remove from hand
    last_located_hand = None
    trash_container = None

    def __init__(self, index, game_window):        
        self.index = str(index)
        self.game_window = game_window
        if self.isValidConfig():            
            self.char_name = os.getenv('WINDOW_'+self.index)
            self.spell = os.getenv('SPELL_NAME_'+self.index)        
            self.mana_spent = float(os.getenv('MANA_SPENT_'+self.index))
            self.seconds_to_one_mana = float(os.getenv('SECONDS_TO_ONE_MANA_'+self.index))
            self.runes_to_craft = float(os.getenv('RUNES_TO_CRAFT_'+self.index))
            self.mana_train = os.getenv('MANA_TRAIN_'+self.index)
            self.time_to_spell = float(self.seconds_to_one_mana * self.mana_spent)
            self.last_running_time = dt.datetime.now()
            self.state = self.STOPPED
            self.has_blank = True
            self.total_mana_spent = 0
            self.total_rune_made = 0
            self.reconnect = os.getenv('RECONNECT')
            print([self.char_name, self.spell, self.mana_spent, self.mana_train, self.seconds_to_one_mana, 
            self.last_running_time, self.state, self.reconnect])
        else:                        
            pyautogui.alert('Burrão! \nConfigurações icorretas ['+str(index)+'].\nRefaça e comece novamente por favor', 'Atenção')
            self.game_window.kill()        
        

    def isValidConfig(self):

        if not isinstance(self.game_window, pywinauto.Application):
            return False

        if not self.index:
            return False

        if not (os.getenv('WINDOW_'+self.index) or os.getenv('SPELL_NAME_'+self.index)
                    or os.getenv('MANA_SPENT_'+self.index) or os.getenv('SECONDS_TO_ONE_MANA_'+self.index)
                    or os.getenv('MANA_TRAIN_'+self.index)):
            return False

        if not (self.representsInt(os.getenv('MANA_SPENT_'+self.index)) 
                or self.representsInt(os.getenv('RUNES_TO_CRAFT_'+self.index)) 
                or self.representsInt(os.getenv('SECONDS_TO_ONE_MANA_'+self.index))):
            return False    
        
            
        return True
    

    def isFinishToCraftRune(self):
        if self.total_rune_made <= self.runes_to_craft:
            print('Char '+self.char_name+' todas as runas solicitadas foram feitas')
            return True
        return False

    def isValidItems(self):
        try:            
            if not self.getFood():
                self.sendAlert('suas FOODS')
                return False
            return True
        except FileNotFoundError:
            pyautogui.alert('Existem arquivos de imagem faltante / nome errado, refaça e reinicie a configuração', 'Atenção')
            return False
            
    def sendAlert(self, obj):
        pyautogui.alert('Não consegui encontrar '+obj+' , refaça e reinicie a configuração', 'Atenção')

    def representsInt(self, s):
        try: 
            int(s)
            return True
        except ValueError:
            return False
     
    def getFood(self):     
        return pyautogui.locateOnScreen(Item.image_path + '/food.png', grayscale=True)
    
    def getMediviaLoginScreen(self):
        return pyautogui.locateOnScreen(Item.image_path + '/medivia.png', grayscale=True)


    def focus(self):        
        #app_dialog = self.game_window.top_window()        
        #app_dialog.wrapper_object().set_focus()        
        #pyautogui.moveTo(x,y)
        #pywinauto.application.Application().connect(process=self.game_window.process).top_window().set_focus()
        #time.sleep(0.5)                
        app_dialog = self.game_window.top_window()   
        app_dialog.set_focus()
        

    def run(self):
        self.state = self.RUNNING                
        if self.canSpell():
            self.focus()
            self.throws()

    def die(self):
        self.game_window.kill()
                            

    def canSpell(self):        
        now = dt.datetime.now()
        spentTime = (now-self.last_running_time).total_seconds()                
        return self.state != self.FINISHED and spentTime >= self.time_to_spell
    
    def wasDisconneted(self):
        if self.reconnect == 'true' and self.state != self.FINISHED:
            loginScreen = self.getMediviaLoginScreen()            
            if loginScreen:
                print('Char '+self.char_name+' foi desconectado por algum motivo, reconectando...')
                Action.login()
                time.sleep(2)
                return True
        return False

    def throws(self):
        self.last_running_time = dt.datetime.now()
        if self.mana_train == 'true':
            Action.conjureSpell(os.getenv('SPELL_NAME_'+self.index))
            self.total_mana_spent += self.mana_spent
            food = self.getFood()
            if not food and self.wasDisconneted() == False:
                print('Char '+self.char_name+' sem food e conectado, deslogando')
                self.state = self.FINISHED            
                Action.logout()
                self.game_window.kill()
                return 0      
            else:
                Action.eatFood(self.getFood())
                self.state = self.WAITING
                print(self.char_name+': Trabalho feito, aguardando mana')                
        else:           
            Action.conjureSpell(os.getenv('SPELL_NAME_'+self.index))            
            self.total_rune_made += 1
            self.total_mana_spent += self.mana_spent             
            food = self.getFood()
            if self.wasDisconneted() == False and (not self.isFinishToCraftRune() or not food):
                print('Char '+self.char_name+' sem food ou com quantidade de runas feitas, deslogando')
                self.state = self.FINISHED            
                Action.logout()
                self.game_window.kill()
                return 0      
            else:
                Action.eatFood(self.getFood())
                self.state = self.WAITING
                print(self.char_name+': Trabalho feito, aguardando mana')

 