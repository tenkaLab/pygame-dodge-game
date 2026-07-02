import subprocess
import sys
import shutil
from pathlib import Path

from build_configs.context import BuildContext

def rmtree(target: Path, force: bool):
    if target.exists() and any(target.iterdir()):
        if not force:
            answer = input(
                f'The output directory "{target}" and ALL ITS CONTENTS will be REMOVED! Continue? [y/N]: '
            ).strip().lower()

            if answer not in ("y", "yes"):
                return False
        shutil.rmtree(target)
    return True

def main(context: BuildContext) -> None:
    print("Building for WASM...")

    destination = context.build_root / "wasm"
    if not rmtree(destination, context.force):
        print("WASM build canceled.")
        return

    generated = context.project_root / "build"
    if not rmtree(generated, context.force):
        print("WASM build canceled.")
        return

    cmd = [
        sys.executable,
        "-Xutf8",
        "-m",
        "pygbag",
        "--app_name",
        context.name,
        "--title",
        context.name,
        "--icon",
        str(context.icon),
        "--build",
        str(context.project_root)
    ]

    subprocess.run(cmd, check=True)

    shutil.move(str(generated), str(destination))

    print("WASM build completed.")
    print(f"Build artifacts are located in: {(destination / 'web').resolve()}")
