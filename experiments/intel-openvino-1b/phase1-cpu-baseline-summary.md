# Phase 1 CPU Baseline Summary

## Run

- Run ID: `phase1-cpu-20260525-153607`
- Model: `Qwen/Qwen2.5-0.5B-Instruct`
- Exported model: `models/openvino/qwen2.5-0.5b-instruct-fp16`
- Device: `CPU`
- Decode method: greedy
- Prompt set: `experiments/intel-openvino-1b/prompts/baseline-prompts.json`
- Result file: `results/phase1-cpu-20260525-153607/results.json`

## Commands

```powershell
$env:UV_CACHE_DIR='D:\proj\edge-llm-lab\.cache\uv'
$env:HF_HOME='D:\proj\edge-llm-lab\.cache\huggingface'
$env:HF_HUB_CACHE='D:\proj\edge-llm-lab\.cache\huggingface\hub'
uv run --python 3.12 experiments\intel-openvino-1b\scripts\export-openvino-model.py
uv run --python 3.12 experiments\intel-openvino-1b\scripts\run-cpu-baseline.py
```

## Result

- Status: completed
- OpenVINO version: `2026.1.0-21367-63e31528c62-releases/2026/1`
- OpenVINO GenAI version: `2026.1.0.0`
- Converted FP16 model size: about 1.01 GB
- Model load time: about 1.24 seconds
- Prompt count: 4
- Quality gate: all prompts passed

| Prompt | Expected Format | Generation Time | Quality |
|---|---|---:|---|
| `zh-edge-llm-short` | plain text | 4.06s | pass |
| `en-quantization` | plain text | 3.70s | pass |
| `json-format` | JSON object | 1.39s | pass |
| `debugging` | plain text | 3.95s | pass |

## Issues Encountered

- Hugging Face download timed out once and resumed automatically.
- Windows Hugging Face cache symlink support is degraded without Developer Mode or administrator privileges, so the local cache may use more disk space.
- OpenVINO/Torch tracing warnings appeared during export. The export still completed.
- Passing `temperature=0.0` to OpenVINO GenAI failed because sampling temperature must be positive. The baseline now uses greedy decoding by omitting sampling parameters.
- The first JSON prompt returned Markdown fenced JSON. The prompt and quality gate were tightened so the baseline requires a strict JSON object.

## Mechanism

The export step uses Optimum Intel to load the Hugging Face model and convert it into OpenVINO IR with tokenizer/detokenizer artifacts. The runtime step uses `openvino_genai.LLMPipeline(model_path, "CPU")`, which loads the converted model directory and runs token generation through OpenVINO Runtime on the CPU backend.

OpenVINO GenAI sits above OpenVINO Runtime. It handles tokenizer/detokenizer use, generation loop control, generation config validation, and KV-cache/state management. The CPU plugin executes the compiled graph behind the pipeline.

## What This Proves

- The selected 0.5B model can be converted to OpenVINO FP16 format.
- The converted model can generate text through OpenVINO GenAI on CPU.
- The fixed prompt set can be evaluated with simple correctness and format quality gates.

## What This Does Not Prove

- GPU or NPU execution.
- Quantized INT8/INT4 behavior.
- Fallback behavior.
- Numerical equivalence to PyTorch or another reference runtime.
- Speculative decoding behavior.

## Next Step

Phase 2 should add a reference comparison layer: capture the CPU baseline outputs as reference, then run a small INT8 or INT4 export and compare size, output quality, and generation timing.

Source-reading note: see `docs/openvino-genai-source-reading.md`.
