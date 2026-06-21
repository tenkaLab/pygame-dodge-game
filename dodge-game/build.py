import subprocess
import datetime
from pathlib import Path

from game import config


_name = config.game["name"]
_version = config.game["version"]
_icon_image_path = config.game["icon_image_path"]

ROOT = Path(__file__).resolve().parent
DIR_NAME = datetime.datetime.now().strftime(f"{_name}_v{_version}_%Y%m%d_%H%M%S")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BUILD_ROOT = PROJECT_ROOT / "build" / "win" / DIR_NAME
BUILD_ROOT.mkdir(parents=True, exist_ok=True)


spec_file = BUILD_ROOT / f"{_name}.spec"
if spec_file.exists():
    spec_file.unlink()

cmd = [
    "pyinstaller",
    "--onedir",
    "--contents-directory", ".",
    "--noconsole",
    "--name",        _name,
    "--icon",        str((ROOT / _icon_image_path).resolve()),
    "--add-data",    f"{ROOT / 'game/app/assets'};game/app/assets",
    "--add-data",    f"{ROOT / 'game/package/assets'};game/package/assets",
    "--distpath",    str(BUILD_ROOT / "dist"),
    "--workpath",    str(BUILD_ROOT / "build"),
    "--specpath",    str(BUILD_ROOT),
    str((ROOT / "main.py").resolve()),
]

subprocess.run(cmd)