from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from edge_llm_lab.phase0.inventory import collect_environment, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect Phase 0 environment inventory.")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--project-root", default=project_root(), type=Path)
    args = parser.parse_args()

    snapshot = collect_environment(
        project_root=args.project_root,
        python_executable=sys.executable,
    )
    write_json(args.output, snapshot)
    return 0


def project_root() -> Path:
    return PROJECT_ROOT


if __name__ == "__main__":
    raise SystemExit(main())
