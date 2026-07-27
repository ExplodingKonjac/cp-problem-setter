---
name: writing-statement
description: Use when drafting a competitive-programming problem statement from an idea, reviewing an existing statement for judgeability and ambiguity, or explicitly rewriting a statement.
---

# Writing Problem Statements

Write for contestants and judges, not for the solution author. A statement must define one observable task with one unambiguous input/output contract, without implying the intended algorithm.

## Establish the contract first

Extract or confirm the task rules, input fields, output requirement, constraints, special cases, and sample behavior. If any missing detail could change which submissions are accepted—such as contiguity, indexing, tie handling, numeric range, operation limits, scoring, or output alternatives—ask one focused question through the available user-input mechanism. Do not invent those details or draft a final statement while they remain unresolved.

Use the language indicated by the user's context. If it is not clear, ask which language to use. Preserve the source language when reviewing or rewriting an existing statement unless translation is requested.

## Draft a new statement

After the contract is complete, write only the requested statement, organized as appropriate:

1. Title and supplied limits.
2. Problem description: define every object, operation, and required result.
3. Input and output: state field order, types, ranges, and formatting exactly.
4. Constraints: include per-case and aggregate bounds.
5. Examples: provide input, output, and an explanation only when the examples are supplied or their expected results are established.

Use consistent names and notation. Define boundary behavior explicitly. Do not include algorithm hints, proofs, complexity claims, reference code, or solution-specific terminology.

## Review or rewrite an existing statement

For a review request, return issues only. Group concrete findings under ambiguity, input/output format, constraints, samples, consistency, and unintended solution leakage. Identify the exact wording or omission and explain why it prevents reliable judging; do not rewrite unless explicitly asked.

For an explicit rewrite request, retain the established task semantics and return the corrected statement. Ask before resolving any ambiguity that would change those semantics.

## Final check

- Every term used in input, output, and constraints is defined.
- A contestant can determine validity and the required answer for every legal input.
- Constraints support the intended judge behavior and do not contradict examples.
- Samples conform exactly to the stated format.
- The statement is self-contained and algorithm-neutral.

## Avoid

- Do not infer a common problem variant from a vague phrase such as “best subarray.”
- Do not silently change a reviewed problem while reporting issues.
- Do not expose hidden data, checker logic, or the intended algorithm.
