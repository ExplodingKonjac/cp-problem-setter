#!/usr/bin/env python3
"""Run deterministic competitive-programming stress tests."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


@dataclass
class RunResult:
    command: list[str]
    stdout: bytes = b""
    stderr: bytes = b""
    returncode: int | None = None
    timed_out: bool = False
    error: str | None = None


def parse_command(value: str, option: str) -> list[str]:
    try:
        command = shlex.split(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid {option}: {exc}") from exc
    if not command:
        raise argparse.ArgumentTypeError(f"{option} must not be empty")
    return command


def run_command(
    command: Sequence[str], input_data: bytes | None, timeout: float
) -> RunResult:
    result = RunResult(command=list(command))
    try:
        completed = subprocess.run(
            command,
            input=input_data,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        result.stdout = completed.stdout
        result.stderr = completed.stderr
        result.returncode = completed.returncode
    except subprocess.TimeoutExpired as exc:
        result.stdout = exc.stdout or b""
        result.stderr = exc.stderr or b""
        result.timed_out = True
    except OSError as exc:
        result.error = str(exc)
    return result


def failure_reason(label: str, result: RunResult) -> str | None:
    if result.timed_out:
        return f"{label} timed out"
    if result.error:
        return f"{label} could not start: {result.error}"
    if result.returncode != 0:
        return f"{label} exited with status {result.returncode}"
    return None


def failure_path(root: Path, seed: int) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    base = root / f"failure-{seed}"
    path = base
    suffix = 2
    while path.exists():
        path = root / f"{base.name}-{suffix}"
        suffix += 1
    path.mkdir()
    return path


def result_metadata(result: RunResult) -> dict[str, object]:
    return {
        "command": result.command,
        "returncode": result.returncode,
        "timed_out": result.timed_out,
        "error": result.error,
        "stdout_bytes": len(result.stdout),
        "stderr_bytes": len(result.stderr),
    }


def save_failure(
    root: Path,
    seed: int,
    reason: str,
    input_data: bytes,
    results: dict[str, RunResult],
    arguments: argparse.Namespace,
) -> Path:
    path = failure_path(root, seed)
    input_path = path / "input.txt"
    candidate_path = path / "candidate.out"
    reference_path = path / "reference.out"
    input_path.write_bytes(input_data)
    if "candidate" in results:
        candidate_path.write_bytes(results["candidate"].stdout)
    if "reference" in results:
        reference_path.write_bytes(results["reference"].stdout)
    if "checker" in results:
        results["checker"].command = results["checker"].command[:-3] + [
            str(input_path),
            str(candidate_path),
            str(reference_path),
        ]
    for label, result in results.items():
        (path / f"{label}.stdout").write_bytes(result.stdout)
        (path / f"{label}.stderr").write_bytes(result.stderr)
    metadata = {
        "seed": seed,
        "reason": reason,
        "arguments": vars(arguments),
        "results": {
            label: result_metadata(result) for label, result in results.items()
        },
    }
    (path / "metadata.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generator-cmd", required=True)
    parser.add_argument("--candidate-cmd", required=True)
    parser.add_argument("--reference-cmd", required=True)
    parser.add_argument("--iterations", required=True, type=int)
    parser.add_argument("--validator-cmd")
    parser.add_argument("--checker-cmd")
    parser.add_argument("--seed-start", type=int, default=1)
    parser.add_argument("--timeout-seconds", type=float, default=5.0)
    parser.add_argument("--failure-dir", default="stress-failures")
    return parser


def validate_arguments(
    parser: argparse.ArgumentParser, args: argparse.Namespace
) -> None:
    if "{seed}" not in args.generator_cmd:
        parser.error("--generator-cmd must contain the {seed} placeholder")
    if args.iterations <= 0:
        parser.error("--iterations must be positive")
    if args.timeout_seconds <= 0:
        parser.error("--timeout-seconds must be positive")
    for option in (
        "generator_cmd",
        "candidate_cmd",
        "reference_cmd",
        "validator_cmd",
        "checker_cmd",
    ):
        value = getattr(args, option)
        if value is not None:
            try:
                parse_command(value, f"--{option.replace('_', '-')}")
            except argparse.ArgumentTypeError as exc:
                parser.error(str(exc))


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    validate_arguments(parser, args)

    failure_root = Path(args.failure_dir)
    for index in range(args.iterations):
        seed = args.seed_start + index
        generator_cmd = parse_command(
            args.generator_cmd.replace("{seed}", str(seed)), "--generator-cmd"
        )
        results: dict[str, RunResult] = {}
        results["generator"] = run_command(generator_cmd, None, args.timeout_seconds)
        input_data = results["generator"].stdout
        reason = failure_reason("generator", results["generator"])

        if reason is None and args.validator_cmd:
            validator_cmd = parse_command(args.validator_cmd, "--validator-cmd")
            results["validator"] = run_command(
                validator_cmd, input_data, args.timeout_seconds
            )
            reason = failure_reason("validator", results["validator"])

        if reason is None:
            candidate_cmd = parse_command(args.candidate_cmd, "--candidate-cmd")
            reference_cmd = parse_command(args.reference_cmd, "--reference-cmd")
            results["candidate"] = run_command(
                candidate_cmd, input_data, args.timeout_seconds
            )
            reason = failure_reason("candidate", results["candidate"])
            results["reference"] = run_command(
                reference_cmd, input_data, args.timeout_seconds
            )
            reason = reason or failure_reason("reference", results["reference"])

        if reason is None and args.checker_cmd:
            with tempfile.TemporaryDirectory(prefix="stress-checker-") as temp_dir:
                temp_path = Path(temp_dir)
                input_path = temp_path / "input.txt"
                candidate_path = temp_path / "candidate.out"
                reference_path = temp_path / "reference.out"
                input_path.write_bytes(input_data)
                candidate_path.write_bytes(results["candidate"].stdout)
                reference_path.write_bytes(results["reference"].stdout)
                checker_cmd = parse_command(args.checker_cmd, "--checker-cmd")
                checker_cmd.extend(
                    [str(input_path), str(candidate_path), str(reference_path)]
                )
                results["checker"] = run_command(
                    checker_cmd, None, args.timeout_seconds
                )
                reason = failure_reason("checker", results["checker"])
        elif (
            reason is None
            and results["candidate"].stdout != results["reference"].stdout
        ):
            reason = "candidate output differs from reference output"

        if reason is not None:
            path = save_failure(failure_root, seed, reason, input_data, results, args)
            print(f"FAIL seed={seed}: {reason}\nartifacts: {path}", file=sys.stderr)
            return 1

        completed = index + 1
        if completed == 1 or completed == args.iterations or completed % 100 == 0:
            print(f"OK {completed}/{args.iterations} (seed={seed})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
