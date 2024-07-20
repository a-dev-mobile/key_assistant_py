import time
import logging
import keyboard
import traceback
from read_key.key_reader import start_reading_keys
from core.yaml_loader import load_key_sequences

class KeySequenceReplacer:
    def __init__(self, yaml_path, delay, device_path):
        self.key_sequences = load_key_sequences(yaml_path)
        self.delay = delay
        self.device_path = device_path
        self.key_sequence = []
        self.special_characters = {
            '!': 'shift+1',
            '@': 'shift+2',
            '#': 'shift+3',
            '$': 'shift+4',
            '%': 'shift+5',
            '^': 'shift+6',
            '&': 'shift+7',
            '*': 'shift+8',
            '(': 'shift+9',
            ')': 'shift+0',
            '_': 'shift+-',
            '+': 'shift+=',
            '{': 'shift+[', 
            '}': 'shift+]', 
            '|': 'shift+\\', 
            ':': 'shift+;', 
            '"': 'shift+\'', 
            '<': 'shift+,', 
            '>': 'shift+.', 
            '?': 'shift+/'
        }

    def replace_text(self, key_group, replace):
        try:
            logging.info(f"Detected match: {key_group}, replacing with: {replace}")
            # Delete the key sequence
            for _ in range(len(key_group)):
                keyboard.send('backspace')
                time.sleep(self.delay)
            
            # Enter the replacement text
            for char in replace:
                if char.isupper():
                    keyboard.send(f'shift+{char.lower()}')
                elif char in self.special_characters:
                    keyboard.send(self.special_characters[char])
                else:
                    keyboard.write(char)
                time.sleep(self.delay)
            
            self.key_sequence.clear()
        except Exception as e:
            error_message = f"Error replacing text: {e}\n{traceback.format_exc()}"
            logging.error(error_message)
            print(error_message)

    def check_key_sequence(self):
        # Check if the current key sequence matches any sequence in the YAML file
        for sequence in self.key_sequences:
            if isinstance(sequence['keys'][0], list):  # Handle common replacements
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
        start_reading_keys(self.on_key_event, self.device_path)
