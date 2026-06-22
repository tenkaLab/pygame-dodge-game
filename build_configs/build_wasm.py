import subprocess

from build_configs.context import BuildContext

def main(context: BuildContext) -> None:
    print("Building for WASM...")
    print(f"Context: {context}")
    return
