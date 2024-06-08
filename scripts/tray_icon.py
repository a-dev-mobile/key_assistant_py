import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

def create_image(width, height, color1, color2):
    # Генерация иконки для трея
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)
    return image

def on_exit(icon, item):
    icon.stop()

def setup_tray():
    icon = pystray.Icon("Test Icon")
    icon.icon = create_image(64, 64, 'black', 'white')
    icon.menu = pystray.Menu(
        item('Exit', on_exit)
    )
    icon.run()
