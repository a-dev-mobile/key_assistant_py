import keyboard
import time
from threading import Thread
from pynput import mouse
from tray_icon import setup_tray
from alt_z_x_handler import setup_alt_z_handler, get_active_window_title
from double_shift_handler import setup_double_shift_handler
from ctrl_shift_p_handler import on_ctrl_shift_p


DELAY_BEFORE_ACTION = 0.5  # Задержка перед действием

def log_action(event_type, event_name, window_title):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    log_message = f"{timestamp} - {event_type}: {event_name} - Active window: {window_title}"
    print(log_message)

def perform_action(window_title, action_keys):
    if window_title and 'Obsidian' in window_title:
        time.sleep(DELAY_BEFORE_ACTION)
        keyboard.press_and_release(action_keys)

def on_ctrl_equals():
    perform_action(get_active_window_title(), 'ctrl+n')

def on_key_event(event):
    log_action('Key Press', event.name, get_active_window_title())

def on_mouse_move(x, y):
    log_action('Mouse Move', f'Position ({x}, {y})', get_active_window_title())

def on_mouse_click(x, y, button, pressed):
    event_type = 'Mouse Press' if pressed else 'Mouse Release'
    log_action('Raw Button Event', f'Button: {button}, Pressed: {pressed}', get_active_window_title())

def on_mouse_scroll(x, y, dx, dy):
    log_action('Mouse Scroll', f'Scroll ({dx}, {dy})', get_active_window_title())

def start_key_listener():
    keyboard.on_press(on_key_event)
    keyboard.add_hotkey('ctrl+shift+p', on_ctrl_shift_p)
    keyboard.add_hotkey('alt+=', on_ctrl_equals)
    setup_alt_z_handler()
    setup_double_shift_handler()

def start_mouse_listener():
    listener = mouse.Listener(
        on_move=on_mouse_move,
        on_click=on_mouse_click,
        on_scroll=on_mouse_scroll
    )
    listener.start()
    listener.join()

def main():
    print("Скрипт старт windows_assistant_py")

    # Запуск слушателя клавиш в отдельном потоке
    listener_thread = Thread(target=start_key_listener)
    listener_thread.daemon = True
    listener_thread.start()

    # Запуск слушателя мыши в отдельном потоке
    mouse_thread = Thread(target=start_mouse_listener)
    mouse_thread.daemon = True
    mouse_thread.start()

    # Запуск значка в трее
    tray_thread = Thread(target=setup_tray)
    tray_thread.daemon = True
    tray_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Скрипт остановлен windows_assistant_py")

if __name__ == "__main__":
    main()
