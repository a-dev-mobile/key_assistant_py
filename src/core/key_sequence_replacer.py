import time
import logging
from threading import Thread
from read_key.key_reader import start_reading_keys
from core.yaml_loader import load_key_sequences
from core.clipboard_monitor import ClipboardMonitor
from core.key_sequence_handler import KeySequenceHandler

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
        self.clipboard_monitor = ClipboardMonitor()
        self.key_sequence_handler = KeySequenceHandler(self.key_sequences, self.delay, self.key_sequence, self.clipboard_monitor)

    def on_key_event(self, key_name, key_code, key_type, key_state):
        logging.debug(
            f"Key event - Name: {key_name}, Code: {key_code}, Type: {key_type}, State: {key_state}"
        )
        # Handle key events and update the key sequence
        if key_state == "down":
            self.key_sequence.append(key_name)
            self.key_sequence_handler.check_key_sequence()

    def start(self):
        logging.debug("Starting KeySequenceReplacer")
        clipboard_thread = Thread(target=self.clipboard_monitor.start)
        clipboard_thread.daemon = True
        clipboard_thread.start()
        start_reading_keys(self.on_key_event, self.device_path)

    def stop(self):
        logging.debug("Stopping KeySequenceReplacer")
        pass
