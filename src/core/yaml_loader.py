import yaml

def load_key_sequences(yaml_path):
    # Load key sequences from a YAML file
    with open(yaml_path, 'r') as file:
        return yaml.safe_load(file)['replacements']
    
    """ 
    
    yaml_path
    yaml
    safe_loadsafe_loadsafe_load
    import time
import logging
import keyboard
import traceback
import pyperclip
from threading import Thread
from read_key.key_reader import start_reading_keys
from core.yaml_loader import load_key_sequences
from core.sqlite_manager import SQLiteManagersafe_loadyamlyaml_path
    """
