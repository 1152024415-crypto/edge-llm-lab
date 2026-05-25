# OpenVINO GenAI Source Reading Notes

## Current Focus

Phase 1 uses OpenVINO GenAI for CPU text generation with a converted Hugging Face LLM.

## Conversion Path

The model conversion command follows the OpenVINO GenAI model preparation guide:

```powershell
optimum-cli export openvino --model Qwen/Qwen2.5-0.5B-Instruct --task text-generation-with-past --weight-format fp16 models/openvino/qwen2.5-0.5b-instruct-fp16
```

Official docs:

- Convert models to OpenVINO format: https://openvinotoolkit.github.io/openvino.genai/docs/guides/model-preparation/convert-to-openvino/
- Text generation with LLMs: https://openvinotoolkit.github.io/openvino.genai/docs/use-cases/text-generation/

## Runtime Path

The Phase 1 baseline uses:

```python
import openvino_genai as ov_genai

pipe = ov_genai.LLMPipeline(model_path, "CPU")
output = pipe.generate(prompt, max_new_tokens=96)
```

OpenVINO GenAI's LLM pipeline loads the converted model directory, tokenizer, detokenizer, and generation configuration. It then runs token-by-token generation through OpenVINO Runtime on the selected backend.

## What GenAI Adds Above OpenVINO Runtime

OpenVINO Runtime can compile and execute graphs. OpenVINO GenAI adds LLM-specific orchestration:

- tokenizer and detokenizer handling
- generation loop
- generation parameters such as `max_new_tokens`, `temperature`, `top_p`, and beam settings
- KV-cache/state handling for efficient autoregressive decoding
- higher-level pipeline APIs for text generation, chat, streaming, and speculative decoding

The OpenVINO GenAI concept docs explain that LLMs can be transformed to a stateful form, hiding KV-cache inputs and outputs and storing cache state in OpenVINO model state during generation.

Official docs:

- How OpenVINO GenAI works: https://openvinotoolkit.github.io/openvino.genai/docs/concepts/how-it-works/
- `LLMPipeline` API: https://docs.openvino.ai/2026/api/genai_api/_autosummary/openvino_genai.LLMPipeline.html

## Local Observations

- The converted FP16 model directory is about 1.01 GB.
- The directory contains OpenVINO model files, tokenizer files, detokenizer files, config files, and generation config.
- CPU baseline generation worked with greedy decoding when no sampling parameters were passed.
- Passing `temperature=0.0` caused OpenVINO GenAI to reject the generation config because sampling temperature must be positive.
- The JSON format prompt initially failed because the model returned Markdown fenced JSON; making the prompt explicit and enforcing a strict JSON quality gate produced a passing baseline.

## Source Reading Targets

Read in this order:

1. OpenVINO GenAI `LLMPipeline` API.
2. OpenVINO GenAI text-generation sample.
3. OpenVINO GenAI "How It Works" concept page for stateful LLM and KV-cache handling.
4. Upstream OpenVINO GenAI source for `LLMPipeline`, generation config validation, tokenizer/detokenizer, and streamer support.
5. OpenVINO Runtime source for compiled model, infer request, state API, and CPU plugin execution.

## Boundary

Phase 1 proves CPU generation through OpenVINO GenAI. It does not prove GPU/NPU execution, quantized model behavior, fallback detection, or speculative decoding behavior.
