import time
import logging
import pyperclip
from core.sqlite_manager import SQLiteManager

class ClipboardMonitor:
    def __init__(self):
        self.db_manager = SQLiteManager()
        self.current_clipboard = pyperclip.paste()
        self.skip_saving_clipboard = False  # Флаг для пропуска сохранения
        self.data_written = True  # Флаг для отслеживания записи данных
        self.update_initiated_by_key_sequence = False  # Флаг для отслеживания обновления буфера ключевой последовательностью

    def update_clipboard_buffers(self):
        self.data_written = True  
        if not self.data_written:
            logging.debug("Waiting for data to be written before checking clipboard again.")
            return

        new_clipboard = pyperclip.paste()
        if new_clipboard != self.current_clipboard:
            logging.debug(
                f"Clipboard changed from {self.current_clipboard} to {new_clipboard}"
            )
            self.current_clipboard = new_clipboard
            if not self.skip_saving_clipboard and not self.update_initiated_by_key_sequence:
                self.db_manager.save_clipboard_content(new_clipboard, self.data_written_callback)
                self.data_written = False
                logging.info(f"Clipboard updated: {new_clipboard}")
            else:
                logging.info(f"Skipping clipboard save: {new_clipboard}")
                self.skip_saving_clipboard = False  # Сброс флага пропуска сохранения
                self.update_initiated_by_key_sequence = False  # Сброс флага обновления буфера ключевой последовательностью

    def data_written_callback(self):
        self.data_written = True  # Установка флага, что данные записаны
        logging.debug("Data has been written, ready for next clipboard check.")

    def start(self):
        logging.debug("Starting clipboard monitor thread")
        while True:
            self.update_clipboard_buffers()
            time.sleep(1)  # Check for changes every second
