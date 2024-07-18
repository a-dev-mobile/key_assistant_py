import yaml

def load_key_sequences(yaml_path):
    # Load key sequences from a YAML file
    with open(yaml_path, 'r') as file:
        return yaml.safe_load(file)['replacements']
