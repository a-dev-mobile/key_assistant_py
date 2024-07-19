import evdev

def get_input_device(device_path):
    dev = evdev.InputDevice(device_path)
    print(f"Используемое устройство: {dev.name}")
    return dev
