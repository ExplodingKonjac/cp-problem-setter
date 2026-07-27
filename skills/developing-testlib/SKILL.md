---
name: developing-testlib
description: Use when creating or reviewing C++ testlib generators, validators, checkers, or interactors, especially when choosing command-line parsing and input/output streams.
---

# Developing with Testlib

Use testlib for role registration, reproducible random generation, assertions, and special file streams. Keep ordinary program I/O idiomatic C++: read stdin with `std::cin` and write stdout with `std::cout`.

## Establish the executable role

- Include `testlib.h` and register the correct role before reading arguments or data.
- Parse named arguments with the typed `opt` family, such as `opt<int>("n")`; do not hand-roll `argv` parsing.
- Name options by their domain meaning and reject invalid combinations with testlib assertions.
- Use `std::cin` and `std::cout` for the process's standard input and output. Reserve `inf`, `ouf`, and `ans` for the input, contestant-output, and jury-answer files that testlib supplies to validators, checkers, and interactors.

```cpp
#include "testlib.h"
#include <iostream>

int main(int argc, char* argv[]) {
    registerGen(argc, argv, 1);
    const int n = opt<int>("n");
    const int limit = opt<int>("limit");
    ensuref(n > 0 && limit >= 0, "invalid n=%d limit=%d", n, limit);

    std::cout << n << '\n';
    for (int i = 0; i < n; ++i)
        std::cout << rnd.next(0, limit) << " \n"[i + 1 == n];
}
```

## Quick reference

| Need | Use |
| --- | --- |
| Generator arguments | `registerGen(...)`, then `opt<T>("name")` |
| Reproducible randomness | testlib `rnd` after `registerGen` |
| Normal stdin/stdout | `std::cin`, `std::cout` |
| Problem input / contestant output / answer files | `inf`, `ouf`, `ans` after the relevant testlib registration |

## Avoid

- Do not mix standard streams with `inf`/`ouf`/`ans` merely for convenience; choose by file role.
- Do not parse flags manually or seed a separate random engine.
- Do not silently accept absent, malformed, or incompatible options.
