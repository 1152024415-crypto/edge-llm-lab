# OpenVINO Source Reading Notes

## Current Focus

Phase 0 uses OpenVINO only for device discovery. It does not compile or execute an LLM.

## Device Discovery Path

The Phase 0 script calls:

```python
import openvino as ov

core = ov.Core()
devices = core.available_devices
core.get_property(device, "FULL_DEVICE_NAME")
core.get_property(device, "OPTIMIZATION_CAPABILITIES")
core.get_property(device, "SUPPORTED_PROPERTIES")
```

OpenVINO documents `Core.available_devices` and `Core.get_available_devices()` as returning devices available for inference by going over registered plugins. The returned names can later be used with `compile_model`, `query_model`, `set_property`, and related Core methods.

Official docs:

- OpenVINO Python `Core`: https://docs.openvino.ai/2024/api/ie_python_api/_autosummary/openvino.Core.html
- Inference device enumeration: https://docs.openvino.ai/2023.3/openvino_docs_OV_UG_Working_with_devices.html
- Plugin extensibility docs: https://docs.openvino.ai/2024/documentation/openvino-extensibility/openvino-plugin-library/plugin.html

## Local Plugin Libraries

The local `uv` environment installed these OpenVINO plugin libraries:

- `.venv/Lib/site-packages/openvino/libs/openvino_intel_cpu_plugin.dll`
- `.venv/Lib/site-packages/openvino/libs/openvino_intel_gpu_plugin.dll`
- `.venv/Lib/site-packages/openvino/libs/openvino_intel_npu_plugin.dll`
- `.venv/Lib/site-packages/openvino/libs/openvino_intel_npu_compiler.dll`
- `.venv/Lib/site-packages/openvino/libs/openvino_auto_plugin.dll`
- `.venv/Lib/site-packages/openvino/libs/openvino_hetero_plugin.dll`

These libraries are the runtime-side implementation boundary. The Python API asks `ov.Core`; `ov.Core` talks to registered plugins; plugins query or use the relevant driver/runtime stack.

## What Phase 0 Proved

- The Python package imports.
- OpenVINO Core can load or access CPU, GPU, and NPU plugins.
- Device names and capabilities can be queried without error.
- On this machine, OpenVINO reports:
  - `CPU`: Intel Core Ultra 5 125H
  - `GPU`: Intel Arc Graphics (iGPU)
  - `NPU`: Intel AI Boost

## What Phase 0 Did Not Prove

- It did not prove that any LLM can compile on GPU or NPU.
- It did not prove that INT4 or INT8 LLM inference works.
- It did not prove that a later model run will avoid fallback.
- It did not measure performance, memory, power, or output quality.

## System API Boundary

Phase 0 does not directly call Windows device APIs from our code. The direct system interaction in our code is limited to:

- PowerShell/CIM inventory for CPU, GPU, OS, RAM, and visible NPU-like devices.
- OpenVINO Python API for plugin-level device discovery.

The lower-level OS or driver APIs are behind OpenVINO plugins:

- CPU plugin uses CPU runtime capabilities and threading libraries.
- GPU plugin depends on Intel GPU driver/runtime support.
- NPU plugin depends on the Intel NPU driver and NPU compiler/runtime path.

OpenVINO's NPU configuration docs state that the NPU device requires a proper driver. On Windows, the Intel NPU driver is delivered through Windows Update or a manual driver package. Official docs: https://docs.openvino.ai/nightly/get-started/install-openvino/configurations/configurations-intel-npu.html

## Reading Targets

For device discovery, read in this order:

1. Python `Core.available_devices` documentation.
2. OpenVINO device enumeration docs.
3. Plugin docs for `ov::available_devices`, `ov::device::full_name`, and `ov::device::capabilities`.
4. Local package plugin libraries to understand what binary components are installed.
5. Upstream OpenVINO repository for `Core`, plugin registration, CPU plugin, GPU plugin, and NPU plugin implementation.

## Next Source Questions

- Where does `ov.Core()` load plugin metadata from in the Python wheel?
- How does each plugin implement `AVAILABLE_DEVICES` and `FULL_DEVICE_NAME`?
- For `compile_model(model, "NPU")`, where does OpenVINO hand the graph to the NPU compiler?
- How can we prove actual execution device after model compilation?
