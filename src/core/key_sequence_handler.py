import logging
import time
import keyboard
import pyperclip
import traceback
from core.sqlite_manager import SQLiteManager
from core.utils import delete_key_sequence

class KeySequenceHandler:
    def __init__(self, key_sequences, delay, key_sequence, clipboard_monitor):
        self.key_sequences = key_sequences
        self.delay = delay
        self.key_sequence = key_sequence
        self.db_manager = SQLiteManager()
        self.first_match = True
        self.skip_saving_clipboard = False
        self.clipboard_monitor = clipboard_monitor
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
            '?': 'shift+/',
        }

    def replace_text(self, key_group, replace):
        try:
            logging.info(f"Detected match: {key_group}, replacing with: {replace}")

            # Ensure the first character is deleted properly only once
            if self.first_match and self.key_sequence:
                logging.debug("Deleting first character")
                keyboard.send("backspace")
                time.sleep(self.delay)
                self.first_match = False

            # Delete the rest of the key sequence
            delete_key_sequence(len(key_group), self.delay)

            # Enter the replacement text
            logging.debug(f"Entering replacement text: {replace}")
            for char in replace:
                logging.debug(f"Entering character: {char}")
                if char.isupper():
                    keyboard.send(f"shift+{char.lower()}")
                elif char in self.special_characters:
                    keyboard.send(self.special_characters[char])
                else:
                    keyboard.write(char)
                time.sleep(self.delay)

            self.key_sequence.clear()
        except Exception as e:
            error_message = f"Error replacing text: {e}\n{traceback.format_exc()}"
            logging.error(error_message)

    def insert_text_from_buffer(self, position, length):
        try:
            text_to_insert = self.db_manager.get_clipboard_content_by_position(position)
            if text_to_insert is None:
                raise ValueError("Invalid buffer position")

            logging.info(
                f"Inserting text from buffer position {position}: {text_to_insert}"
            )

            # Удаление введенных ключей перед вставкой текста
            if self.first_match:
                # Повторное удаление, если это первый матч
                logging.info("Deleting key sequence again due to first_match")
                delete_key_sequence(length - 1, self.delay)
                self.first_match = False

            delete_key_sequence(length, self.delay)

            # Вставляем текст
            pyperclip.copy(text_to_insert)  # Скопируем текст в буфер обмена
            keyboard.send("shift+insert")  # Вставим текст из буфера обмена
            time.sleep(self.delay)

            if self.first_match:
                logging.info(
                    f"Inserting text again due to first_match: {text_to_insert}"
                )
                keyboard.send("shift+insert")  # Вставим текст из буфера обмена второй раз
                time.sleep(self.delay)
                self.first_match = False

            self.key_sequence.clear()
            self.skip_saving_clipboard = True
            self.clipboard_monitor.update_initiated_by_key_sequence = True  # Установка флага
        except Exception as e:
            error_message = (
                f"Error inserting text from buffer: {e}\n{traceback.format_exc()}"
            )
            logging.error(error_message)

    def check_key_sequence(self):
        logging.debug(f"Checking key sequence: {self.key_sequence}")
        # Check if the current key sequence matches any sequence in the YAML file
        for sequence in self.key_sequences:
            if isinstance(sequence["keys"][0], list):  # Handle common replacements
                for key_group in sequence["keys"]:
                    if self.key_sequence[-len(key_group):] == key_group:
                        logging.debug(f"Match found for key group: {key_group}")
                        if sequence["action"] == "replace":
                            self.replace_text(key_group, sequence["replace"])
                        elif sequence["action"] == "insert_from_buffer":
                            self.insert_text_from_buffer(
                                sequence["position"], len(key_group)
                            )
                        return
            else:
                if self.key_sequence[-len(sequence["keys"]):] == sequence["keys"]:
                    logging.debug(f'Match found for sequence: {sequence["keys"]}')
                    if sequence["action"] == "replace":
                        self.replace_text(sequence["keys"], sequence["replace"])
                    elif sequence["action"] == "insert_from_buffer":
                        self.insert_text_from_buffer(
                            sequence["position"], len(sequence["keys"])
                        )
                    return
