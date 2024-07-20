import time
from read_key.key_reader import start_reading_keys
from core.yaml_loader import load_key_sequences

class KeySequenceReplacer:
    def __init__(self, yaml_path, delay):
        self.key_sequences = load_key_sequences(yaml_path)
        self.delay = delay
        self.key_sequence = []

    def replace_text(self, key_group, replace):
        # Replace text by deleting the key sequence and typing the replacement text
        for _ in range(len(key_group)):
            # Имитация нажатия клавиши backspace
            print('\b', end='', flush=True)
        for char in replace:
            print(char, end='', flush=True)
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

    def on_key_event(self, key_name, key_code, key_type, key_state):
        # Handle key events and update the key sequence
        if key_state == 'down':
            self.key_sequence.append(key_name)
            self.check_key_sequence()

    def start(self):
        start_reading_keys(self.on_key_event)
