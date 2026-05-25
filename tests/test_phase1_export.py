from pathlib import Path

from edge_llm_lab.phase1.export import build_export_command


def test_build_export_command_uses_text_generation_task_and_project_cache():
    command = build_export_command(
        model_id="Qwen/Qwen2.5-0.5B-Instruct",
        output_dir=Path("models/openvino/qwen2.5-0.5b-instruct-fp16"),
        cache_dir=Path(".cache/huggingface"),
        weight_format="fp16",
        trust_remote_code=False,
    )

    assert command == [
        "optimum-cli",
        "export",
        "openvino",
        "--model",
        "Qwen/Qwen2.5-0.5B-Instruct",
        "--task",
        "text-generation-with-past",
        "--weight-format",
        "fp16",
        "--cache_dir",
        str(Path(".cache/huggingface")),
        str(Path("models/openvino/qwen2.5-0.5b-instruct-fp16")),
    ]


def test_build_export_command_can_enable_trust_remote_code():
    command = build_export_command(
        model_id="custom/model",
        output_dir=Path("models/openvino/custom"),
        cache_dir=Path(".cache/huggingface"),
        weight_format="fp16",
        trust_remote_code=True,
    )

    assert "--trust-remote-code" in command
