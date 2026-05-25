# Edge LLM Lab

This project is a Codex-maintained lab for learning and validating edge/on-device LLM deployment. The current first target is an Intel Core Ultra laptop, but the project should stay general enough to later cover NVIDIA, Qualcomm, Huawei, Android, iOS, and other runtimes.

## Project Structure

- `experiments/` contains runnable experiments. Each platform or stack gets its own subdirectory.
- `docs/` contains process notes, quality gates, troubleshooting notes, and experiment templates.
- `results/` contains generated run outputs, metrics, logs, and summaries.
- `models/` is for local model artifacts only. Do not commit model weights or large generated exports.
- `README.md` is the user-facing project index. Update it when major experiments or docs are added.

## Core Rules

- Keep experiments reproducible: every optimization must be comparable to a clear baseline.
- Treat deployment as more than speed: validate correctness, quality, resource use, fallback behavior, and reproducibility before drawing conclusions.
- Quantization, speculative decoding, heterogeneous execution, and custom operators must pass a quality gate before any performance claim is made.
- Do not claim a CPU/GPU/NPU/AUTO/MULTI/HETERO backend worked unless the actual execution path, fallback behavior, and key metrics are recorded.
- Preserve failures as useful evidence. Record the context, full error, likely failure class, and next diagnostic step.
- Do not commit model weights, caches, large exports, secrets, API tokens, or license-unclear files.
- Keep docs concise and practical. Put detailed commands and run metadata in experiment docs or result records, not in this file.
- Use `uv` for Python environments and Python command execution.
- Keep local artifacts inside this project when practical. Document any external cache, model, or result path.
- Current active scope is 0.5B/1B basic experiments. Do not expand to 3B/7B or vendor-specific stacks without an explicit request.

## Experiment Workflow

1. Define the question being tested.
2. Select the model, runtime, backend, precision, prompt set, and baseline.
3. Run the baseline first.
4. Apply one change at a time: quantization, backend change, speculative decoding, graph rewrite, or custom operator.
5. Run the quality gate and compare against the baseline.
6. Save result records under `results/` or the experiment's own `results/` directory.
7. Summarize what worked, what failed, and what should be tested next.

## Quality Gate Categories

- Correctness: output is non-empty, decodes cleanly, follows required format, and does not obviously regress from baseline.
- Quantization: precision mode, skipped layers, mixed precision choices, calibration data, and quality impact are recorded.
- Heterogeneous execution: actual devices, fallback, cross-device movement signs, numeric drift, and output differences are recorded.
- Speculative decoding: target model, draft model, tokenizer compatibility, acceptance behavior, speed impact, memory cost, and output drift are recorded.
- Operators: unsupported or new operators are handled by checking native support, export options, graph rewrites, primitive decomposition, then custom op only when justified.

## File Conventions

- Use lowercase kebab-case for experiment and doc filenames.
- Prefer small, focused docs over large manuals.
- Keep generated outputs out of source files unless they are short summaries.
- If a result supports a durable conclusion, link it from `README.md` or the relevant doc.

## Working Style

- Start from the existing README and relevant experiment docs before changing files.
- Keep changes scoped to the active experiment.
- State uncertainty clearly, especially for NPU support, fallback behavior, and benchmark conclusions.
- When in doubt, add a small diagnostic experiment rather than guessing.
