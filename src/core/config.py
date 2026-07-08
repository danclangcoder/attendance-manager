import json
import os
import sys
from pathlib import Path


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2  # type: ignore
    except Exception:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relative_path)


with open(resource_path('config/config.json'), encoding='utf-8') as file:
    config = json.load(file)

IMAGE_PATH = Path(resource_path(config['images']['path']))
ICON_PATH = Path(resource_path(config['icons']['path']))

WINDOW_ICON = resource_path(str(ICON_PATH / 'calendar.ico'))

SCHOOL_LOGO = resource_path(str(IMAGE_PATH / 'access.png'))
APP_LOGO = resource_path(str(IMAGE_PATH / 'qr.png'))
BLUE_BG = resource_path(str(IMAGE_PATH / 'blue-bg.jpg'))
