import subprocess

from build_configs.context import BuildContext

def main(context: BuildContext) -> None:
    print("Building for x64...")

    destination = context.build_root / "x64"
    destination.mkdir(parents=True, exist_ok=True)

    spec_file = destination / f"{context.name}.spec"
    if spec_file.exists():
        spec_file.unlink()

    cmd = [
        "pyinstaller",
        "--onedir",
        "--contents-directory", ".",
        "--noconsole",
        "--name", context.name,
        "--icon", context.icon,
        "--add-data",    f"{context.project_root / 'game/app/assets'};game/app/assets",
        "--add-data",    f"{context.project_root / 'game/package/assets'};game/package/assets",
        "--distpath", str(destination / "dist"),
        "--workpath", str(destination / "build"),
        "--specpath", str(destination),
        str((context.project_root / "main.py").resolve()),
    ]

    if context.force:
        cmd.insert(-1, "--noconfirm")

    subprocess.run(cmd, check=True)
    print("x64 build completed.")
    print(f"Build artifacts are located in: { (destination / 'dist').resolve() }")
