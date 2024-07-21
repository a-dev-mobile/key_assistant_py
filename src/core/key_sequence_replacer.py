import time
import logging
import keyboard
import traceback
import pyperclip
from threading import Thread
from read_key.key_reader import start_reading_keys
from core.yaml_loader import load_key_sequences
from core.sqlite_manager import SQLiteManager


class KeySequenceReplacer:
    def __init__(self, yaml_path, delay, device_path):
        logging.debug(
            f"Initializing KeySequenceReplacer with yaml_path: {yaml_path}, delay: {delay}, device_path: {device_path}"
        )
        self.key_sequences = load_key_sequences(yaml_path)
        self.delay = delay
        self.device_path = device_path
        self.key_sequence = []
        self.first_match = True
        self.special_characters = {
            "!": "shift+1",
            "@": "shift+2",
            "#": "shift+3",
            "$": "shift+4",
            "%": "shift+5",
            "^": "shift+6",
            "&": "shift+7",
            "*": "shift+8",
            "(": "shift+9",
            ")": "shift+0",
            "_": "shift+-",
            "+": "shift+=",
            "{": "shift+[",
            "}": "shift+]",
            "|": "shift+\\",
            ":": "shift+;",
            '"': "shift+'",
            "<": "shift+,",
            ">": "shift+.",
            "?": "shift+/",
        }
        self.db_manager = SQLiteManager()
        self.current_clipboard = pyperclip.paste()
        self.skip_saving_clipboard = False

    def update_clipboard_buffers(self):
        new_clipboard = pyperclip.paste()
        if new_clipboard != self.current_clipboard:
            logging.debug(
                f"Clipboard changed from {self.current_clipboard} to {new_clipboard}"
            )
            self.current_clipboard = new_clipboard
            if not self.skip_saving_clipboard:
                self.db_manager.save_clipboard_content(new_clipboard)
                logging.info(f"Clipboard updated: {new_clipboard}")
            else:
                logging.info(f"Skipping clipboard save: {new_clipboard}")
                self.skip_saving_clipboard = False

    def clipboard_monitor(self):
        logging.debug("Starting clipboard monitor thread")
        while True:
            self.update_clipboard_buffers()
            time.sleep(1)  # Check for changes every second

    def delete_key_sequence(self, length):
        logging.debug(f"Deleting key sequence of length: {length}")
        for _ in range(length):
            keyboard.send("backspace")
            time.sleep(self.delay)

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
                self.delete_key_sequence(length - 1)
                self.first_match = False

            self.delete_key_sequence(length)

            # Вставляем текст
            pyperclip.copy(text_to_insert)  # Скопируем текст в буфер обмена
            keyboard.send("ctrl+v")  # Вставим текст из буфера обмена
            time.sleep(self.delay)

            if self.first_match:
                logging.info(
                    f"Inserting text again due to first_match: {text_to_insert}"
                )
                keyboard.send("ctrl+v")  # Вставим текст из буфера обмена второй раз
                time.sleep(self.delay)
                self.first_match = False

            self.key_sequence.clear()
            self.skip_saving_clipboard = True
        except Exception as e:
            error_message = (
                f"Error inserting text from buffer: {e}\n{traceback.format_exc()}"
            )
            logging.error(error_message)

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
            self.delete_key_sequence(len(key_group))

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

    def check_key_sequence(self):
        logging.debug(f"Checking key sequence: {self.key_sequence}")
        # Check if the current key sequence matches any sequence in the YAML file
        for sequence in self.key_sequences:
            if isinstance(sequence["keys"][0], list):  # Handle common replacements
                for key_group in sequence["keys"]:
                    if self.key_sequence[-len(key_group) :] == key_group:
                        logging.debug(f"Match found for key group: {key_group}")
                        if sequence["action"] == "replace":
                            self.replace_text(key_group, sequence["replace"])
                        elif sequence["action"] == "insert_from_buffer":
                            self.insert_text_from_buffer(
                                sequence["position"], len(key_group)
                            )
                        return
            else:
                if self.key_sequence[-len(sequence["keys"]) :] == sequence["keys"]:
                    logging.debug(f'Match found for sequence: {sequence["keys"]}')
                    if sequence["action"] == "replace":
                        self.replace_text(sequence["keys"], sequence["replace"])
                    elif sequence["action"] == "insert_from_buffer":
                        self.insert_text_from_buffer(
                            sequence["position"], len(sequence["keys"])
                        )
                    return

    def on_key_event(self, key_name, key_code, key_type, key_state):
        logging.debug(
            f"Key event - Name: {key_name}, Code: {key_code}, Type: {key_type}, State: {key_state}"
        )
        # Handle key events and update the key sequence
        if key_state == "down":
            self.key_sequence.append(key_name)
            self.check_key_sequence()

    def start(self):
        logging.debug("Starting KeySequenceReplacer")
        clipboard_thread = Thread(target=self.clipboard_monitor)
        clipboard_thread.daemon = True
        clipboard_thread.start()
        start_reading_keys(self.on_key_event, self.device_path)

    def stop(self):
        logging.debug("Stopping KeySequenceReplacer")
        pass
