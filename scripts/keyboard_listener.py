from pynput import keyboard

class KeyboardListener:
    def __init__(self, on_key_press):
        # Initialize the listener with a callback function for key presses
        self.on_key_press = on_key_press

    def start(self):
        # Start listening for keyboard events
        with keyboard.Listener(on_press=self.on_key_press) as listener:
            listener.join()
