import evdev

def get_input_device(device_path):
    dev = evdev.InputDevice(device_path)
    print(f"Using device: {dev.name}")
    return dev

def find_device_path_by_name(device_name):
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if device_name in device.name:
            return device.path
    raise ValueError(f"Device with name '{device_name}' not found")
