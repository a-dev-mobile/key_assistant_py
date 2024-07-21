import sys
import os
import argparse
import evdev
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.key_sequence_replacer import KeySequenceReplacer
from read_key.device_setup import find_device_path_by_name
from read_key.logger_setup import setup_logger

if __name__ == "__main__":
    # Argument parser to get command line arguments for YAML file path, delay, device name, and log level
    parser = argparse.ArgumentParser(description='Key sequence replacer')
    parser.add_argument('--yaml_path', type=str, required=True, help='Path to the YAML file with key sequences')
    parser.add_argument('--delay', type=float, required=True, help='Delay between key presses for emulating human typing')
    parser.add_argument('--device_name', type=str, required=True, help='Name of the input device')
    parser.add_argument('--log_level', type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default='INFO', help='Set the logging level')

    args = parser.parse_args()

    # Setup logger with specified log level
    setup_logger(args.log_level)
    logging.debug(f'Arguments: {args}')

    # Find the device path by name
    device_path = find_device_path_by_name(args.device_name)
    logging.debug(f'Device path: {device_path}')

    # Create an instance of KeySequenceReplacer and start the replacer
    replacer = KeySequenceReplacer(args.yaml_path, args.delay, device_path)
    
    try:
        replacer.start()
    except KeyboardInterrupt:
        replacer.stop()
        logging.info("Program terminated.")
