# CP Problem Setter

CP Problem Setter is a cross-platform agent plugin for creating and reviewing
competitive-programming problems. It provides testlib conventions, problem
package organization, and solution-authoring workflows.

## Included skills

| Skill | Use it for |
| --- | --- |
| `developing-testlib` | Shared C++ testlib conventions, including options and streams |
| `writing-testlib-generators` | Reproducible, adversarial test-data generators |
| `writing-testlib-validators` | Strict input-format and constraint validation |
| `writing-testlib-checkers` | Custom checkers for semantic or non-unique output |
| `writing-testlib-interactors` | Interactive judge protocols and pipe-safe I/O |
| `writing-solution` | Editorials or C++23 reference solutions from a problem statement and idea |
| `problem-directories` | Initializing or safely reorganizing a problem package |

Invoke a skill explicitly when needed, for example:

```text
Use $writing-testlib-validators to write a strict validator for this input format.
```

## Problem package layout

`problem-directories` bundles the canonical template at
`skills/problem-directories/assets/example-problem`. It keeps authored files in
`src/` and treats `build/` as generated output:

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
problem needs a custom checker or interactive judge.

## Plugin layout

The repository is both a plugin and a single-plugin marketplace. Its manifests
are provided for Codex, Claude-compatible clients, and agent marketplaces:

```text
.
├── .agents/plugins/marketplace.json
├── .claude-plugin/
├── .codex-plugin/plugin.json
├── skills/
└── opencode.json
```
