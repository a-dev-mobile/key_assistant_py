import time
from pynput import keyboard
from yaml_loader import load_key_sequences

class KeySequenceReplacer:
    def __init__(self, yaml_path, delay):
        # Initialize with key sequences and delay from YAML file
        self.key_sequences = load_key_sequences(yaml_path)
        self.delay = delay
        self.key_sequence = []
        self.keyboard_controller = keyboard.Controller()

    def replace_text(self, key_group, replace):
        # Replace text by deleting the key sequence and typing the replacement text
        for _ in range(len(key_group)):
            self.keyboard_controller.press(keyboard.Key.backspace)
            self.keyboard_controller.release(keyboard.Key.backspace)
        for char in replace:
            self.keyboard_controller.type(char)
            time.sleep(self.delay)
        self.key_sequence.clear()

    def check_key_sequence(self):
        # Check if the current key sequence matches any sequence in the YAML file
        for sequence in self.key_sequences:
            if isinstance(sequence['keys'][0], list):  # Handle shared replacements
                for key_group in sequence['keys']:
                    if self.key_sequence[-len(key_group):] == key_group:
                        self.replace_text(key_group, sequence['replace'])
                        return
            else:
                if self.key_sequence[-len(sequence['keys']):] == sequence['keys']:
                    self.replace_text(sequence['keys'], sequence['replace'])
                    return

    def on_key_press(self, key):
        # Handle key press events and update the key sequence
        try:
            key_name = key.char if hasattr(key, 'char') and key.char else key.name
        except AttributeError:
            key_name = str(key)
        self.key_sequence.append(key_name)
        self.check_key_sequence()

    def start(self):
        # Start listening for key press events
        with keyboard.Listener(on_press=self.on_key_press) as listener:
            listener.join()
