from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from edge_llm_lab.phase1.export import build_export_command


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a Hugging Face LLM to OpenVINO IR.")
    parser.add_argument("--model-id", default="Qwen/Qwen2.5-0.5B-Instruct")
    parser.add_argument(
        "--output-dir",
        default=PROJECT_ROOT / "models/openvino/qwen2.5-0.5b-instruct-fp16",
        type=Path,
    )
    parser.add_argument("--weight-format", default="fp16", choices=["fp16", "int8", "int4"])
    parser.add_argument("--trust-remote-code", action="store_true")
    args = parser.parse_args()

    env = os.environ.copy()
    env.setdefault("HF_HOME", str(PROJECT_ROOT / ".cache/huggingface"))
    env.setdefault("HF_HUB_CACHE", str(PROJECT_ROOT / ".cache/huggingface/hub"))

    command = build_export_command(
        model_id=args.model_id,
        output_dir=args.output_dir,
        cache_dir=PROJECT_ROOT / ".cache/huggingface",
        weight_format=args.weight_format,
        trust_remote_code=args.trust_remote_code,
    )

    args.output_dir.parent.mkdir(parents=True, exist_ok=True)
    print(" ".join(command))
    completed = subprocess.run(command, cwd=PROJECT_ROOT, env=env, check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
