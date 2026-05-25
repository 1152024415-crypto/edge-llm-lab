# Experiment Record Template

Use this template for each run. Store the completed record beside the run output, for example `results/<run-id>/record.md`.

## Identity

- Run ID:
- Date:
- Experiment:
- Question:
- Commit:

## Environment

- Machine:
- CPU:
- GPU:
- NPU:
- RAM:
- OS build:
- Power mode:
- Driver versions:
- Runtime versions:
- Python version:
- Package versions:

## Model

- Model name:
- Source:
- Revision or hash:
- License:
- Tokenizer:
- Chat template:
- Special tokens and stop rules:

## Configuration

- Runtime:
- Backend:
- Precision:
- Quantization method:
- Skipped layers:
- Mixed precision choices:
- Calibration data:
- Context length:
- Prompt set:
- Sampling parameters:
- Random seed:

## Commands

```powershell
# Export command

# Run command
```

## Results

- Output path:
- stdout/stderr path:
- Metrics path:
- Model size:
- Load time:
- Compile time:
- TTFT:
- Prefill latency:
- Decode tokens/sec:
- Total time:
- Peak memory:
- Actual device path:
- Fallback observed:

## Quality Gate

- Correctness:
- Quantization:
- Heterogeneous execution:
- Speculative decoding:
- Operator compatibility:
- Resource use:

## Conclusion

- Status:
- What worked:
- What failed:
- Likely cause:
- Next diagnostic step:
