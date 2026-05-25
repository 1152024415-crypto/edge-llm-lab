# Common GGUF 0.5B Experiment

This experiment is the portable baseline track for the lab. It should teach the common mechanics of local LLM deployment before the project makes Intel-specific claims.

## Goal

Run a 0.5B/1B-class instruction model from GGUF with llama.cpp, establish a CPU baseline, compare quantized GGUF variants, and use the same quality-gate style as the Intel OpenVINO track.

## Why This Comes First

The common GGUF track separates general deployment learning from hardware-specific runtime behavior. A working GGUF baseline answers basic questions before OpenVINO, GPU, NPU, or heterogeneous execution are introduced:

- Which model and tokenizer/template are being used?
- Which prompt set and decode settings are fixed?
- What is the reference output quality?
- What are the baseline model size, load behavior, prompt processing speed, and generation speed?
- What changes when only quantization changes?

## Initial Success Criteria

- A CPU baseline run is saved with prompt output and metrics.
- The model source, GGUF file, quantization format, prompt set, decode settings, and llama.cpp version are recorded.
- At least one quantized variant is compared against the baseline.
- The JSON prompt passes a strict format gate or the failure is preserved with diagnosis.
- Ollama is used only as a smoke test after the llama.cpp baseline is understood.

## Suggested First Models

- `Qwen/Qwen2.5-0.5B-Instruct` GGUF variant
- Another 0.5B/1B GGUF instruction model only if it is easier to obtain and has clear licensing

Do not move to 3B or 7B models in this track unless the scope is explicitly changed.

## Planned Phases

### Phase 1: llama.cpp CPU Baseline

Run a GGUF model on CPU with fixed prompts and greedy or otherwise fixed decode settings. Record model path, runtime version, command, prompt outputs, timing, and quality-gate results.

### Phase 2: GGUF Quantization

Compare one quantized GGUF variant against the Phase 1 baseline. Start with Q8 or Q4, but change only one variable at a time. Record size, speed, memory, output quality, and JSON format behavior.

### Phase 3: Ollama Smoke Test

Run the same model family through Ollama when practical. Treat this as an application-layer usability check, not the source of low-level backend claims.

### Phase 4: Speculative Decoding

Use llama.cpp speculative decoding after the non-speculative baseline is stable. Record the target model, draft strategy or draft model, tokenizer compatibility, acceptance behavior when available, speed, memory, and output drift.

### Phase 5: Operator Diagnostics

If a model or runtime path fails because of architecture or operator support, record the full failure and work through native support, conversion options, graph rewrite, and primitive decomposition before considering custom operators.
