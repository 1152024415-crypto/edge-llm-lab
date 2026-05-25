# Quality Gates

Quality gates decide whether an experiment result can support a conclusion. Passing a gate does not prove production readiness; it means the result is interpretable.

## Baseline Gate

- A reference or deployment baseline exists.
- The model source, tokenizer, prompt set, decode settings, and backend are fixed.
- Baseline output and metrics are saved.

## Correctness Gate

- Output is non-empty.
- Text decodes cleanly.
- Required output format is followed.
- No obvious repetition loop, garbled text, or premature stop appears.
- Candidate output is compared with baseline output.

## Quantization Gate

- Precision format is recorded, such as INT8, INT4, W4A16, or W8A8.
- Skipped layers and mixed precision choices are recorded.
- Calibration data is recorded when used.
- Model size, speed, and output quality are compared with baseline.
- Any quality recovery trick is documented.

## Heterogeneous Execution Gate

- Requested backend and actual execution path are recorded.
- CPU/GPU/NPU/AUTO/MULTI/HETERO fallback is checked.
- Cross-device movement or partitioning evidence is captured when available.
- Numeric or output drift is compared with baseline.
- If actual backend execution cannot be proven, do not claim that backend succeeded.

## Speculative Decoding Gate

- Target model and draft model are recorded.
- Tokenizer compatibility is checked.
- Acceptance behavior is recorded if the runtime exposes it.
- Speed, memory cost, and output drift are compared with non-speculative baseline.

## Operator Gate

- Unsupported or unknown operators are recorded with full error text.
- First try native runtime support, export options, or static shape changes.
- Then try graph rewrite or decomposition into supported primitives.
- Use a custom op only when the learning value justifies backend-specific work.

## Result Gate

- Cold and warm measurements are separated when relevant.
- TTFT, decode tokens/sec, total time, and peak memory are recorded.
- Failures are classified as environment, download, export, compile, operator, fallback, memory, quality, performance, thermal, or power related.
