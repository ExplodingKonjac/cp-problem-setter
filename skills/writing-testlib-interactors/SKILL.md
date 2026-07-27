---
name: writing-testlib-interactors
description: Use when designing or implementing C++ testlib interactors for interactive competitive-programming problems, especially where protocol latency, pipe buffering, or query limits matter.
---

# Writing Testlib Interactors

An interactor is a protocol endpoint under a time limit. Make each exchange deterministic, cheap, and immediately visible to the contestant process.

## Build the protocol before the loop

1. Specify the first speaker, exact command grammar, response grammar, ranges, query budget, and final-answer command in the statement and implementation.
2. Call `registerInteraction(argc, argv)`. Read hidden testcase data from `inf`; read contestant messages from `ouf` with bounded testlib readers.
3. Precompute information that would otherwise be expensive per query. Enforce the query count before replying.
4. After every protocol response, write through `std::cout` and flush immediately. A newline alone can remain buffered in a pipe; use `std::endl` or `std::cout.flush()`.
5. Reject malformed commands and out-of-range values promptly. Return `_wa` for an invalid query or answer and `_fail` only for broken judge data or an interactor invariant.

```cpp
#include "testlib.h"
#include <iostream>

int main(int argc, char* argv[]) {
    registerInteraction(argc, argv);
    const int n = inf.readInt(1, 1'000'000, "n");
    const int secret = inf.readInt(1, n, "secret");
    constexpr int limit = 20;

    for (int used = 0;;) {
        const std::string command = ouf.readToken("command");
        if (command == "?") {
            if (++used > limit) quitf(_wa, "query limit exceeded");
            const int x = ouf.readInt(1, n, "query value");
            std::cout << (x <= secret ? "YES" : "NO") << std::endl;
        } else if (command == "!") {
            const int x = ouf.readInt(1, n, "answer");
            if (x != secret) quitf(_wa, "incorrect final answer");
            quitf(_ok, "answered in %d queries", used);
        } else {
            quitf(_wa, "expected '?' or '!', found '%s'", command.c_str());
        }
    }
}
```

## Pipe-safety checklist

| Risk | Required handling |
| --- | --- |
| Buffered reply | Flush after every reply |
| Slow interaction | Keep per-query work bounded; precompute judge state |
| Excess queries | Count and reject before responding |
| EOF or malformed command | Let testlib diagnose it or issue a prompt `_wa` |
| Diagnostic pollution | Never write prompts or debug output to protocol stdout |

## Avoid

- Do not mix unflushed `std::cout` output with reads from `ouf`.
- Do not leave protocol states implicit or wait for input after a final verdict.
- Do not depend on a contestant's output buffering “probably” flushing; test conversations through pipes.
