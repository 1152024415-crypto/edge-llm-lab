from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from edge_llm_lab.phase0.inventory import write_json
from edge_llm_lab.phase0.openvino_devices import collect_openvino_devices


def main() -> int:
    parser = argparse.ArgumentParser(description="Check OpenVINO visible devices.")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    snapshot = collect_openvino_devices()
    write_json(args.output, snapshot)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
