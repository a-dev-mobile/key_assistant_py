import sys
import os
import argparse
from core.key_sequence_replacer import KeySequenceReplacer

if __name__ == "__main__":
    # Argument parser to get command line arguments for YAML file path and delay
    parser = argparse.ArgumentParser(description='Key sequence replacer')
    parser.add_argument('--yaml_path', type=str, required=True, help='Path to the YAML file with key sequences')
    parser.add_argument('--delay', type=float, required=True, help='Delay between key presses for emulating human typing')

    args = parser.parse_args()

    # Create an instance of KeySequenceReplacer and start the replacer
    replacer = KeySequenceReplacer(args.yaml_path, args.delay)
    replacer.start()
