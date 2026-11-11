---
name: writing-statement
description: Use when drafting a competitive-programming problem statement from an idea, reviewing an existing statement for judgeability and ambiguity, or explicitly rewriting a statement.
---

# Writing Problem Statements

Write for contestants and judges, not for the solution author. A statement must define one observable task with one unambiguous input/output contract, without implying the intended algorithm.

## Establish the contract first

Extract or confirm the task rules, input fields, output requirement, constraints, special cases, and sample behavior. If any missing detail could change which submissions are accepted—such as contiguity, indexing, tie handling, numeric range, operation limits, scoring, or output alternatives—ask one focused question through the available user-input mechanism. Do not invent those details or draft a final statement while they remain unresolved.

Use the language indicated by the user's context. If it is not clear, ask which language to use. Preserve the source language when reviewing or rewriting an existing statement unless translation is requested.

## What the statement must convey

A judgeable statement carries all of the following information. Treat this as a content checklist, not as an outline: choose the organization, headings, and order that present this particular problem most clearly; follow an established platform format when the user or platform supplies one, but never impose a fixed template of your own.

- **Task semantics.** Define every object and its domain, the allowed operations, and the exact property, quantity, or object the contestant must determine or construct, including the optimization direction when several answers are possible. State what makes an input instance valid and when the task has a solution.
- **Input contract.** Give the order, type, and range of every field, the separators and line structure, how repeated structures are encoded, and how multiple test cases are grouped or counted.
- **Output contract.** Give the exact required format and the meaning of each value. State how to report a non-unique answer, tie-breaking, required precision, or the absence of a solution.
- **Constraints.** Bound every quantity that appears in the input, and make the scope of each bound explicit: per element, per test case, summed over cases, or across the whole batch. State guarantees the input is promised to satisfy, such as connectivity, distinctness, ordering, or acyclicity.
- **Judging conditions that affect acceptance.** Include time and memory limits, the interaction protocol for interactive problems, subtask and scoring rules, and any other rule a contestant must follow to be judged correct.
- **Samples.** Provide input/output pairs and explanations when they are supplied or their expected results are established; never invent sample output.

Use consistent names and notation, define each term where it first appears, and state boundary behavior explicitly. Keep the statement self-contained and algorithm-neutral: do not include algorithm hints, proofs, complexity claims, reference code, or solution-specific terminology.

## Draft a new statement

After the contract is complete, write only the requested statement, conveying the information above in an order and layout that suit the problem. Do not reproduce this checklist as a section skeleton, and do not drop a required detail because no matching heading exists.

## Review or rewrite an existing statement

For a review request, return concrete issues only, without rewriting. For each issue, identify the exact wording or omission and explain why it prevents reliable judging or could change which submissions are accepted.

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
- Do not pad the statement with sections or boilerplate that carry no required information.
