"""Integration tests for the portable stress-testing runner."""

from __future__ import annotations

import json
import shlex
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("stress.py")


def python_command(code: str) -> str:
    return f"{shlex.quote(sys.executable)} -c {shlex.quote(code)}"


class StressRunnerTests(unittest.TestCase):
    def run_stress(self, *arguments: str, cwd: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_requires_seed_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_stress(
                "--generator-cmd",
                python_command("print('1')"),
                "--candidate-cmd",
                python_command("print('1')"),
                "--reference-cmd",
                python_command("print('1')"),
                "--iterations",
                "1",
                cwd=Path(directory),
            )

        self.assertEqual(result.returncode, 2)
        self.assertIn("{seed}", result.stderr)

    def test_rejects_nonpositive_iterations_and_timeout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            common = (
                "--generator-cmd",
                python_command("print('1')") + " {seed}",
                "--candidate-cmd",
                python_command("print('1')"),
                "--reference-cmd",
                python_command("print('1')"),
            )
            iterations = self.run_stress(
                *common, "--iterations", "0", cwd=Path(directory)
            )
            timeout = self.run_stress(
                *common,
                "--iterations",
                "1",
                "--timeout-seconds",
                "0",
                cwd=Path(directory),
            )

        self.assertEqual(iterations.returncode, 2)
        self.assertIn("--iterations must be positive", iterations.stderr)
        self.assertEqual(timeout.returncode, 2)
        self.assertIn("--timeout-seconds must be positive", timeout.stderr)

    def test_successfully_compares_identical_program_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_stress(
                "--generator-cmd",
                python_command("import sys; print(sys.argv[1])") + " {seed}",
                "--candidate-cmd",
                python_command("import sys; print(int(sys.stdin.read()) * 2)"),
                "--reference-cmd",
                python_command("import sys; print(int(sys.stdin.read()) * 2)"),
                "--iterations",
                "2",
                "--seed-start",
                "7",
                cwd=Path(directory),
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("OK 2/2 (seed=8)", result.stdout)

    def test_output_mismatch_saves_reproducible_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            failure_dir = Path(directory) / "failures"
            result = self.run_stress(
                "--generator-cmd",
                python_command("print('3')") + " {seed}",
                "--candidate-cmd",
                python_command("print('candidate')"),
                "--reference-cmd",
                python_command("print('reference')"),
                "--iterations",
                "1",
                "--failure-dir",
                str(failure_dir),
                cwd=Path(directory),
            )

            artifact = failure_dir / "failure-1"
            metadata = json.loads((artifact / "metadata.json").read_text())
            input_data = (artifact / "input.txt").read_text()
            candidate_output = (artifact / "candidate.out").read_text()
            reference_output = (artifact / "reference.out").read_text()

            self.assertEqual(result.returncode, 1)
            self.assertIn("candidate output differs", result.stderr)
            self.assertEqual(input_data, "3\n")
            self.assertEqual(candidate_output, "candidate\n")
            self.assertEqual(reference_output, "reference\n")
            self.assertEqual(metadata["seed"], 1)

    def test_validator_failure_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            failure_dir = Path(directory) / "failures"
            result = self.run_stress(
                "--generator-cmd",
                python_command("print('invalid')") + " {seed}",
                "--candidate-cmd",
                python_command("print('unused')"),
                "--reference-cmd",
                python_command("print('unused')"),
                "--validator-cmd",
                python_command("import sys; sys.exit(1)"),
                "--iterations",
                "1",
                "--failure-dir",
                str(failure_dir),
                cwd=Path(directory),
            )

            metadata = json.loads(
                (failure_dir / "failure-1" / "metadata.json").read_text()
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("validator exited with status 1", result.stderr)
        self.assertIn("validator", metadata["results"])
        self.assertNotIn("candidate", metadata["results"])

    def test_candidate_timeout_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            failure_dir = Path(directory) / "failures"
            result = self.run_stress(
                "--generator-cmd",
                python_command("print('1')") + " {seed}",
                "--candidate-cmd",
                python_command("import time; time.sleep(1)"),
                "--reference-cmd",
                python_command("print('1')"),
                "--iterations",
                "1",
                "--timeout-seconds",
                "0.05",
                "--failure-dir",
                str(failure_dir),
                cwd=Path(directory),
            )

            metadata = json.loads(
                (failure_dir / "failure-1" / "metadata.json").read_text()
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("candidate timed out", result.stderr)
        self.assertTrue(metadata["results"]["candidate"]["timed_out"])

    def test_checker_acceptance_and_rejection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            common = (
                "--generator-cmd",
                python_command("print('input')") + " {seed}",
                "--candidate-cmd",
                python_command("print('candidate')"),
                "--reference-cmd",
                python_command("print('reference')"),
                "--iterations",
                "1",
            )
            accepted = self.run_stress(
                *common,
                "--checker-cmd",
                python_command("import sys; sys.exit(0)"),
                cwd=root,
            )
            failure_dir = root / "rejected"
            rejected = self.run_stress(
                *common,
                "--checker-cmd",
                python_command("import sys; sys.exit(1)"),
                "--failure-dir",
                str(failure_dir),
                cwd=root,
            )
            metadata = json.loads(
                (failure_dir / "failure-1" / "metadata.json").read_text()
            )

        self.assertEqual(accepted.returncode, 0, accepted.stderr)
        self.assertEqual(rejected.returncode, 1)
        self.assertIn("checker exited with status 1", rejected.stderr)
        self.assertEqual(metadata["results"]["checker"]["returncode"], 1)


if __name__ == "__main__":
    unittest.main()
