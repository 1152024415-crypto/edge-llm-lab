from pathlib import Path
import sys

from edge_llm_lab.phase0.inventory import CommandResult, collect_environment, run_command


def test_collect_environment_records_hardware_tools_and_failures():
    def fake_runner(args, timeout=30):
        command = " ".join(args)
        if "Win32_Processor" in command:
            return CommandResult(0, '{"Name":"Intel Core Ultra","NumberOfCores":14}', "")
        if "Win32_VideoController" in command:
            return CommandResult(0, '[{"Name":"Intel Arc","DriverVersion":"31.0"}]', "")
        if "Win32_ComputerSystem" in command:
            return CommandResult(0, '{"TotalPhysicalMemory":33779150848}', "")
        if "Win32_OperatingSystem" in command:
            return CommandResult(0, '{"Caption":"Windows","BuildNumber":"26000"}', "")
        if "Win32_PnPEntity" in command:
            return CommandResult(0, '[{"Name":"Intel AI Boost","Status":"OK"}]', "")
        if args[:2] == ["uv", "--version"]:
            return CommandResult(0, "uv 0.11.0", "")
        if args[:2] == ["git", "rev-parse"]:
            return CommandResult(0, "abc123", "")
        if args[:2] == ["git", "status"]:
            return CommandResult(0, "## main", "")
        if args[:3] == ["uv", "pip", "freeze"]:
            return CommandResult(0, "openvino==2026.1.0\npytest==8.4.0", "")
        if args == ["python", "--version"]:
            return CommandResult(0, "Python 3.12.13", "")
        return CommandResult(1, "", f"unexpected command: {command}")

    snapshot = collect_environment(
        runner=fake_runner,
        project_root=Path("D:/proj/edge-llm-lab"),
        python_executable="python",
    )

    assert snapshot["hardware"]["cpu"][0]["Name"] == "Intel Core Ultra"
    assert snapshot["hardware"]["gpu"][0]["Name"] == "Intel Arc"
    assert snapshot["hardware"]["npu_candidates"][0]["Name"] == "Intel AI Boost"
    assert snapshot["tools"]["uv"]["stdout"] == "uv 0.11.0"
    assert snapshot["python"]["version"]["stdout"] == "Python 3.12.13"
    assert snapshot["git"]["commit"] == "abc123"
    assert snapshot["packages"] == ["openvino==2026.1.0", "pytest==8.4.0"]
    assert snapshot["failures"] == []


def test_run_command_replaces_undecodable_output():
    result = run_command(
        [
            sys.executable,
            "-c",
            "import sys; sys.stdout.buffer.write(bytes([0x88]))",
        ]
    )

    assert result.returncode == 0
    assert result.stdout
