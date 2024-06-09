import time
import keyboard
from alt_z_x_handler import get_active_window_title

DOUBLE_SHIFT_TIME = 0.3  # Максимальное время между двойными нажатиями Shift
shift_pressed_time = []

def on_shift_press(event):
    global shift_pressed_time
    current_time = time.time()
    shift_pressed_time.append(current_time)

    # Очищаем старые записи
    shift_pressed_time = [t for t in shift_pressed_time if current_time - t < DOUBLE_SHIFT_TIME]

    # Если было два нажатия Shift в установленное время
    if len(shift_pressed_time) == 2:
        shift_pressed_time = []
        from main import perform_action
        perform_action(get_active_window_title(), 'ctrl+o')

def setup_double_shift_handler():
    keyboard.on_press_key('shift', on_shift_press)
