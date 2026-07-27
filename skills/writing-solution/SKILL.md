---
name: writing-solution
description: Use when turning a competitive-programming problem statement and a proposed solution idea into an editorial-style explanation or a reference implementation, particularly when the idea may be incomplete, ambiguous, or incorrect.
---

# Writing Problem Solutions

Treat the problem statement and constraints as the source of truth. A user’s idea is evidence to assess, not an algorithm to endorse automatically.

## Establish the direction

1. Extract the input/output contract, constraints, required property, and target complexity from the statement.
2. If an idea is supplied, test its invariant, completeness, edge cases, and worst-case complexity against that contract.
3. If the idea is absent, derive a solution independently.
4. If a material ambiguity prevents a correct choice—an undefined operation, missing constraint, unclear intended interpretation, or incompatible requested artifact—ask one focused question using the available user-input mechanism. Do not produce a speculative final solution or code while awaiting that answer.
5. If the idea is plainly incorrect but the statement is unambiguous, say why concisely and replace it with a justified approach; do not preserve a known-bad method.

## Produce the requested artifact

Honor the requested form exactly.

| Request | Deliverable |
| --- | --- |
| Solution text / editorial / explanation | Algorithm, correctness argument, complexity, and decisive edge cases |
| Reference solution / standard solution code | Complete compilable code in the requested language, with only the explanation needed to establish the approach |
| Neither form specified | Ask whether the user wants solution text or reference code |

For a solution explanation, present the idea before its proof and make every claim traceable to the statement. For reference code, implement the validated algorithm, use types safe for constraints, and keep I/O and indexing consistent with the stated format.

Use C++23 for reference solutions unless the user, problem statement, or target judge specifies a different language or language standard.

## Validation gate

Before delivering, confirm:

- Every case in the statement is handled, including minima, maxima, duplicates, and degenerate structures.
- The proof covers both feasibility and optimality/counting requirements.
- The complexity fits the largest input, not only samples.
- The code matches the described algorithm and output contract.

## Avoid

- Do not infer unstated constraints or silently choose between incompatible interpretations.
- Do not turn a vague intuition into a proof by assertion.
- Do not provide both an editorial and code when the user requested only one, unless they ask for both.
