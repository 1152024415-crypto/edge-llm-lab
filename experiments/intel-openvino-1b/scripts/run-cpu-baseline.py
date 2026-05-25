from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from edge_llm_lab.phase1.generation import run_generation_pipeline, write_json
from edge_llm_lab.phase1.prompts import load_prompt_set
from edge_llm_lab.phase1.record import render_cpu_baseline_summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Phase 1 CPU baseline generation.")
    parser.add_argument(
        "--model-path",
        default=PROJECT_ROOT / "models/openvino/qwen2.5-0.5b-instruct-fp16",
        type=Path,
    )
    parser.add_argument(
        "--prompts",
        default=PROJECT_ROOT / "experiments/intel-openvino-1b/prompts/baseline-prompts.json",
        type=Path,
    )
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--temperature", default=None, type=float)
    parser.add_argument("--top-p", default=None, type=float)
    args = parser.parse_args()

    run_id = args.run_id or datetime.now().strftime("phase1-cpu-%Y%m%d-%H%M%S")
    run_dir = PROJECT_ROOT / "results" / run_id
    results_path = run_dir / "results.json"
    record_path = run_dir / "record.md"

    prompt_set = load_prompt_set(args.prompts)
    results = run_generation_pipeline(
        model_path=args.model_path,
        prompt_set=prompt_set,
        device="CPU",
        temperature=args.temperature,
        top_p=args.top_p,
    )
    write_json(results_path, results)

    status = "completed" if all(p["quality"]["passed"] for p in results["prompts"]) else "completed-with-quality-failures"
    record_path.write_text(
        render_cpu_baseline_summary(
            run_id=run_id,
            model_id="Qwen/Qwen2.5-0.5B-Instruct",
            model_path=args.model_path.relative_to(PROJECT_ROOT).as_posix(),
            results_path=results_path.relative_to(PROJECT_ROOT).as_posix(),
            prompt_count=len(prompt_set.prompts),
            openvino_version=str(results["openvino_version"]),
            status=status,
        ),
        encoding="utf-8",
    )
    print(f"run_id={run_id}")
    print(f"record={record_path}")
    print(f"results={results_path}")
    print(f"status={status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
