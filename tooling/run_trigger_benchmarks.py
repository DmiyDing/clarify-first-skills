#!/usr/bin/env python3
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def resolve_skill_creator_root() -> Path:
    env_root = os.environ.get("SKILL_CREATOR_ROOT")
    if env_root:
        root = Path(env_root).expanduser().resolve()
        if (root / "scripts" / "run_eval.py").exists():
            return root

    env_scripts = os.environ.get("SKILL_CREATOR_SCRIPTS")
    if env_scripts:
        scripts_dir = Path(env_scripts).expanduser().resolve()
        if (scripts_dir / "run_eval.py").exists():
            return scripts_dir.parent

    home = Path.home()
    candidates = [
        home / ".claude" / "skills" / "skill-creator",
        home / ".codex" / "skills" / ".system" / "skill-creator",
        ROOT / "vendor" / "skill-creator",
    ]
    for candidate in candidates:
        if (candidate / "scripts" / "run_eval.py").exists():
            return candidate
    raise SystemExit(
        "Could not locate Anthropic skill-creator. "
        "Set SKILL_CREATOR_ROOT or SKILL_CREATOR_SCRIPTS to a valid installation path."
    )


def ensure_claude_ready() -> None:
    probe = subprocess.run(
        ["claude", "-p", "ping", "--output-format", "text"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    combined = f"{probe.stdout}\n{probe.stderr}".strip()
    if probe.returncode != 0 or "Not logged in" in combined:
        raise RuntimeError(
            "Claude Code CLI is not authenticated for benchmark runs. "
            "Run `claude /login` and retry."
        )


def main() -> int:
    skill_creator_root = resolve_skill_creator_root()
    official_run_eval = skill_creator_root / "scripts" / "run_eval.py"
    ensure_claude_ready()
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    results_dir = ROOT / "benchmarks" / "results" / timestamp
    results_dir.mkdir(parents=True, exist_ok=True)

    eval_set = ROOT / "benchmarks" / "trigger-evals" / "clarify-first.json"
    skill_path = ROOT / "clarify-first"
    output_path = results_dir / "clarify-first.json"

    env = dict(os.environ)
    env["PYTHONPATH"] = str(skill_creator_root)
    cmd = [
        "python3",
        str(official_run_eval),
        "--eval-set",
        str(eval_set),
        "--skill-path",
        str(skill_path),
        "--runs-per-query",
        "2",
        "--trigger-threshold",
        "0.5",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, env=env)
    output_path.write_text(result.stdout, encoding="utf-8")
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    data = json.loads(result.stdout)
    summary = {
        "results_dir": str(results_dir.relative_to(ROOT)),
        "summary": {
            "skill": "clarify-first",
            "passed": data["summary"]["passed"],
            "total": data["summary"]["total"],
            "results_file": str(output_path.relative_to(ROOT)),
        },
    }
    (results_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
