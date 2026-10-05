# Initial exploratory evaluation

24 paired tasks, independently generated baseline and skill-assisted answers, one blinded model judge. Scores are 0–10 under a coarse rubric. All agents inherited the same session model; exact sampling parameters and model revision were not independently recorded. This is not cross-model or human validation.

| Group | Baseline mean | Skill mean | Mean paired difference | Wins / ties / losses |
|---|---:|---:|---:|---|
| Overall | 9.88 | 10.00 | +0.12 | 3 / 21 / 0 |
| application | 9.83 | 10.00 | +0.17 | 2 / 10 / 0 |
| regression | 9.92 | 10.00 | +0.08 | 1 / 11 / 0 |

Blind pairwise preferences: {'tie': 21, 'skilled': 3}. These can differ from coarse score ties.

## Per-case evidence

| Case | Baseline | Skill | Difference | Preference |
|---|---:|---:|---:|---|
| socrates-1 | 10 | 10 | +0 | tie |
| kant-1 | 9 | 10 | +1 | skilled |
| nietzsche-1 | 10 | 10 | +0 | tie |
| epictetus-1 | 10 | 10 | +0 | tie |
| popper-1 | 10 | 10 | +0 | tie |
| wittgenstein-1 | 9 | 10 | +1 | skilled |
| rawls-1 | 10 | 10 | +0 | tie |
| mill-1 | 10 | 10 | +0 | tie |
| aristotle-1 | 10 | 10 | +0 | tie |
| descartes-1 | 10 | 10 | +0 | tie |
| selector-1 | 10 | 10 | +0 | tie |
| council-1 | 10 | 10 | +0 | tie |
| socrates-2 | 10 | 10 | +0 | tie |
| kant-2 | 10 | 10 | +0 | tie |
| nietzsche-2 | 10 | 10 | +0 | tie |
| epictetus-2 | 10 | 10 | +0 | tie |
| popper-2 | 10 | 10 | +0 | tie |
| wittgenstein-2 | 10 | 10 | +0 | tie |
| rawls-2 | 10 | 10 | +0 | tie |
| mill-2 | 10 | 10 | +0 | tie |
| aristotle-2 | 10 | 10 | +0 | tie |
| descartes-2 | 9 | 10 | +1 | skilled |
| selector-2 | 10 | 10 | +0 | tie |
| council-2 | 10 | 10 | +0 | tie |

## Interpretation limits

Read the actual answers and `judgments.json`, not just scores. Cases are a small non-random sample; scores are subjective and can saturate. Word limits match, but prompt lengths differ. Cases are batched, so there is possible context carryover. No repeated sampling, neutral equal-length control, human review, latency/cost measurement, or independent model family is included. Method-specific detail can influence a judge even without a clear improvement to the user's decision.

A tie means this judge did not distinguish quality at this resolution; a win does not prove general superiority. Any regression remains in the public record. Use this pilot to guide further testing, not as a success badge. See [the full protocol](../../README.md).
