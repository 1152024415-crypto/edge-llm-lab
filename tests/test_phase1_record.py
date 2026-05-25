from edge_llm_lab.phase1.record import render_cpu_baseline_summary


def test_render_cpu_baseline_summary_records_scope_and_paths():
    markdown = render_cpu_baseline_summary(
        run_id="phase1-cpu-20260525-150000",
        model_id="Qwen/Qwen2.5-0.5B-Instruct",
        model_path="models/openvino/qwen2.5-0.5b-instruct-fp16",
        results_path="results/phase1-cpu-20260525-150000/results.json",
        prompt_count=4,
        openvino_version="2026.1.0",
        status="completed",
    )

    assert "# Phase 1 CPU Baseline Summary" in markdown
    assert "Qwen/Qwen2.5-0.5B-Instruct" in markdown
    assert "CPU only" in markdown
    assert "results/phase1-cpu-20260525-150000/results.json" in markdown
    assert "4" in markdown
