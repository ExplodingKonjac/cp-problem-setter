---
name: writing-testlib-checkers
description: Use when a competitive-programming problem needs a custom C++ testlib checker because standard preset checkers cannot validate its non-unique, semantic, scored, or certificate-style output.
---

# Writing Testlib Checkers

Write a custom checker only when a preset checker cannot express the acceptance rule. A checker is part of the judging contract: it must accept every valid output, reject every invalid one, and never confuse a contestant error with a broken package.

## Define the verdict contract first

1. State the semantic property to verify and whether the jury answer is needed for feasibility, optimality, or scoring.
2. Start with `registerTestlibCmd(argc, argv)`. Read the testcase from `inf`, contestant output from `ouf`, and jury output from `ans` only when that reference is genuinely required.
3. Parse contestant output completely with typed testlib readers, check all bounds and relationships, then call `ouf.readEof()`.
4. Return `_wa` for invalid contestant output; reserve `_fail` for an invalid jury answer, checker invariant, or other package defect. Return `_ok` only after all conditions pass.
5. Make messages precise without revealing hidden answer data.

```cpp
#include "testlib.h"

int main(int argc, char* argv[]) {
    registerTestlibCmd(argc, argv);
    const long long target = inf.readLong(0, 1'000'000'000'000LL, "target");

    const long long x = ouf.readLong(0, target, "x");
    const long long y = ouf.readLong(0, target, "y");
    ouf.readEof();
    if ((__int128)x + y != target)
        quitf(_wa, "x + y = %lld, expected %lld", x + y, target);
    quitf(_ok, "valid decomposition");
}
```

## Quick reference

| Situation | Action |
| --- | --- |
| Exact unique output | Use a preset token/line checker instead |
| Construction or certificate | Validate the full witness semantically |
| Optimization | Validate feasibility before comparing objectives or applying the platform score contract |
| Malformed or invalid contestant output | `_wa` with a safe diagnostic |
| Invalid test, answer, or checker assumption | `_fail`; investigate the package |

## Avoid

- Do not compare a contestant witness to one jury witness when multiple valid witnesses exist.
- Do not trust a reported objective: recompute it from the contestant output.
- Do not accept extra output, use ambiguous parsing, or leak the jury's hidden values in a rejection message.
