import sys
import os
import argparse
import evdev

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.key_sequence_replacer import KeySequenceReplacer
from read_key.device_setup import find_device_path_by_name

if __name__ == "__main__":
    # Argument parser to get command line arguments for YAML file path, delay, and device name
    parser = argparse.ArgumentParser(description='Key sequence replacer')
    parser.add_argument('--yaml_path', type=str, required=True, help='Path to the YAML file with key sequences')
    parser.add_argument('--delay', type=float, required=True, help='Delay between key presses for emulating human typing')
    parser.add_argument('--device_name', type=str, required=True, help='Name of the input device')

    args = parser.parse_args()

    # Find the device path by name
    device_path = find_device_path_by_name(args.device_name)

    # Create an instance of KeySequenceReplacer and start the replacer
    replacer = KeySequenceReplacer(args.yaml_path, args.delay, device_path)
    replacer.start()
