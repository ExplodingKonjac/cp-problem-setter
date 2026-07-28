---
name: designing-test-data
description: Use when planning competitive-programming test data, defining generator strategies, analyzing weak solutions to target, or reviewing whether a test suite is strong, random-looking, and comprehensive.
---

# Designing Test Data

Design a probability distribution over meaningful problem instances—not a bag of handcrafted cases and not independent uniform noise. Good data has varied local structure, natural correlations, and broad semantic behavior; difficult cases should arise as ordinary samples from a delicate random process.

## Develop taste

Judge a generator by the distribution it induces after the reference solution transforms input into output. Random inputs can still produce nearly constant answers, repeated extrema, one dominant graph shape, or predictable optima.

Keep these principles:

- **Randomize causes, not appearances.** Sample latent structure—regimes, scales, densities, correlations, component shapes, value ranks—then realize the visible input.
- **Prefer mixtures over one law.** Combine several stochastic climates and randomize their parameters continuously. A single uniform distribution explores one narrow notion of “typical.”
- **Work at several scales.** Sample sizes, run lengths, gaps, magnitudes, densities, and perturbations on linear and logarithmic scales. Use irregular boundaries and heavy-tailed or geometric durations when appropriate.
- **Explore phase transitions.** Interesting behavior often lives where connectivity, feasibility, optimal structure, or complexity changes rapidly. Sample around these regions without pinning every case to an exact answer.
- **Preserve natural dependence.** Do not flatten outputs blindly. Query length should still influence range minima; density should still influence connectivity. Seek breadth inside these relationships.
- **Condition softly.** Generate a large candidate pool, evaluate it with the reference, and favor underrepresented semantic regions with broad bins or weighted reservoirs. Keep an untouched baseline sample. Never rewrite jury answers.
- **Let strength emerge.** Correlated noise, competing local regimes, irregular clusters, and multiscale structure naturally exercise more behavior than a visibly planted gadget.

The goal is not statistical uniformity. The goal is a suite whose inputs and outputs do not collapse into a small, predictable set of shapes.

## Design the random process

1. **Model the semantic map.** Identify input features that control the solution and output observables that reveal collapse: answer value or class, witness size and position, component count, optimum length, path shape, degree profile, or query scale.
2. **Diagnose the naive law.** Predict or simulate what uniform generation produces. Look for concentration, symmetry, saturation, trivial answers, hidden correlations, and rare regimes it almost never visits.
3. **Choose latent variables.** Build a hierarchical process with case-level parameters and local variation: mixture component, scale, drift, density, persistence, cluster shape, correlation, or noise level.
4. **Generate a candidate pool.** Draw reproducibly from broad parameter priors. Use continuous jitter and irregular sizes so generator modes do not leave obvious fingerprints.
5. **Measure the pushforward distribution.** Run the trusted reference and inspect both marginal and joint summaries. Useful diagnostics include entropy/effective category count, dominant-answer share, histograms, quantiles, and heatmaps such as answer × size or witness length × position.
6. **Tune, do not sculpt.** Adjust priors, mixture weights, proposal kernels, or soft selection pressure. If a semantic region is rare, oversample the conditions that produce it; do not manufacture exact outputs or alter generated instances after seeing an inconvenient answer.
7. **Freeze a reproducible schedule.** Record modes, parameter priors, pool size, selection policy, seeds, and retained baseline fraction.

## Recognize good and bad randomness

| Weak taste | Better taste |
| --- | --- |
| Independent uniform values everywhere | Hierarchical mixtures with correlations and changing local regimes |
| Fixed blocks with random labels | Random durations, scales, transitions, and internal texture |
| Force equal counts of every answer | Preserve natural relationships while reducing pathological concentration |
| Choose an exact answer, then reverse-engineer input | Sample semantic causes; use broad oracle-guided strata only when needed |
| Add noise after constructing an obvious trap | Make difficult structure a natural outcome of the stochastic model |
| Inspect input histograms only | Inspect joint input, structural, witness, and output distributions |
| Add more seeds to the same weak law | Change the law when new seeds reproduce the same semantic behavior |

## Add the engineering safety net

After the central random process is sound:

- Add minimum, maximum, degenerate, and format-boundary cases that randomness should not be trusted to hit.
- Check performance regimes with realistic maximum-scale samples.
- Run representative wrong solutions and stress testing as audits. Use discovered gaps to improve the stochastic model first; retain exact regression cases only when the failure is too rare or fragile to generate reliably.
- Validate every input and compute every output with the reference solution. Cross-check small samples with an independent brute-force oracle.

Write a design brief describing the stochastic model, parameter priors, semantic observables, diagnostics, tuning policy, edge-case layer, generation schedule, and validation evidence. Read [the generative test-data playbook](references/test-data-playbook.md) for deeper model patterns, domain starting points, and an end-to-end example.

After the design is accepted, use **REQUIRED SUB-SKILL:** `writing-testlib-generators` to implement the reproducible C++ testlib generator.
