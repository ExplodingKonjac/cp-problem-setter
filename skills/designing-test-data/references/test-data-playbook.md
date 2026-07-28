# Generative Test-Data Playbook

## Contents

- [Diagnose semantic collapse](#diagnose-semantic-collapse)
- [Build a richer probability law](#build-a-richer-probability-law)
- [Use the oracle as an instrument](#use-the-oracle-as-an-instrument)
- [Choose domain models](#choose-domain-models)
- [End-to-end example](#end-to-end-example)
- [Add the safety audit](#add-the-safety-audit)
- [Common failures](#common-failures)

## Diagnose semantic collapse

A generator samples inputs from a distribution \(P_X\). The reference solution maps each input to semantic observations \(F(X)\): the official answer and useful witness properties. Inspect the induced distribution of \(F(X)\), not only the serialized input.

Start by asking:

- Which input variables actually control the solution?
- What does the naive random law make overwhelmingly likely?
- Which phase transitions or structural regimes occupy very little probability mass?
- Do different seeds produce new semantic behavior or only new surface values?
- Which output features should remain dependent, such as query length and range minimum?

Typical collapse includes nearly every answer being zero, one global minimum answering most queries, almost every graph being connected, optimum witnesses having the same length, or all feasible instances having the same certificate shape.

## Build a richer probability law

Use a hierarchical model:

1. Sample a **climate** describing broad behavior.
2. Sample case-level latent parameters from wide priors.
3. Generate irregular local structure conditionally on those parameters.
4. Add fine noise inside the structure rather than after it.

Useful ingredients:

- Mixtures of stationary, clustered, trend-driven, sparse, dense, smooth, and shock-heavy climates.
- Log-scale priors for sizes, magnitudes, durations, gaps, densities, and perturbations.
- Renewal or Markov processes for irregular regime changes.
- Heavy-tailed component sizes, run lengths, or degree propensities.
- Correlated noise, random fields, latent ranks, and slowly changing parameters.
- Sampling around phase transitions instead of only deep inside stable regimes.

Randomize mixture weights or latent priors between cases when appropriate. Avoid a fixed menu whose modes leave recognizable fingerprints. The climates should overlap: one realization may be both clustered and shock-heavy, or both sparse and strongly correlated.

Prefer sampling semantic causes to choosing an exact official answer. Answer-first construction is appropriate only when the problem naturally exposes that answer as a structural parameter, and even then randomize the conditional structure richly and verify that answer classes do not have unique visible signatures.

## Use the oracle as an instrument

Generate a candidate pool larger than the retained suite. Run the trusted reference and record semantic features for every candidate.

Inspect:

- marginal histograms, quantiles, entropy, and dominant-category share;
- joint distributions such as size × answer, density × component count, or query length × answer rank;
- witness properties such as position, length, multiplicity, depth, topology, or certificate size;
- correlations between visible input summaries and official answers.

If the distribution collapses, first change latent priors, proposal kernels, or mixture weights. Soft selection may then favor underrepresented broad regions:

\[
w(x) \propto \prod_j (1 + C_j(F(x)))^{-\alpha_j},
\]

where \(C_j\) counts an occupied semantic bin and each \(\alpha_j\) is moderate and capped. Keep a substantial untouched baseline sample. Use broad or joint bins, never exact-answer quotas.

Soft selection must not destroy genuine relationships. Long ranges should still tend toward deeper minima; denser random graphs should still tend toward fewer components. The selected suite should broaden the natural distribution, not flatten it into something artificial.

## Choose domain models

| Domain | Latent causes worth sampling | Semantic diagnostics |
| --- | --- | --- |
| Arrays/sequences | Drift, volatility, correlation length, regimes, shocks, latent ranks, quantization | Answer scale, optimum length/position, ties, run statistics, prefix extrema |
| Strings | Source entropy, motif duration, mutation rate, periodicity, grammar/state transitions | Match count, border structure, mismatch depth, period, witness spacing |
| Graphs | Component-size process, degree propensities, geometry, closure rate, density climate | Components, isolates, degree/diameter profile, surplus edges, giant share |
| Trees | Branching law, depth bias, attachment kernel, heavy-path persistence | Height, diameter, leaf count, balance, subtree-size distribution |
| Intervals/queries | Cluster centers, length scales, endpoint jitter, latent hotspots | Overlap count, query scale, witness location, tie multiplicity |
| Numeric problems | Factor process, sign law, scale mixture, precision/threshold distance | Feasibility, factor counts, answer magnitude/class, threshold proximity |
| Constructive tasks | Constraint density, latent solution multiplicity, symmetry, slack | Feasibility, certificate size, number of choices, bottleneck location |

These are starting points, not prescribed modes. Derive the model from the problem’s semantic map.

## End-to-end example

Consider static range-minimum queries. Independent uniform array values and independent query endpoints make long queries repeatedly return a few global minima.

### Generate the array landscape

Create a continuous latent score field:

1. Sample several spatial scales log-uniformly.
2. At each scale, generate irregular renewal segments with correlated offsets.
3. Add a slowly changing drift process, fine independent noise, and sparse heavy-tailed shocks.
4. Randomize the relative strength of these components per case.
5. Map latent ranks into legal integers; sometimes keep values distinct, sometimes quantize into a randomly sized alphabet to create natural ties.

This produces smooth basins, record-minimum chains, plateaus, local noise, and deep shocks as overlapping outcomes of one process.

### Generate queries

Sample a large pool from overlapping proposal kernels:

- geometric and log-uniform lengths;
- ordinary random endpoints;
- long ranges with random margins;
- lengths near latent spatial scales;
- a minority centered near valleys, shocks, or regime boundaries with jittered endpoints.

Run the RMQ oracle and record length, answer-rank percentile, tie count, minimum position, and whether a one-step endpoint change changes the answer.

Keep an untouched baseline, then apply capped soft selection over joint length × answer-rank and length × tie-count bins. If long queries still collapse onto one minimum, increase landscape diversity or valley proposals before increasing selection pressure.

Accept the generator when new seeds expand the Cartesian-tree, query-scale, witness-position, and answer profiles while preserving the natural tendency for longer queries to return deeper minima.

## Add the safety audit

Only after the stochastic core is sound:

- Add minimum, maximum, degenerate, and exact format-boundary inputs.
- Benchmark intended and tempting slower algorithms on natural maximum-scale samples.
- Run representative wrong solutions and inspect the kill matrix.
- Improve the stochastic law when a broad failure class survives.
- Keep a fixed regression case only when the failure is too narrow or fragile to reproduce naturally.

The audit checks the distribution; it does not define it.

## Common failures

| Failure | Correction |
| --- | --- |
| Uniform inputs produce concentrated answers | Model the semantic causes and change the probability law |
| Every climate is a visible handcrafted mode | Overlap climates and randomize continuous latent parameters |
| Output categories are forced to equal counts | Use broad diagnostics and capped soft selection |
| Exact answers are chosen before inputs | Sample causal structure; reserve conditioning for natural structural parameters |
| Noise is added after an obvious construction | Generate fine texture conditionally inside the latent structure |
| Input histograms look varied, so the suite is accepted | Inspect joint structural, witness, and output distributions |
| More seeds reproduce the same behavior | Change priors or model family rather than adding seeds |
| Mutants dictate the entire generator | Use mutants as a late audit and improve the general law first |
