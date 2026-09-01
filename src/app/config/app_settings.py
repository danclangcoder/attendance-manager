import json
import sys
from pathlib import Path

if "__compiled__" in globals():
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).resolve().parents[3]

def load_config():
    config_path = BASE_DIR / "config" / "config.json"

    with config_path.open(encoding="utf-8") as file:
        config = json.load(file)

    return config


config = load_config()


class Settings:
    LOGO_PATH = BASE_DIR / config["assets"]["logos"]
    ICON_PATH = BASE_DIR / config["assets"]["icons"]
    CLIENT_SECRET = BASE_DIR / config["oauth"]["client_secret"]

    APP_DATA_DIR = Path.home() / "AppData" / "Roaming" / "AttendanceManager"

    DATABASE_PATH = APP_DATA_DIR / "database" / "attendance.db"

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
