from evdev import ecodes
from key_maps import keypad_keys, letter_keys, number_keys, function_keys, navigation_keys, modifier_keys, other_keys
import evdev
from evdev import ecodes, KeyEvent
import logging
def get_key_type(key_code):
    if key_code in keypad_keys:
        return 'Keypad Number'
    elif key_code in letter_keys:
        return 'Letter'
    elif key_code in number_keys:
        return 'Number'
    elif key_code in function_keys:
        return 'Function'
    elif key_code in navigation_keys:
        return 'Navigation'
    elif key_code in modifier_keys:
        return 'Modifier'
    elif key_code in other_keys:
        return 'Other'
    else:
        return 'Unknown'

def get_key_state(event):
    if event.keystate == KeyEvent.key_down:
        return 'down'
    elif event.keystate == KeyEvent.key_up:
        return 'up'
    elif event.keystate == KeyEvent.key_hold:
        return 'hold'

def get_key_name(key_code, shift_pressed, caps_lock_on):
    if key_code in keypad_keys:
        return keypad_keys[key_code]
    elif key_code in letter_keys:
        key_name = letter_keys[key_code]
        if (shift_pressed and not caps_lock_on) or (not shift_pressed and caps_lock_on):
            return key_name.upper()
        else:
            return key_name.lower()
    elif key_code in number_keys:
        return number_keys[key_code]
    elif key_code in function_keys:
        return function_keys[key_code]
    elif key_code in navigation_keys:
        return navigation_keys[key_code]
    elif key_code in modifier_keys:
        return modifier_keys[key_code]
    elif key_code in other_keys:
        return other_keys[key_code]
    return ecodes.KEY[key_code] if key_code in ecodes.KEY else 'UNKNOWN'
