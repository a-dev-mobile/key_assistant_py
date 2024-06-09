# alt_z_handler.py

import keyboard
import time
import pygetwindow as gw

DELAY_BEFORE_ACTION = 0.5  # Задержка перед действием
ALT_Z_TIME = 1  # Максимальное время между alt+z и x

alt_z_pressed = False

def get_active_window_title():
    try:
        return gw.getActiveWindow().title
    except Exception:
        return None

def perform_action(window_title, action_keys):
    if window_title and 'Obsidian' in window_title:
        time.sleep(DELAY_BEFORE_ACTION)
        keyboard.press_and_release(action_keys)

def on_alt_z():
    global alt_z_pressed
    alt_z_pressed = True

def on_x():
    global alt_z_pressed
    if alt_z_pressed:
        active_window = get_active_window_title()
        if active_window and ('Obsidian' in active_window or 'Total Commander' in active_window):
            time.sleep(DELAY_BEFORE_ACTION)
            keyboard.press_and_release('backspace')
            keyboard.press_and_release('F2')
        alt_z_pressed = False  # Сброс состояния после выполнения действия

def setup_alt_z_handler():
    keyboard.add_hotkey('alt+z', on_alt_z)
    keyboard.on_press_key('x', lambda e: on_x())
