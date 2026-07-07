from pathlib import Path


ROOT = Path(__file__).resolve().parent

GAME_CONFIG = ROOT / "config.json"

PACKAGE_ASSET_DIR = ROOT  /  "package" / "assets" 
APP_ASSET_DIR = ROOT / "app" / "assets" 

DEFAULT_ICON_IMAGE = PACKAGE_ASSET_DIR / "img" / "default_icon.ico"