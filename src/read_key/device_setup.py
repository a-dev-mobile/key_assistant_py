import evdev

def get_input_device(device_path):
    dev = evdev.InputDevice(device_path)
    print(f"Using device: {dev.name}")
    return dev
