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


def run_eval(skill_creator_root: Path, description: str | None) -> dict:
    eval_set = ROOT / "benchmarks" / "trigger-evals" / "clarify-first.json"
    skill_path = ROOT / "clarify-first"
    env = dict(os.environ)
    env["PYTHONPATH"] = str(skill_creator_root)
    cmd = [
        "python3",
        str(skill_creator_root / "scripts" / "run_eval.py"),
        "--eval-set",
        str(eval_set),
        "--skill-path",
        str(skill_path),
        "--runs-per-query",
        "2",
        "--trigger-threshold",
        "0.5",
    ]
    if description is not None:
        cmd.extend(["--description", description])
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, env=env)
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout)
    return json.loads(result.stdout)


def main() -> int:
    ensure_claude_ready()
    skill_creator_root = resolve_skill_creator_root()
    variants_path = ROOT / "benchmarks" / "description-variants" / "clarify-first.json"
    variants_data = json.loads(variants_path.read_text(encoding="utf-8"))
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    results_dir = ROOT / "benchmarks" / "ab-results" / timestamp
    results_dir.mkdir(parents=True, exist_ok=True)

    results = []

    baseline_result = run_eval(skill_creator_root, None)
    results.append(
        {
            "label": variants_data["baseline_label"],
            "description": baseline_result["description"],
            "passed": baseline_result["summary"]["passed"],
            "total": baseline_result["summary"]["total"],
            "results": baseline_result["results"],
        }
    )

    for variant in variants_data["variants"]:
        result = run_eval(skill_creator_root, variant["description"])
        results.append(
            {
                "label": variant["label"],
                "description": variant["description"],
                "passed": result["summary"]["passed"],
                "total": result["summary"]["total"],
                "results": result["results"],
            }
        )

    best = max(results, key=lambda item: (item["passed"], item["label"] == variants_data["baseline_label"]))
    summary = {
        "results_dir": str(results_dir.relative_to(ROOT)),
        "baseline": variants_data["baseline_label"],
        "best_label": best["label"],
        "scores": {item["label"]: f"{item['passed']}/{item['total']}" for item in results},
    }
    (results_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (results_dir / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
