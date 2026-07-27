---
name: stress-testing
description: Use when comparing a candidate competitive-programming solution against a reference solution on generated tests to find reproducible counterexamples or runtime failures.
---

# Stress Testing

Stress testing turns a suspected difference into a reproducible input. Use strong generator modes from `writing-testlib-generators`; random uniform data alone rarely finds the important failures.

## Run the universal runner

```bash
python3 skills/stress-testing/scripts/stress.py \
  --generator-cmd './build/gen {seed} --mode random' \
  --candidate-cmd './build/candidate' \
  --reference-cmd './build/std' \
  --iterations 1000
```

`{seed}` is required in `--generator-cmd` and is replaced by sequential values beginning at `--seed-start` (default `1`). Use the saved seed and command to reproduce a failure exactly.

Add `--validator-cmd './build/val'` to reject invalid generated input before running solutions. For a special judge, add `--checker-cmd './build/checker'`; the runner appends the input, candidate-output, and reference-output paths to that command. Without a checker, it compares output bytes exactly.

Set `--timeout-seconds` (default `5`) for each process and `--failure-dir` (default `stress-failures`) for preserved counterexamples. A failure is stored in `failure-<seed>` beneath that directory. The run ends after the required positive `--iterations` count, or immediately on the first failure.

## Investigate a failure

- Read `metadata.json` and reproduce the recorded generator command and seed.
- Inspect `input.txt`, outputs, and stderr logs before changing either solution.
- Minimize the input manually while preserving the failure, then add the minimized case to the permanent suite.
- Distinguish a generator or validator failure from a candidate mismatch; fix the component that violated its contract.

## Avoid

- Do not compare ordinary outputs with a byte comparison when a custom checker defines correctness.
- Do not discard a failure directory before making its input reproducible.
- Do not run an unbounded stress loop; choose an iteration count appropriate to the generator and timeout.
