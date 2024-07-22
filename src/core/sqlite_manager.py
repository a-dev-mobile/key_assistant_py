import sqlite3
import logging

class SQLiteManager:
    def __init__(self, db_path='clipboard_buffers.db'):
        logging.debug(f'Initializing SQLiteManager with db_path: {db_path}')
        self.db_path = db_path
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS clipboard_buffers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL
                )
            ''')
            logging.debug('Table clipboard_buffers created or already exists')

    def save_clipboard_content(self, content, callback=None):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('INSERT INTO clipboard_buffers (content) VALUES (?)', (content,))
                logging.info(f'Added to database: {content}')
            logging.debug("Calling callback after saving content.")  # Дополнительный лог
            if callback:
                callback()
        except Exception as e:
            logging.error(f"Error saving content to database: {e}")
            if callback:
                callback()  # Вызов callback даже при ошибке для сброса флага

    def get_clipboard_content_by_position(self, position):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT content FROM clipboard_buffers ORDER BY id DESC LIMIT 1 OFFSET ?', (position,))
            row = cursor.fetchone()
            logging.debug(f'Fetched content from position {position}: {row[0] if row else "None"}')
            return row[0] if row else None
