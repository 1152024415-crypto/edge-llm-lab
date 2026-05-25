from __future__ import annotations


def render_phase0_record(
    *,
    run_id: str,
    environment_path: str,
    devices_path: str,
    devices: list[str],
    failures: list[dict[str, object]],
) -> str:
    device_summary = ", ".join(devices) if devices else "none detected"
    status = "completed" if not failures else "completed-with-failures"
    failure_lines = render_failures(failures)
    return f"""# Phase 0 Record

## Identity

- Run ID: {run_id}
- Experiment: intel-openvino-1b
- Question: What hardware, software, and OpenVINO devices are visible before running an LLM?
- Status: {status}

## Outputs

- Environment: `{environment_path}`
- OpenVINO devices: `{devices_path}`

## Device Summary

- Available OpenVINO devices: {device_summary}

## Quality Gate

- Reproducibility: environment snapshot saved
- Heterogeneous execution: backend visibility recorded before model execution
- Result scope: no model was downloaded or executed in Phase 0

## Failures

{failure_lines}

## Next Step

Use this record to decide whether Phase 1 can run a CPU baseline directly or needs driver/runtime diagnostics first.
"""


def render_failures(failures: list[dict[str, object]]) -> str:
    if not failures:
        return "- None"
    return "\n".join(f"- `{item}`" for item in failures)

