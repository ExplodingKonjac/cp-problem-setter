---
name: writing-testlib-validators
description: Use when implementing or reviewing C++ testlib input validators that must enforce problem constraints and an exact competitive-programming input format.
---

# Writing Testlib Validators

A validator is the authoritative definition of legal input. Parse the specified grammar exactly, then check every semantic constraint; accepting an unintended format is a package bug.

## Validate in format order

1. Call `registerValidation(argc, argv)` and read the test input from `inf`.
2. Read each token with a bounded testlib reader (`readInt`, `readLong`, `readToken`, and similar) and give it a diagnostic name.
3. Require every separator explicitly: use `readSpace()` between same-line fields and `readEoln()` at every prescribed line boundary.
4. Check cross-field constraints immediately after all data they depend on is known: sizes, uniqueness, graph connectivity conventions, sums, ordering, and relationships.
5. End with `inf.readEof()`. This requires the final newline and rejects trailing whitespace or extra tokens.

```cpp
#include "testlib.h"

int main(int argc, char* argv[]) {
    registerValidation(argc, argv);
    const int n = inf.readInt(1, 200000, "n");
    inf.readEoln();

    for (int i = 0; i < n; ++i) {
        inf.readInt(-1'000'000'000, 1'000'000'000, format("a[%d]", i + 1));
        if (i + 1 == n) inf.readEoln();
        else inf.readSpace();
    }
    inf.readEof();
}
```

## Strict-format checklist

| Requirement | Testlib mechanism |
| --- | --- |
| Bound a value | `inf.readInt(lo, hi, name)` or the matching typed reader |
| Require one separator | `inf.readSpace()` |
| Require a line ending | `inf.readEoln()` |
| Reject trailing spaces and data; require final newline | `inf.readEof()` after the final `readEoln()` |
| Reject invalid relationships | `ensuref(...)` or `quitf(_fail, ...)` with a precise message |

## Avoid

- Do not tokenize with `std::cin`, `readInts`, or permissive whitespace readers when the statement specifies line layout.
- Do not check only numeric ranges; validate all structural and semantic invariants.
- Do not omit `readEof()` or treat trailing spaces as harmless.
