from evdev import ecodes

class KeyStates:
    def __init__(self):
        self.key_states = {}
        self.shift_pressed = False
        self.caps_lock_on = False

    def update_key_state(self, key_code, key_state):
        if key_code in [ecodes.KEY_LEFTSHIFT, ecodes.KEY_RIGHTSHIFT]:
            self.shift_pressed = (key_state == 'down') or (key_state == 'hold')
        elif key_code == ecodes.KEY_CAPSLOCK and key_state == 'down':
            self.caps_lock_on = not self.caps_lock_on
        
        self.key_states[key_code] = key_state
