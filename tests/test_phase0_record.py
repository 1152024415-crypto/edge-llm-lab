from edge_llm_lab.phase0.record import render_phase0_record


def test_render_phase0_record_links_outputs_and_device_summary():
    markdown = render_phase0_record(
        run_id="phase0-20260525-120000",
        environment_path="results/phase0-20260525-120000/environment.json",
        devices_path="results/phase0-20260525-120000/openvino-devices.json",
        devices=["CPU", "GPU", "NPU"],
        failures=[],
    )

    assert "# Phase 0 Record" in markdown
    assert "phase0-20260525-120000" in markdown
    assert "CPU, GPU, NPU" in markdown
    assert "environment.json" in markdown
    assert "openvino-devices.json" in markdown
    assert "Status: completed" in markdown
