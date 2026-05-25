from __future__ import annotations

from pathlib import Path


def build_export_command(
    *,
    model_id: str,
    output_dir: Path,
    cache_dir: Path,
    weight_format: str,
    trust_remote_code: bool,
) -> list[str]:
    command = [
        "optimum-cli",
        "export",
        "openvino",
        "--model",
        model_id,
        "--task",
        "text-generation-with-past",
        "--weight-format",
        weight_format,
        "--cache_dir",
        str(cache_dir),
    ]
    if trust_remote_code:
        command.append("--trust-remote-code")
    command.append(str(output_dir))
    return command
