from read_key.main import start_reading_keys

class KeyboardListener:
    def __init__(self, on_key_press):
        self.on_key_press = on_key_press

    def start(self):
        start_reading_keys(self.on_key_press)
