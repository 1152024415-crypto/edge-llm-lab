import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_phase1_scripts_show_help_when_run_directly():
    scripts = [
        PROJECT_ROOT / "experiments/intel-openvino-1b/scripts/export-openvino-model.py",
        PROJECT_ROOT / "experiments/intel-openvino-1b/scripts/run-cpu-baseline.py",
    ]

    for script in scripts:
        completed = subprocess.run(
            [sys.executable, str(script), "--help"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stderr
        assert "usage:" in completed.stdout
