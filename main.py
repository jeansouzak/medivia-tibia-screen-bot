import settings
from agent import Agent
import keyboard
import time
import os
import pywinauto
from pynput import keyboard
import threading
from PIL import Image
import sys
import pyautogui
pyautogui.FAILSAFE = False


agents = []
run = 0


def generateAgents():    
    agent_number = int(os.getenv('AGENT_NUMBER'))
    medivia_path = os.getenv('MEDIVIA_PATH')
    

    i = 1
    while i <= agent_number:
        app = pywinauto.Application().start(r'{}'.format(medivia_path))
        print(app.process)        
        agents.append(Agent(i, app))
        i += 1

def hasAgentRunning():
    global run
    for agent in agents:
        if agent.state == Agent.RUNNING:
            return True
    if len(agents) == 0:
        run = 0
    return False


def pause():
    print('Vou dar uma pausadinha amigão')
    global run
    run = 0


def die(icon = None):
    pyautogui.alert('Adeus, até a proxima', 'Tchau')
    print('Adeus amigão, espero que eu tenha lhe ajudado')
    global run
    run = 0
    change_state.stop()
    #For icon tray
    if icon:
        icon.visible = False
        icon.stop()
    sys.exit()

def isValidItems():
    for agent in agents:
        if not agent.isValidItems():
            print('Configuração de imagens / itens errados ['+str(agent.char_name)+']')            
            return False

    return True


def start():
    global run    
    print('Vamos la!')        
    run = 1
    threading.Thread(target = init).start()    

def init():
    global run
    lock = threading.Lock()    
    while run:
        total_mana_spent = 0
        total_rune_made = 0
        changed = False
        with lock:
            for agent in agents:
                if not hasAgentRunning() and agent.canSpell():
                    print('Agent '+agent.char_name+' preparado para fazer')
                    agent.run()
                    changed = True
                    total_mana_spent += agent.total_mana_spent
                    total_rune_made += agent.total_rune_made
                    if agent.state == Agent.FINISHED:
                        print('Agent '+agent.char_name+' removido por falta de blank ou food')
                        agents.remove(agent)
        if changed:
            print('Total de runas feitas: '+str(total_rune_made))
            print('Total de mana gasta: '+str(total_mana_spent))

        time.sleep(1)

def reboot(): 
    generateAgents()
    start()

def startDraw():            
    threading.Thread(target = draw).start()  

def draw():
    global run
    run = not run
    time.sleep(5)  
    pyautogui.click() 
    distance = 50
    lock = threading.Lock()
    initialPosition = pyautogui.position()
    while distance > 0 and run:
        with lock:
            pyautogui.dragRel(distance, 0)
            distance = distance - 5  # ❹
            pyautogui.dragRel(0, distance, duration=0.0)  
            pyautogui.dragRel(-distance, 0, duration=0.1) 
            distance = distance - 5
            pyautogui.dragRel(0, -distance, duration=0.2) 
    if run:
        pyautogui.dragTo(initialPosition)
        time.sleep(5)
        pyautogui.dragTo(initialPosition, duration=0.1)
        time.sleep(5)
        pyautogui.dragTo(initialPosition, duration=0.2)
        time.sleep(5)
        pyautogui.dragTo(initialPosition, button='left', duration=0.2)
        time.sleep(5)
        pyautogui.dragTo(initialPosition, button='left', duration=1)

        pyautogui.moveTo(initialPosition)
        pyautogui.mouseDown(button='left')
        pyautogui.move(0, 30)
        pyautogui.mouseUp(button='left')

if __name__ == "__main__":     
    generateAgents()
    with keyboard.GlobalHotKeys({
            '<ctrl>+<alt>+s': start,
            '<ctrl>+<alt>+p': pause,
            '<ctrl>+<alt>+q': die,
            '<ctrl>+<alt>+t': startDraw}) as change_state:
        change_state.join()

    
    

