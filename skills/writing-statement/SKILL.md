---
name: writing-statement
description: Use when drafting a competitive-programming problem statement from an idea, reviewing an existing statement for judgeability and ambiguity, or explicitly rewriting a statement.
---

# Writing Problem Statements

Write for contestants and judges, not for the solution author. A statement must define one observable task with one unambiguous input/output contract, without implying the intended algorithm.

## Establish the contract

Extract or confirm the task rules, input fields, output requirement, constraints, special cases, and sample behavior. If a missing detail could change which submissions are accepted—such as contiguity, indexing, tie handling, numeric range, operation limits, scoring, or output alternatives—ask one focused question through the available user-input mechanism. Do not invent those details or draft a final statement while they remain unresolved.

Use the language indicated by the user's context. If it is not clear, ask which language to use, and preserve the source language when reviewing or rewriting an existing statement unless translation is requested.

## Content and style

A judgeable statement carries all of the following information. Treat this as a content checklist, not an outline: choose the organization that presents this problem most clearly, and follow an established platform format when the user or platform supplies one.

- **Task semantics.** Define every object and its domain, the allowed operations, and the exact property, quantity, or object the contestant must determine or construct, including the optimization direction when several answers are possible. State what makes an input instance valid and when the task has a solution.
- **Input contract.** Give the order, type, and range of every field, the separators and line structure, how repeated structures are encoded, and how multiple test cases are grouped or counted.
- **Output contract.** Give the exact required format and the meaning of each value. State how to report a non-unique answer, tie-breaking, required precision, or the absence of a solution.
- **Constraints.** Bound every quantity that appears in the input, and make the scope of each bound explicit: per element, per test case, summed over cases, or across the whole batch. State guarantees the input is promised to satisfy, such as connectivity, distinctness, ordering, or acyclicity.
- **Judging conditions that affect acceptance.** Include time and memory limits, the interaction protocol for interactive problems, subtask and scoring rules, and any other rule a contestant must follow to be judged correct.
- **Samples.** Provide input/output pairs and explanations when they are supplied or their expected results are established; never invent sample output.

Write plain, exact prose: natural language where the task is ordinary, precise notation where the definition is not, with each rule exact as written rather than repaired later.

- **Write clean, natural language.** Use plain, direct sentences and ordinary words, introducing each term before it is used. Remove hedging, filler, and restatements; every sentence should add information a contestant needs. The prose around any notation must still read naturally.
- **Avoid negative patches.** Constrain the intended behavior through precise definitions, conditions, and guarantees, not through statements of what is forbidden or not meant. Do not repair a vague rule by appending a negative clarification such as “note that the array is not circular” or “you may not visit a vertex twice”; strengthen the underlying rule, input contract, or guarantee so the unwanted reading is excluded by definition. A sentence beginning with “note that” or a chain of “except” and “unless” usually signals that the definition itself needs rewriting. Keep a negative clause only when it expresses a genuine condition or guarantee, and prefer the affirmative equivalent even then.
- **Use mathematical language for complex procedures and definitions.** When a definition, construction, or update rule would take a long or ambiguous paragraph, introduce notation and state it as formulas: define each symbol, its domain, and its index ranges, then use it consistently. Reserve prose for intuition and context, and do not force a simple rule into unnecessary notation.

Use consistent names, define each term where it first appears, and state boundary behavior explicitly. Keep the statement self-contained and algorithm-neutral: do not include algorithm hints, proofs, complexity claims, reference code, or solution-specific terminology.

## Draft, review, or rewrite

After the contract is complete, write only the requested statement, conveying the information above in an order and layout that suit the problem. Do not reproduce the checklist as a section skeleton, and do not drop a required detail because no matching heading exists.

For a review request, return concrete issues only, without rewriting. For each issue, identify the exact wording or omission and explain why it prevents reliable judging or could change which submissions are accepted.

For an explicit rewrite request, retain the established task semantics and return the corrected statement. Ask before resolving any ambiguity that would change those semantics.

## Delivery gate

Confirm before delivering:

- Every term used in input, output, and constraints is defined.
- A contestant can determine validity and the required answer for every legal input.
- Constraints support the intended judge behavior and do not contradict examples.
- Samples conform exactly to the stated format.
- Rules are stated affirmatively and exactly, so no negative clarification is needed to make them unambiguous.
- Complex definitions and procedures use consistent notation, defined where it is introduced, while simple rules stay in prose.
- The statement is self-contained and algorithm-neutral.

**Avoid:**

- Do not infer a common problem variant from a vague phrase such as “best subarray.”
- Do not silently change a reviewed problem while reporting issues.
- Do not expose hidden data, checker logic, or the intended algorithm.
- Do not pad the statement with sections or boilerplate that carry no required information.
