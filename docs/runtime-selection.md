# Runtime Selection

This project uses two tracks:

1. A portable GGUF track for learning the common deployment mechanics.
2. A Windows + Intel OpenVINO track for hardware-specific validation.

The portable track should come first. It keeps the first learning loop focused on model files, prompts, decoding settings, quantization, result records, and quality gates before adding vendor runtime and driver complexity.

## Why GGUF First

GGUF plus llama.cpp is the common baseline because it is portable across many local deployment environments and exposes the core mechanics directly:

- the model artifact is a single GGUF file with metadata and tensors
- quantized variants can be compared against a clear high-precision or less-quantized baseline
- llama.cpp exposes CPU execution, prompt processing speed, generation speed, context settings, and server mode
- speculative decoding can be tested with llama.cpp before introducing vendor-specific runtime behavior
- failures usually start from model format, tokenizer/template, prompt settings, quantization, memory, or unsupported architecture

Ollama is useful as an application-layer smoke test because it wraps model download, model management, and serving into a simple user workflow. It should not be the primary source for low-level benchmark conclusions because it intentionally hides runtime details.

## Why Keep OpenVINO

OpenVINO remains the Intel-specific track. It is useful for learning:

- OpenVINO IR export
- OpenVINO GenAI pipeline behavior
- CPU, GPU, NPU, AUTO, MULTI, and HETERO device selection
- plugin and driver boundaries
- fallback detection
- Intel NPU limits and failure modes

The existing OpenVINO Phase 0 and Phase 1 work is still valid. It should be treated as the first Intel-specific baseline, not as the universal project baseline.

## Recommended Order

1. Common GGUF CPU baseline with llama.cpp.
2. GGUF quantization comparison, such as Q8 then Q4.
3. Ollama smoke test using the same model family and prompt intent when practical.
4. llama.cpp speculative decoding, first without a draft model when possible, then with a compatible draft model.
5. Operator diagnostics: identify unsupported model/runtime/operator issues and try native support, conversion options, or graph decomposition before custom operators.
6. Intel OpenVINO comparison: CPU baseline, quantized OpenVINO, GPU validation, NPU smoke test, then heterogeneous execution.

## Decision Rules

- Use GGUF and llama.cpp when the question is about common local LLM deployment mechanics.
- Use Ollama when the question is about end-user local serving or app integration.
- Use OpenVINO when the question is about Intel hardware acceleration, OpenVINO IR, plugins, NPU behavior, or fallback evidence.
- Do not compare runtimes until each runtime has its own baseline and quality gate.
- Do not claim acceleration worked unless execution path, fallback behavior, and key metrics are recorded.

## Source Reading Path

- llama.cpp README for supported backends, GGUF usage, and CLI/server entry points.
- llama.cpp quantization tool documentation for GGUF quantization.
- llama.cpp speculative decoding documentation for n-gram and draft-model approaches.
- Ollama Windows documentation for local installation and serving behavior.
- OpenVINO GenAI `LLMPipeline` documentation for Intel-specific inference.
