---
name: building-problem-packages
description: Use when initializing a competitive-programming problem package or reorganizing an existing package into the repository's standard source, build, generator, validator, and documentation layout.
---

# Building Problem Packages

Use the bundled [`assets/example-problem`](assets/example-problem) as the canonical layout. Keep authored material in `src/`; make `build/` disposable output produced by the Makefile.

## Initialize a package

Copy `assets/example-problem` to the requested package location, then replace its visible placeholders. Keep this required layout:

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

The file layout is required; the Markdown inside `statement.md` and `solution.md` is not. Their placeholder text lists the content a statement or editorial must carry, not a section structure to preserve—keep that content and organize the result however the problem reads best.

- Write the statement and editorial in the Markdown files.
- Write the C++23 reference solution in `std.cpp`.
- Write the testlib generator in `gen.cpp` and strict validator in `val.cpp`.
- Add test-point definitions to the Makefile only after generator options and coverage strategy are known.
- Keep `.in`, `.ans`, binaries, copied sources, and all `build/` output out of version control.

## Reorganize an existing package

1. Inventory files before moving anything. Map only clear equivalents into `src/`: statement/problem → `statement.md`, editorial/solution text → `solution.md`, reference solution → `std.cpp`, generator → `gen.cpp`, validator → `val.cpp`.
2. Retain the root `Makefile` and `.gitignore`, updating their paths to use `src/` and `build/` when necessary.
3. Preserve every unmatched file in its current location and report it; do not rename, archive, or delete it merely to make the tree look clean.
4. Treat an existing `build/` directory as generated output. Before clearing it, obtain explicit approval. Without approval, leave it intact and report that it is stale output.
5. Verify that all recognized authored files have one authoritative source location and that the Makefile regenerates outputs from it.

## Optional judging roles

Create `src/checker.cpp` only for a custom checker, or `src/interactor.cpp` only for an interactive problem. When adding either file, extend the Makefile with its build target and add it to the required outputs; do not scaffold either role for ordinary problems.

## Avoid

- Do not put statements, sources, or test data directly in `build/`.
- Do not replace a problem's custom checker with an ordinary answer generator.
- Do not delete unknown files, generated output, or test data without explicit approval.
