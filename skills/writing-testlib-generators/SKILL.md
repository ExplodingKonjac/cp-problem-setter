---
name: writing-testlib-generators
description: Use when implementing C++ testlib generators from an existing competitive-programming test-data design, including parameterized modes, reproducible randomness, and valid structured output.
---

# Writing Testlib Generators

**REQUIRED UPSTREAM SKILL:** Use `designing-test-data` to define the stochastic model, parameter priors, semantic diagnostics, and generation schedule before implementing generator modes.

Treat a generator as a targeted implementation of that design, not a source of arbitrary random input. Every generated case must be valid, reproducible, and chosen to distinguish incorrect or slow solutions.

## Implement the planned families

1. Translate each stochastic climate and supplemental family in the settled design into an explicit generator mode. Preserve its latent-variable relationships and required invariants.
2. Map only the planned parameters (`n`, bounds, scale, density, persistence, shape) to that mode; do not invent a new testing strategy inside the generator.
3. Expose parameters with typed, named `opt` calls and reject absent or incompatible combinations with `ensuref`.
4. Use testlib `rnd` exclusively after `registerGen`; never use `rand`, `<random>`, or clock-derived seeds. Preserve the invoking command and seed when a failure is found.
5. Construct valid data directly and assert postconditions that protect the planted property after relabeling, shuffling, or jitter.
6. Keep serialization separate from construction when the design calls for randomized presentation.

The following example shows Testlib mechanics for a design whose latent process has geometric regime lengths and per-regime drift. Its parameters must come from the settled design.

```cpp
#include "testlib.h"
#include <iostream>
#include <vector>

int main(int argc, char* argv[]) {
    registerGen(argc, argv, 1);
    const int n = opt<int>("n");
    const int limit = opt<int>("limit");
    const int meanRun = opt<int>("mean-run");
    const int maxDrift = opt<int>("max-drift");
    const int noise = opt<int>("noise");
    ensuref(n >= 1 && meanRun >= 1, "invalid size or duration");
    ensuref(maxDrift >= 0 && noise >= 0 && maxDrift + noise <= limit,
            "latent value range exceeds output bounds");

    std::vector<int> a(n);
    int drift = 0;
    for (int i = 0; i < n; ++i) {
        if (i == 0 || rnd.next(meanRun) == 0)
            drift = rnd.next(-maxDrift, maxDrift);
        a[i] = drift + rnd.next(-noise, noise);
    }

    std::cout << n << '\n';
    for (int i = 0; i < n; ++i) std::cout << a[i] << " \n"[i + 1 == n];
}
```

## Quick reference

| Concern | Requirement |
| --- | --- |
| Reproduction | `registerGen`, testlib `rnd`, recorded command and seed |
| Configuration | Typed, named `opt` values and `ensuref` validation |
| Fidelity | Modes preserve the design's distributions, dependencies, and invariants |
| Validity | Construct the object under its invariants; do not repair random garbage |

## Avoid

- Do not use one uniform distribution as the entire suite.
- Do not hide strategy selection in source edits or unlabelled positional arguments.
- Do not invent or silently omit distributions when the settled design is incomplete; return to `designing-test-data`.
