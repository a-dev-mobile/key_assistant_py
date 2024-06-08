import keyboard
import time
import pygetwindow as gw
from threading import Thread
from tray_icon import setup_tray

double_shift_time = 0.3  # Максимальное время между двойными нажатиями shift
shift_pressed_time = []
delay_before_action = 0.5  # Задержка

# State variables for alt+z followed by x
alt_z_pressed = False
alt_z_time = 1  # Maximum time between alt+z and x

def get_active_window_title():
    try:
        return gw.getActiveWindow().title
    except Exception as e:
        return None

def log_action(window_title):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    log_message = f"{timestamp} - {window_title}"
    print(log_message)

def on_ctrl_shift_p():
    active_window = get_title_active_window()
    if active_window and 'Obsidian' in active_window:
        time.sleep(delay_before_action)
        keyboard.press_and_release('ctrl+p')

def on_ctrl_equals():
    active_window = get_title_active_window()
    if active_window and 'Obsidian' in active_window:
        time.sleep(delay_before_action)
        keyboard.press_and_release('ctrl+n')

def on_shift_press(event):
    global shift_pressed_time
    current_time = time.time()
    shift_pressed_time.append(current_time)

    # Очищаем старые записи
    shift_pressed_time = [t for t in shift_pressed_time if current_time - t < double_shift_time]

    # Если было два нажатия Shift в установленное время
    if len(shift_pressed_time) == 2:
        shift_pressed_time = []
        active_window = get_title_active_window()
        if active_window and 'Obsidian' in active_window:
            time.sleep(delay_before_action)
            keyboard.press_and_release('ctrl+o')

def on_alt_z():
    global alt_z_pressed
    alt_z_pressed = True

def on_x():
    global alt_z_pressed 
    
    if alt_z_pressed:
        active_window = get_title_active_window()
        if active_window and ('Obsidian' in active_window or 'Total Commander' in active_window):
            time.sleep(delay_before_action)
            keyboard.press_and_release('backspace')
            keyboard.press_and_release('F2')
        alt_z_pressed = False  # Сброс состояния после выполнения действия

def get_title_active_window():
    active_window = get_active_window_title()
    log_action(active_window)
    return active_window

def start_key_listener():
    keyboard.on_press_key('shift', on_shift_press)
    keyboard.add_hotkey('ctrl+shift+p', on_ctrl_shift_p)
    keyboard.add_hotkey('alt+=', on_ctrl_equals)
    keyboard.add_hotkey('alt+z', on_alt_z)
    keyboard.on_press_key('x', lambda e: on_x())
    # keyboard.wait('esc')  # Ожидание нажатия клавиши ESC для выхода

def main():
    print("Скрипт старт")

    # Запуск слушателя клавиш в отдельном потоке
    listener_thread = Thread(target=start_key_listener)
    listener_thread.daemon = True
    listener_thread.start()

    # Запуск значка в трее
    tray_thread = Thread(target=setup_tray)
    tray_thread.daemon = True
    tray_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Скрипт остановлен")

if __name__ == "__main__":
    main()
