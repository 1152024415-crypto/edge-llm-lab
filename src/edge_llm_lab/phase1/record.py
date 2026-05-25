from __future__ import annotations


def render_cpu_baseline_summary(
    *,
    run_id: str,
    model_id: str,
    model_path: str,
    results_path: str,
    prompt_count: int,
    openvino_version: str,
    status: str,
) -> str:
    return f"""# Phase 1 CPU Baseline Summary

## Scope

- Run ID: `{run_id}`
- Status: {status}
- Device: CPU only
- Model: `{model_id}`
- OpenVINO version: `{openvino_version}`
- Converted model path: `{model_path}`
- Result file: `{results_path}`
- Prompt count: {prompt_count}

## What This Proves

This phase proves that the selected 0.5B/1B model can be loaded through OpenVINO GenAI and generate text on the CPU backend with fixed prompts and generation settings.

## What This Does Not Prove

This phase does not prove GPU, NPU, AUTO, MULTI, HETERO, quantization, speculative decoding, or fallback behavior. Those require separate quality gates.

## Teaching Focus

- Hugging Face model artifacts are converted to OpenVINO IR before deployment.
- OpenVINO GenAI owns tokenization, generation loop, KV cache handling, and output decoding for this baseline.
- The CPU backend is the reference deployment baseline for later optimization phases.
"""
