from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE_ASSET_DIR = ROOT / "game" /  "package" / "asset" 
APP_ASSET_DIR = ROOT / "game" / "app" / "asset" 

CB_IMAGE = PACKAGE_ASSET_DIR / "img" / "cb.jpg"
DEFAULT_ICON_IMAGE = PACKAGE_ASSET_DIR / "img" / "default_icon.ico"