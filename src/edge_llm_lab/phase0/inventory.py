from __future__ import annotations

import json
import platform
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable, Sequence


@dataclass(frozen=True)
class CommandResult:
    returncode: int
    stdout: str
    stderr: str

    def to_record(self) -> dict[str, object]:
        return asdict(self)


Runner = Callable[[Sequence[str], int], CommandResult]


def run_command(args: Sequence[str], timeout: int = 30) -> CommandResult:
    completed = subprocess.run(
        list(args),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        check=False,
    )
    return CommandResult(
        returncode=completed.returncode,
        stdout=(completed.stdout or "").strip(),
        stderr=(completed.stderr or "").strip(),
    )


def collect_environment(
    *,
    runner: Runner = run_command,
    project_root: Path,
    python_executable: str,
) -> dict[str, object]:
    failures: list[dict[str, object]] = []

    def powershell_json(name: str, script: str) -> list[dict[str, object]]:
        result = runner(
            [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-Command",
                "$OutputEncoding = [System.Text.UTF8Encoding]::new(); "
                "[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new(); "
                + script,
            ],
            30,
        )
        if result.returncode != 0:
            failures.append(
                {
                    "stage": f"inventory:{name}",
                    "returncode": result.returncode,
                    "stderr": result.stderr,
                }
            )
            return []
        try:
            return normalize_json_records(json.loads(result.stdout or "[]"))
        except json.JSONDecodeError as exc:
            failures.append(
                {
                    "stage": f"inventory:{name}",
                    "error": f"json decode failed: {exc}",
                    "stdout": result.stdout,
                }
            )
            return []

    def tool_result(name: str, args: Sequence[str], timeout: int = 30) -> dict[str, object]:
        result = runner(args, timeout)
        if result.returncode != 0:
            failures.append(
                {
                    "stage": f"tool:{name}",
                    "returncode": result.returncode,
                    "stderr": result.stderr,
                }
            )
        return result.to_record()

    git_commit_result = runner(["git", "rev-parse", "HEAD"], 30)
    if git_commit_result.returncode != 0:
        failures.append(
            {
                "stage": "git:commit",
                "returncode": git_commit_result.returncode,
                "stderr": git_commit_result.stderr,
            }
        )

    package_freeze = runner(["uv", "pip", "freeze"], 60)
    if package_freeze.returncode != 0:
        failures.append(
            {
                "stage": "python:uv-pip-freeze",
                "returncode": package_freeze.returncode,
                "stderr": package_freeze.stderr,
            }
        )

    return {
        "schema_version": 1,
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "project_root": str(project_root),
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        },
        "hardware": {
            "computer_system": powershell_json(
                "computer-system",
                "Get-CimInstance Win32_ComputerSystem | "
                "Select-Object Manufacturer,Model,TotalPhysicalMemory | "
                "ConvertTo-Json -Depth 4",
            ),
            "os": powershell_json(
                "operating-system",
                "Get-CimInstance Win32_OperatingSystem | "
                "Select-Object Caption,Version,BuildNumber,OSArchitecture | "
                "ConvertTo-Json -Depth 4",
            ),
            "cpu": powershell_json(
                "cpu",
                "Get-CimInstance Win32_Processor | "
                "Select-Object Name,Manufacturer,NumberOfCores,NumberOfLogicalProcessors,MaxClockSpeed | "
                "ConvertTo-Json -Depth 4",
            ),
            "gpu": powershell_json(
                "gpu",
                "Get-CimInstance Win32_VideoController | "
                "Select-Object Name,AdapterRAM,DriverVersion | "
                "ConvertTo-Json -Depth 4",
            ),
            "npu_candidates": powershell_json(
                "npu-candidates",
                "Get-CimInstance Win32_PnPEntity | "
                "Where-Object { $_.Name -match 'NPU|AI Boost|Neural|VPU|Movidius|OpenVINO' } | "
                "Select-Object Name,Status,PNPClass | "
                "ConvertTo-Json -Depth 4",
            ),
        },
        "tools": {
            "uv": tool_result("uv", ["uv", "--version"]),
            "git_status": tool_result("git-status", ["git", "status", "-sb"]),
        },
        "python": {
            "executable": python_executable,
            "version": tool_result("python-version", [python_executable, "--version"]),
        },
        "packages": package_lines(package_freeze.stdout)
        if package_freeze.returncode == 0
        else [],
        "git": {
            "commit": git_commit_result.stdout if git_commit_result.returncode == 0 else None,
        },
        "failures": failures,
    }


def normalize_json_records(value: object) -> list[dict[str, object]]:
    if value is None:
        return []
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        return [value]
    return [{"value": value}]


def package_lines(output: str) -> list[str]:
    return [line.strip() for line in output.splitlines() if line.strip()]


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def merge_failures(*collections: Iterable[dict[str, object]]) -> list[dict[str, object]]:
    merged: list[dict[str, object]] = []
    for collection in collections:
        merged.extend(collection)
    return merged
