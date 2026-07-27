---
name: writing-testlib-generators
description: Use when designing or implementing C++ testlib generators for competitive-programming test data, including parameterized generation strategies and adversarial test suites.
---

# Writing Testlib Generators

Treat a generator as a targeted test-design tool, not a source of arbitrary random input. Every generated case must be valid, reproducible, and chosen to distinguish incorrect or slow solutions.

## Design the test families

1. Extract the input invariants and the likely wrong algorithms from the problem.
2. Define named modes for meaningful structures: boundary sizes, all-equal values, monotone order, clustered values, sparse/dense graphs, pathological ties, or cases near the time limit.
3. Give each mode only the hyperparameters it needs (`n`, bounds, density, shape). Expose them with named `opt` calls and validate their combination.
4. Use testlib `rnd` exclusively after `registerGen`; never use `rand`, `<random>`, or clock-derived seeds. Preserve the invoking command and seed when a failure is found.
5. Generate data that satisfies invariants by construction. Combine modes in the package rather than relying on uniform randomness.

```cpp
#include "testlib.h"
#include <algorithm>
#include <iostream>
#include <vector>

int main(int argc, char* argv[]) {
    registerGen(argc, argv, 1);
    const int n = opt<int>("n");
    const int limit = opt<int>("limit");
    const std::string mode = opt<std::string>("mode");
    ensuref(n >= 1 && limit >= 1, "invalid bounds");

    std::vector<int> a(n);
    if (mode == "equal") std::fill(a.begin(), a.end(), rnd.next(1, limit));
    else for (int& x : a) x = rnd.next(1, limit);
    if (mode == "sorted") std::sort(a.begin(), a.end());
    else ensuref(mode == "random" || mode == "equal", "unknown mode: %s", mode.c_str());

    std::cout << n << '\n';
    for (int i = 0; i < n; ++i) std::cout << a[i] << " \n"[i + 1 == n];
}
```

## Quick reference

| Concern | Requirement |
| --- | --- |
| Reproduction | `registerGen`, testlib `rnd`, recorded command and seed |
| Configuration | Typed, named `opt` values and `ensuref` validation |
| Strength | Deliberate modes derived from constraints and failure hypotheses |
| Validity | Construct the object under its invariants; do not repair random garbage |

## Avoid

- Do not use one uniform distribution as the entire suite.
- Do not hide strategy selection in source edits or unlabelled positional arguments.
- Do not generate maximum-size data without considering both the intended and tempting incorrect complexities.
