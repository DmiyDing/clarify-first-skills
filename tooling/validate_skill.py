#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def resolve_quick_validate() -> Path:
    env_root = os.environ.get("SKILL_CREATOR_ROOT")
    if env_root:
        root = Path(env_root).expanduser().resolve()
        candidate = root / "scripts" / "quick_validate.py"
        if candidate.exists():
            return candidate

    env_scripts = os.environ.get("SKILL_CREATOR_SCRIPTS")
    if env_scripts:
        scripts_dir = Path(env_scripts).expanduser().resolve()
        candidate = scripts_dir / "quick_validate.py"
        if candidate.exists():
            return candidate

    home = Path.home()
    candidates = [
        home / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py",
        home / ".claude" / "skills" / "skill-creator" / "scripts" / "quick_validate.py",
        ROOT / "vendor" / "skill-creator" / "scripts" / "quick_validate.py",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    raise SystemExit(
        "Could not locate Anthropic skill-creator validator. "
        "Set SKILL_CREATOR_ROOT or SKILL_CREATOR_SCRIPTS to a valid installation path."
    )


def main() -> int:
    validator = resolve_quick_validate()
    result = subprocess.run(
        ["python3", str(validator), "./clarify-first"],
        cwd=ROOT,
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
