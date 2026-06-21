from pathlib import Path


ROOT = Path(__file__).resolve().parent

PACKAGE_ASSET_DIR = ROOT  /  "package" / "assets" 
APP_ASSET_DIR = ROOT / "app" / "assets" 

CB_IMAGE = PACKAGE_ASSET_DIR / "img" / "cb.jpg"
DEFAULT_ICON_IMAGE = PACKAGE_ASSET_DIR / "img" / "default_icon.ico"