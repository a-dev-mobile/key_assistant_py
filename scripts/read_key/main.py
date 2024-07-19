import logging
from evdev import InputDevice, categorize, ecodes, KeyEvent
from scripts.read_key.logger_setup import setup_logger
from scripts.read_key.device_setup import get_input_device
from scripts.read_key.key_utils import get_key_type, get_key_state, get_key_name
from scripts.read_key.key_states import KeyStates
import sys
import os

# Добавление корневого каталога проекта в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Настройка логирования
setup_logger()

# Определение устройства ввода
device_path = '/dev/input/event15'  # Проверьте точный путь к вашему устройству

def start_reading_keys(on_key_event):
    dev = get_input_device(device_path)
    try:
        key_states = KeyStates()
        for event in dev.read_loop():
            if event.type == ecodes.EV_KEY:
                key_event = categorize(event)
                key_code = key_event.scancode
                key_state = get_key_state(key_event)
                key_type = get_key_type(key_code)
                key_name = get_key_name(key_code, key_states.shift_pressed, key_states.caps_lock_on)

                if key_code not in key_states.key_states or key_states.key_states[key_code] != key_state:
                    key_states.update_key_state(key_code, key_state)
                    on_key_event(key_name, key_code, key_type, key_state)
    except Exception as e:
        logging.error(f'Error: {e}')
        print(f'Error: {e}')
