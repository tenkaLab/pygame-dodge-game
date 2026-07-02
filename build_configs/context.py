from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class BuildContext:
    name: str
    version: str
    icon: Path
    project_root: Path
    build_root: Path
    force: bool
