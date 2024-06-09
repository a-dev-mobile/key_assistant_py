import time
import keyboard
from alt_z_x_handler import get_active_window_title

DELAY_BEFORE_ACTION = 0.5  # Задержка перед действием

def perform_action(window_title, action_keys):
    if window_title and 'Obsidian' in window_title:
        time.sleep(DELAY_BEFORE_ACTION)
        keyboard.press_and_release(action_keys)

def on_ctrl_shift_p():
    perform_action(get_active_window_title(), 'ctrl+p')
