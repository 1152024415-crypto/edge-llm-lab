# Intel OpenVINO 1B Experiment

This experiment is the first learning target for the lab: run a 1B-class LLM on the user's Intel Core Ultra laptop and learn the deployment workflow before expanding to other hardware stacks.

## Goal

Run a small LLM through OpenVINO, establish a baseline, test quantization, compare CPU/GPU/NPU behavior, and document failures in a way that can transfer to mobile and edge deployments.

## Initial Success Criteria

- A CPU baseline run is saved with prompt output and metrics.
- Intel GPU is tested with the same model and prompt set.
- Intel NPU is smoke-tested; failure is acceptable if the error and likely cause are recorded.
- At least one quantized variant is compared against baseline.
- Backend execution and fallback behavior are documented before any performance conclusion is made.

## Suggested First Models

- `TinyLlama/TinyLlama-1.1B-Chat-v1.0`
- `Qwen/Qwen2.5-0.5B-Instruct`

Start with the smallest model that exercises the pipeline. Do not move to 1.5B, 3B, or 7B models in this phase unless the user explicitly changes the scope.

## Phase 0

- [Phase 0 Summary](phase0-summary.md) - environment inventory and OpenVINO device visibility check.
