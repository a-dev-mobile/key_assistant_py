import logging
from evdev import categorize, ecodes
from .logger_setup import setup_logger
from .device_setup import get_input_device
from .key_utils import get_key_type, get_key_state, get_key_name
from .key_states import KeyStates

# Setup logging
setup_logger()

def start_reading_keys(on_key_event, device_path):
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
