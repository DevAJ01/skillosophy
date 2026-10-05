# Initial exploratory evaluation

24 paired tasks, independently generated baseline and skill-assisted answers, one blinded model judge. Scores are 0–10 under a coarse rubric. All agents inherited the same session model; exact sampling parameters and model revision were not independently recorded. This is not cross-model or human validation.

| Group | Baseline mean | Skill mean | Mean paired difference | Wins / ties / losses |
|---|---:|---:|---:|---|
| Overall | 9.88 | 10.00 | +0.12 | 3 / 21 / 0 |
| application | 9.83 | 10.00 | +0.17 | 2 / 10 / 0 |
| regression | 9.92 | 10.00 | +0.08 | 1 / 11 / 0 |

## Per-case evidence

| Case | Baseline | Skill | Difference |
|---|---:|---:|---:|
| socrates-1 | 10 | 10 | +0 |
| kant-1 | 9 | 10 | +1 |
| nietzsche-1 | 10 | 10 | +0 |
| epictetus-1 | 10 | 10 | +0 |
| popper-1 | 10 | 10 | +0 |
| wittgenstein-1 | 9 | 10 | +1 |
| rawls-1 | 10 | 10 | +0 |
| mill-1 | 10 | 10 | +0 |
| aristotle-1 | 10 | 10 | +0 |
| descartes-1 | 10 | 10 | +0 |
| selector-1 | 10 | 10 | +0 |
| council-1 | 10 | 10 | +0 |
| socrates-2 | 10 | 10 | +0 |
| kant-2 | 10 | 10 | +0 |
| nietzsche-2 | 10 | 10 | +0 |
| epictetus-2 | 10 | 10 | +0 |
| popper-2 | 10 | 10 | +0 |
| wittgenstein-2 | 10 | 10 | +0 |
| rawls-2 | 10 | 10 | +0 |
| mill-2 | 10 | 10 | +0 |
| aristotle-2 | 10 | 10 | +0 |
| descartes-2 | 9 | 10 | +1 |
| selector-2 | 10 | 10 | +0 |
| council-2 | 10 | 10 | +0 |

## Interpretation limits

Read the actual answers and `judgments.json`, not just scores. Cases are a small non-random sample; scores are subjective and can saturate. Word limits match, but prompt lengths differ. Cases are batched, so there is possible context carryover. No repeated sampling, neutral equal-length control, human review, latency/cost measurement, or independent model family is included. Method-specific detail can influence a judge even without a clear improvement to the user's decision.

A tie means this judge did not distinguish quality at this resolution; a win does not prove general superiority. Any regression remains in the public record. Use this pilot to guide further testing, not as a success badge. See [the full protocol](../../README.md).
