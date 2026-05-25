# Edge LLM Lab

This lab is for learning edge/on-device LLM deployment through small, reproducible experiments. The first target is a 1B-class model on an Intel Core Ultra laptop using OpenVINO, but the project is intentionally general enough to later cover NVIDIA, Qualcomm, Huawei, Android, iOS, and other deployment stacks.

## First Experiment

- `experiments/intel-openvino-1b/` - baseline 1B LLM deployment on Intel CPU/GPU/NPU with OpenVINO.

Current status:

- Phase 0 inventory is complete: OpenVINO sees `CPU`, `GPU`, and `NPU`.
- See `experiments/intel-openvino-1b/phase0-summary.md`.

## Current Scope

- Python environment: use `uv`.
- Model size: only 0.5B/1B-class basic experiments for now.
- Storage: keep virtualenvs, caches, model artifacts, exported models, and results inside this project when practical.
- Git: do not push model weights, large exports, caches, raw logs, or secrets.

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
- `docs/teaching-method.md` - how each experiment should teach mechanisms and debugging.
- `docs/openvino-source-reading.md` - source-reading notes for OpenVINO runtime and plugins.
- `docs/quality-gates.md` - practical quality gates for deployment experiments.

## Local Artifact Policy

Model weights, caches, large exported models, generated logs, and raw benchmark outputs should stay local and out of git unless explicitly curated into a small summary.
