import time
import keyboard

def delete_key_sequence(length, delay):
    for _ in range(length):
        keyboard.send("backspace")
        time.sleep(delay)
