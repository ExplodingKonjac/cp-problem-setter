# CP Problem Setter

CP Problem Setter is a cross-platform skill plugin for authoring, testing, and
auditing competitive-programming problems. It supports the full problem-setting
workflow, from a raw idea to a release-ready package.

## Install

Clone or download this repository first. The plugin includes manifests for
Codex and Claude Code; configure OpenCode with the repository's skills path.

### Codex

In an eligible Codex workspace, open **Workspace settings → Plugins**, import
this repository as a plugin or marketplace source, then enable **CP Problem
Setter**. Plugin availability is controlled by workspace policy and may require
an administrator to perform the import.

### Claude Code

Add the repository as a local marketplace, then install the plugin:

```bash
claude plugin marketplace add /absolute/path/to/cp-problem-setter
claude plugin install cp-problem-setter@cp-problem-setter
```

Restart Claude Code after installation if it does not immediately discover the
new skills.

### OpenCode

Add the repository's `skills` directory to the `skills` array in your OpenCode
configuration, using an absolute path:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": ["/absolute/path/to/cp-problem-setter/skills"]
}
```

Alternatively, copy or symlink individual skill directories into a project
skill location that OpenCode discovers, such as `.agents/skills/`.

## Requirements

The skills themselves need no package installation. Problem packages produced
with the bundled layout use:

- a C++23 compiler and GNU Make;
- [testlib](https://github.com/MikeMirzayanov/testlib) for generators,
  validators, checkers, and interactors;
- Python 3 for the portable stress-testing runner.

## Included skills

| Skill | Use it for |
| --- | --- |
| `developing-testlib` | Shared C++ testlib conventions, options, and streams |
| `writing-testlib-generators` | Reproducible, adversarial test-data generators |
| `writing-testlib-validators` | Strict input-format and constraint validation |
| `writing-testlib-checkers` | Custom checkers for semantic or non-unique output |
| `writing-testlib-interactors` | Interactive judge protocols and pipe-safe I/O |
| `writing-statement` | Drafting, reviewing, or rewriting problem statements |
| `writing-solution` | Editorials or C++23 reference solutions from a statement and idea |
| `building-problem-packages` | Initializing or safely reorganizing a problem package |
| `stress-testing` | Reproducible candidate-versus-reference stress testing |
| `auditing-problem-packages` | Read-only pre-release package verification |

Invoke a skill explicitly when needed, for example:

```text
Use $writing-testlib-validators to write a strict validator for this input format.
```

## Typical workflow

1. Use `writing-statement` to turn an idea into a judgeable statement.
2. Use `writing-solution` to validate the intended approach and write an
   editorial or C++23 reference solution.
3. Use `building-problem-packages` to initialize or reorganize the package.
4. Use the testlib skills to implement the generator, validator, and any
   required checker or interactor.
5. Use `stress-testing` to compare candidate and reference programs.
6. Use `auditing-problem-packages` for the final read-only release audit.

## Problem package layout

`building-problem-packages` bundles the canonical layout at
[`skills/building-problem-packages/assets/example-problem`](skills/building-problem-packages/assets/example-problem).
Authored files live in `src/`; `build/` is generated output:

```text
problem/
├── .gitignore
├── Makefile
└── src/
    ├── statement.md
    ├── solution.md
    ├── std.cpp
    ├── gen.cpp
    └── val.cpp
```

The template uses C++23. Add `checker.cpp` or `interactor.cpp` only when the
problem requires a custom checker or interactive judge.

## Repository layout

This repository is both a plugin and a single-plugin marketplace:

```text
.
├── .agents/plugins/marketplace.json
├── .claude-plugin/
├── .codex-plugin/plugin.json
├── skills/
└── opencode.json
```

See [CHANGELOG.md](CHANGELOG.md) for release notes.

## License

CP Problem Setter is licensed under the [GNU General Public License v3.0](LICENSE).
