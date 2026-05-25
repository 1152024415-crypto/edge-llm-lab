# Phase 0 Summary

## Run

- Run ID: `phase0-20260525-144624`
- Command:

```powershell
$env:UV_CACHE_DIR='D:\proj\edge-llm-lab\.cache\uv'
uv run --python 3.12 experiments\intel-openvino-1b\scripts\run-phase0.py
```

## Result

- Status: completed
- Model downloaded: no
- LLM executed: no
- OpenVINO version: `2026.1.0-21367-63e31528c62-releases/2026/1`
- OpenVINO devices visible: `CPU`, `GPU`, `NPU`

## Hardware Snapshot

- CPU: Intel Core Ultra 5 125H, 14 cores, 18 logical processors
- GPU: Intel Arc Graphics, driver `31.0.101.5382`
- NPU candidate: Intel AI Boost, PNP class `ComputeAccelerator`
- RAM: about 32 GB

## Local Result Files

These files are generated locally and intentionally ignored by git:

- `results/phase0-20260525-144624/record.md`
- `results/phase0-20260525-144624/environment.json`
- `results/phase0-20260525-144624/openvino-devices.json`

## Interpretation

Phase 1 can start with an OpenVINO CPU baseline. GPU and NPU are visible to OpenVINO, but they are not proven usable for LLM inference yet. Backend success must be validated with model execution and fallback checks in later phases.

## Mechanism

Phase 0 used OpenVINO Runtime's Python API:

```python
import openvino as ov

core = ov.Core()
core.available_devices
core.get_property(device, "FULL_DEVICE_NAME")
core.get_property(device, "OPTIMIZATION_CAPABILITIES")
```

`Core.available_devices` is a framework-level device discovery call. It asks OpenVINO Core to enumerate devices exposed by registered device plugins. In this local environment, the relevant plugin binaries are installed under `.venv/Lib/site-packages/openvino/libs/`, including CPU, GPU, NPU, AUTO, and HETERO plugins.

This does not directly prove that an LLM can run on NPU. It proves that OpenVINO can see the NPU plugin and query basic device properties. Real backend execution must be checked later with `compile_model`, runtime logs/properties, output comparison, and fallback checks.

Source-reading note: see `docs/openvino-source-reading.md`.
