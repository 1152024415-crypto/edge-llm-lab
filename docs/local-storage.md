# Local Storage Policy

The first phase should stay small: 0.5B/1B models only. Plan for about 10-15 GB of local storage, with extra room if multiple quantized exports are kept.

## Python

Use `uv` for Python setup and execution. Prefer a project-local virtual environment:

```powershell
uv venv .venv
uv run python --version
```

If using a cache override, keep it under this project, for example `.cache/uv`.

## Models and Caches

Keep local artifacts inside the project when practical:

- Hugging Face cache: `.cache/huggingface/`
- raw model references or downloaded artifacts: `models/`
- OpenVINO exports: `models/openvino/`
- benchmark and run outputs: `results/` or `experiments/<name>/results/`

Document any external path in the experiment record.

## Git Policy

Do not commit or push:

- model weights
- caches
- large exported models
- raw logs
- secrets or API tokens

Only commit concise docs, scripts, configs, and curated summaries.
