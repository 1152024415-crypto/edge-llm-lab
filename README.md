# Edge LLM Lab

This lab is for learning edge/on-device LLM deployment through small, reproducible experiments. The project starts with a portable GGUF baseline so the core deployment concepts are not tied to one vendor stack, then uses an Intel Core Ultra laptop as the first hardware-specific optimization target.

## Experiment Tracks

- `experiments/common-gguf-0.5b/` - portable GGUF baseline with llama.cpp and Ollama-oriented smoke tests.
- `experiments/intel-openvino-1b/` - Intel CPU/GPU/NPU deployment with OpenVINO and OpenVINO GenAI.

Current status:

- Intel OpenVINO Phase 0 inventory is complete: OpenVINO sees `CPU`, `GPU`, and `NPU`.
- Intel OpenVINO Phase 1 CPU baseline is complete for `Qwen/Qwen2.5-0.5B-Instruct`.
- The next priority is the common GGUF CPU baseline, not another Intel-specific optimization.
- See `experiments/intel-openvino-1b/phase0-summary.md`.
- See `experiments/intel-openvino-1b/phase1-cpu-baseline-summary.md`.

## Current Scope

- Python environment: use `uv`.
- Model size: only 0.5B/1B-class basic experiments for now.
- Storage: keep virtualenvs, caches, model artifacts, exported models, and results inside this project when practical.
- Git: do not push model weights, large exports, caches, raw logs, or secrets.
- Route order: establish the common GGUF baseline first, then compare Intel-specific OpenVINO, GPU, NPU, and heterogeneous execution paths.

## Core Topics

- Baseline inference and reproducibility
- Framework architecture and source reading
- INT8, INT4, W4A16, mixed precision, and layer exclusion
- CPU/GPU/NPU backend validation and fallback detection
- Speculative decoding
- Unsupported operators and custom operator decisions
- Quality gates for correctness, performance, resources, and deployability

## Key Docs

- `AGENTS.md` - project operating rules for Codex.
- `docs/experiment-record.md` - template for recording hardware, software, model, command, prompt, and result metadata.
- `docs/local-storage.md` - local storage and cache policy.
- `docs/runtime-selection.md` - why the project now starts with a portable GGUF baseline before vendor-specific stacks.
- `docs/teaching-method.md` - how each experiment should teach mechanisms and debugging.
- `docs/openvino-source-reading.md` - source-reading notes for OpenVINO runtime and plugins.
- `docs/openvino-genai-source-reading.md` - source-reading notes for OpenVINO GenAI LLM generation.
- `docs/quality-gates.md` - practical quality gates for deployment experiments.

## Local Artifact Policy

Model weights, caches, large exported models, generated logs, and raw benchmark outputs should stay local and out of git unless explicitly curated into a small summary.
