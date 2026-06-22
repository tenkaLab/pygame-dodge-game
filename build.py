import sys
import argparse
import datetime
from pathlib import Path

from build_configs import build_x64, build_wasm
from build_configs.context import BuildContext

PROJECT_DIR = "dodge-game"

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / PROJECT_DIR))

from game import config

def main():
    parser = argparse.ArgumentParser(
        prog='build.py',
        description='Build the game for different platforms.',
        epilog='Example usage: python build.py --wasm')

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--x64", action="store_const", dest="target", const="x64")
    group.add_argument("--wasm", action="store_const", dest="target", const="wasm")
    group.add_argument("--all", action="store_const", dest="target", const="all")
    group.set_defaults(target="x64")

    parser.add_argument("--output-dir", type=str, default=None, help="Output directory for the build artifacts.")
    parser.add_argument("--force", action="store_true")

    args = parser.parse_args()

    if args.output_dir:
        build_dir_name = args.output_dir
    else:
        build_dir_name = datetime.datetime.now().strftime(f"{config.game['name']}_v{config.game['version']}_%Y%m%d_%H%M%S")

    context = BuildContext(
        name=config.game["name"],
        version=config.game["version"],
        icon=Path(ROOT / PROJECT_DIR / config.game["icon_image_path"]),
        project_root=Path(ROOT / PROJECT_DIR),
        build_root=Path(ROOT / "build" / build_dir_name),
        force=args.force,
    )

    if args.target == "x64":
        build_x64.main(context)
    elif args.target == "wasm":
        build_wasm.main(context)
    elif args.target == "all":
        build_x64.main(context)
        build_wasm.main(context)

if __name__ == "__main__":
    main()
