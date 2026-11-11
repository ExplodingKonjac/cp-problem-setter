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
4. If a material ambiguity blocks a correct choice—an undefined operation, missing constraint, unclear intended interpretation, or incompatible requested artifact—ask one focused question using the available user-input mechanism. Do not produce a speculative final solution or code while awaiting that answer.
5. If the idea is plainly incorrect but the statement is unambiguous, say why concisely and replace it with a justified approach; do not preserve a known-bad method.

## What the deliverable must contain

Honor the requested form exactly. If neither solution text nor reference code is specified, ask which one is wanted.

A solution text, editorial, or explanation must include:

- the algorithm or construction, together with the insight that makes it work;
- why it satisfies the stated requirement—feasibility and optimality, correctness of a count, or validity of a certificate, as applicable;
- the worst-case time and memory complexity, and why it fits the largest allowed input;
- the boundary and degenerate cases that could break the reasoning, and why they do not.

A reference solution must include:

- a complete, compilable implementation of the validated algorithm in the requested language;
- types and complexity safe for the stated bounds, with I/O and indexing consistent with the input format and output contract;
- only the explanation needed to establish what the code does.

Use C++23 for reference solutions unless the user, problem statement, or target judge specifies a different language or language standard.

This list is a content checklist, not an outline. Present the argument in whatever order makes it easiest to follow; proof may be interleaved with the algorithm description, and headings are optional.

## Validation gate

Before delivering, confirm:

- Every case in the statement is handled, including minima, maxima, duplicates, and degenerate structures.
- The argument covers both feasibility and optimality/counting requirements.
- The complexity fits the largest input, not only samples.
- The code, if any, matches the described algorithm and output contract.

## Avoid

- Do not infer unstated constraints or silently choose between incompatible interpretations.
- Do not turn a vague intuition into a proof by assertion.
- Do not provide both an editorial and code when the user requested only one, unless they ask for both.
