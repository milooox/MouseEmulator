import keyboard
from pynput.mouse import Controller, Button
import time
import threading
import os

mouse = Controller()

CONFIG = {
    'toggle': 'ctrl+i',
    'exit': 'ctrl+q',
    'up': 'w',
    'down': 's',
    'left': 'a',
    'right': 'd',
    'lmb': 'space',     
    'rmb': 'enter',     
    'speed': 10,        
    'tick_rate': 0.02   
}

state = {
    'active': False,
    'up': False,
    'down': False,
    'left': False,
    'right': False
}

def set_movement(direction, is_pressed):
    state[direction] = is_pressed

def click_mouse(button, is_pressed):
    if is_pressed:
        mouse.press(button)
    else:
        mouse.release(button)

def enable_control():
    """Włącza sterowanie i blokuje klawiaturę."""
    keyboard.on_press_key(CONFIG['up'], lambda _: set_movement('up', True), suppress=True)
    keyboard.on_release_key(CONFIG['up'], lambda _: set_movement('up', False), suppress=True)
    
    keyboard.on_press_key(CONFIG['down'], lambda _: set_movement('down', True), suppress=True)
    keyboard.on_release_key(CONFIG['down'], lambda _: set_movement('down', False), suppress=True)
    
    keyboard.on_press_key(CONFIG['left'], lambda _: set_movement('left', True), suppress=True)
    keyboard.on_release_key(CONFIG['left'], lambda _: set_movement('left', False), suppress=True)
    
    keyboard.on_press_key(CONFIG['right'], lambda _: set_movement('right', True), suppress=True)
    keyboard.on_release_key(CONFIG['right'], lambda _: set_movement('right', False), suppress=True)
    
    keyboard.on_press_key(CONFIG['lmb'], lambda _: click_mouse(Button.left, True), suppress=True)
    keyboard.on_release_key(CONFIG['lmb'], lambda _: click_mouse(Button.left, False), suppress=True)
    
    keyboard.on_press_key(CONFIG['rmb'], lambda _: click_mouse(Button.right, True), suppress=True)
    keyboard.on_release_key(CONFIG['rmb'], lambda _: click_mouse(Button.right, False), suppress=True)

def disable_control():
    """Niezawodne wyłączanie: resetuje wszystkie skróty i rejestruje podstawowe."""
    keyboard.unhook_all() 
    
    state['up'] = state['down'] = state['left'] = state['right'] = False
    
    keyboard.add_hotkey(CONFIG['toggle'], toggle)
    keyboard.add_hotkey(CONFIG['exit'], exit_program)

def exit_program():
    print("closing")
    os._exit(0)

def toggle():
    state['active'] = not state['active']
    if state['active']:
        print("mouse mode : on")
        enable_control()
    else:
        print("mouse mode : off")
        disable_control()

def mouse_movement_loop():
    while True:
        if state['active']:
            dx = 0
            dy = 0
            if state['left']:  dx -= CONFIG['speed']
            if state['right']: dx += CONFIG['speed']
            if state['up']:    dy -= CONFIG['speed']
            if state['down']:  dy += CONFIG['speed']
            
            if dx != 0 or dy != 0:
                mouse.move(dx, dy)
        
        time.sleep(CONFIG['tick_rate'])

movement_thread = threading.Thread(target=mouse_movement_loop, daemon=True)
movement_thread.start()

keyboard.add_hotkey(CONFIG['toggle'], toggle)
keyboard.add_hotkey(CONFIG['exit'], exit_program)

print(f"- {CONFIG['toggle'].upper()} : on/off mouse mode")
print(f"- {CONFIG['exit'].upper()} : exit")

keyboard.wait()