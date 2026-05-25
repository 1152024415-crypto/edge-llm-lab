from edge_llm_lab.phase0.openvino_devices import collect_openvino_devices


class FakeCore:
    available_devices = ["CPU", "GPU", "NPU"]

    def get_property(self, device, name):
        if name == "FULL_DEVICE_NAME":
            return f"{device} device"
        if name == "OPTIMIZATION_CAPABILITIES":
            return ["FP32", "INT8"]
        if name == "SUPPORTED_PROPERTIES":
            return ["FULL_DEVICE_NAME", "OPTIMIZATION_CAPABILITIES"]
        raise RuntimeError(f"unsupported property {name}")


def test_collect_openvino_devices_records_devices_and_properties():
    snapshot = collect_openvino_devices(
        core_factory=lambda: FakeCore(),
        openvino_version="2026.1.0",
    )

    assert snapshot["openvino_version"] == "2026.1.0"
    assert snapshot["available_devices"] == ["CPU", "GPU", "NPU"]
    assert snapshot["devices"]["NPU"]["properties"]["FULL_DEVICE_NAME"] == "NPU device"
    assert snapshot["devices"]["GPU"]["properties"]["OPTIMIZATION_CAPABILITIES"] == [
        "FP32",
        "INT8",
    ]
    assert snapshot["errors"] == []
