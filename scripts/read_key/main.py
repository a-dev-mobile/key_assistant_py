import logging
from evdev import InputDevice, categorize, ecodes, KeyEvent
from logger_setup import setup_logger
from device_setup import get_input_device
from key_maps import keypad_keys, letter_keys, number_keys, function_keys, navigation_keys, modifier_keys, other_keys
from key_utils import get_key_type, get_key_state, get_key_name
from key_states import KeyStates

# Настройка логирования
setup_logger()

# Определение устройства ввода
device_path = '/dev/input/event15'  # Проверьте точный путь к вашему устройству
dev = get_input_device(device_path)

# Основной цикл для чтения событий
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

                logging.info(f'Key name: {key_name}, Key code: {key_code}, Key type: {key_type}, Key state: {key_state}')

except Exception as e:
    logging.error(f'Error: {e}')
    print(f'Error: {e}')
