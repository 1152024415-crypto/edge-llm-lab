from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from edge_llm_lab.phase0.inventory import collect_environment, merge_failures, write_json
from edge_llm_lab.phase0.openvino_devices import collect_openvino_devices
from edge_llm_lab.phase0.record import render_phase0_record


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Phase 0 inventory and OpenVINO checks.")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--project-root", default=project_root(), type=Path)
    args = parser.parse_args()

    run_id = args.run_id or datetime.now().strftime("phase0-%Y%m%d-%H%M%S")
    run_dir = args.project_root / "results" / run_id
    environment_path = run_dir / "environment.json"
    devices_path = run_dir / "openvino-devices.json"
    record_path = run_dir / "record.md"

    environment = collect_environment(
        project_root=args.project_root,
        python_executable=sys.executable,
    )
    devices = collect_openvino_devices()
    failures = merge_failures(
        environment.get("failures", []),
        devices.get("errors", []),
    )

    write_json(environment_path, environment)
    write_json(devices_path, devices)
    record_path.write_text(
        render_phase0_record(
            run_id=run_id,
            environment_path=relative_to_project(environment_path, args.project_root),
            devices_path=relative_to_project(devices_path, args.project_root),
            devices=list(devices.get("available_devices", [])),
            failures=failures,
        ),
        encoding="utf-8",
    )

    print(f"run_id={run_id}")
    print(f"record={record_path}")
    print(f"devices={', '.join(devices.get('available_devices', [])) or 'none'}")
    return 0


def project_root() -> Path:
    return PROJECT_ROOT


def relative_to_project(path: Path, project_root: Path) -> str:
    return path.relative_to(project_root).as_posix()


if __name__ == "__main__":
    raise SystemExit(main())
