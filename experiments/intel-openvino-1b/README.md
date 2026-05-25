# Intel OpenVINO 1B Experiment

This experiment is the Windows + Intel hardware-specific track for the lab. It validates OpenVINO and OpenVINO GenAI behavior on an Intel Core Ultra laptop after the common GGUF route defines a portable baseline.

## Goal

Run a small LLM through OpenVINO, compare CPU/GPU/NPU behavior, test OpenVINO quantization, and document fallback or failure evidence in a way that can be compared with the common GGUF baseline.

This track should not be treated as the universal baseline. Its job is to answer Intel-specific questions about OpenVINO IR, OpenVINO GenAI, runtime plugins, drivers, NPU limitations, and backend execution evidence.

## Initial Success Criteria

- A CPU baseline run is saved with prompt output and metrics.
- Intel GPU is tested with the same model and prompt set.
- Intel NPU is smoke-tested; failure is acceptable if the error and likely cause are recorded.
- At least one quantized variant is compared against baseline.
- Backend execution and fallback behavior are documented before any performance conclusion is made.
- Results are compared with the common GGUF track when a matching model and prompt set exist.

## Suggested First Models

- `TinyLlama/TinyLlama-1.1B-Chat-v1.0`
- `Qwen/Qwen2.5-0.5B-Instruct`

Start with the smallest model that exercises the pipeline. Do not move to 1.5B, 3B, or 7B models in this phase unless the user explicitly changes the scope.

## Phase 0

- [Phase 0 Summary](phase0-summary.md) - environment inventory and OpenVINO device visibility check.

## Phase 1

- [Phase 1 CPU Baseline Summary](phase1-cpu-baseline-summary.md) - OpenVINO GenAI CPU baseline with `Qwen/Qwen2.5-0.5B-Instruct`.

## Next Position in Roadmap

Pause Intel-specific optimization until the common GGUF CPU baseline and first GGUF quantization comparison exist. After that, return here to compare OpenVINO CPU, OpenVINO quantization, GPU, NPU, and heterogeneous execution against the portable baseline.
