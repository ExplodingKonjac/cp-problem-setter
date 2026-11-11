# Changelog

## 1.2.1 — 2026-11-11

- Adds coding-style requirements to `writing-solution`: reference code must not
  validate input, should follow competitive-programming idioms, use the
  simplest correct implementation, and stay formatter-clean and concise.
- Adds writing-style requirements to `writing-statement`: clean, natural prose;
  affirmative rules instead of negative patches; and notation for complex
  definitions and procedures.
- Consolidates `writing-statement` into four sections.

## 1.2.0 — 2026-11-11

- Reworks `writing-statement` and `writing-solution` to specify required
  content instead of fixed section layouts, leaving organization to the
  author.
- Replaces the fixed audit report skeleton with the content a release
  report must carry.
- Updates the example package templates and `building-problem-packages`
  guidance so the file layout stays canonical while statements and
  editorials are organized freely.
- Removes the required design brief from `designing-test-data`; the design
  is settled directly before generator implementation.

## 1.1.0 — 2026-07-28

- Adds the `designing-test-data` skill for creating strong, natural stochastic
  generators and diagnosing their induced input and output distributions.
- Separates test-data strategy from C++ testlib generator implementation.

## 1.0.0 — 2026-07-28

Initial public release of CP Problem Setter.

- Provides workflows for writing statements and solutions, developing testlib
  tools, building packages, stress testing, and release auditing.
- Includes plugin metadata for Codex, Claude-compatible clients, and agent
  marketplaces.
