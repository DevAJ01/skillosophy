# Transfer exploratory evaluation

12 paired tasks, independently generated baseline and skill-assisted answers, one blinded model judge. Scores are 0–10 under a coarse rubric. All agents inherited the same session model; exact sampling parameters and model revision were not independently recorded. This is not cross-model or human validation.

| Group | Baseline mean | Skill mean | Mean paired difference | Wins / ties / losses |
|---|---:|---:|---:|---|
| Overall | 10.00 | 10.00 | +0.00 | 0 / 12 / 0 |
| transfer | 10.00 | 10.00 | +0.00 | 0 / 12 / 0 |

Blind pairwise preferences: {'tie': 10, 'skilled': 2}. These can differ from coarse score ties.

## Per-case evidence

| Case | Baseline | Skill | Difference | Preference |
|---|---:|---:|---:|---|
| transfer-socrates | 10 | 10 | +0 | tie |
| transfer-kant | 10 | 10 | +0 | tie |
| transfer-nietzsche | 10 | 10 | +0 | tie |
| transfer-epictetus | 10 | 10 | +0 | tie |
| transfer-popper | 10 | 10 | +0 | tie |
| transfer-wittgenstein | 10 | 10 | +0 | tie |
| transfer-rawls | 10 | 10 | +0 | tie |
| transfer-mill | 10 | 10 | +0 | skilled |
| transfer-aristotle | 10 | 10 | +0 | tie |
| transfer-descartes | 10 | 10 | +0 | tie |
| transfer-selector | 10 | 10 | +0 | tie |
| transfer-council | 10 | 10 | +0 | skilled |

## Interpretation limits

Read the actual answers and `judgments.json`, not just scores. Cases are a small non-random sample; scores are subjective and can saturate. Word limits match, but prompt lengths differ. Cases are batched, so there is possible context carryover. No repeated sampling, neutral equal-length control, human review, latency/cost measurement, or independent model family is included. Method-specific detail can influence a judge even without a clear improvement to the user's decision.

A tie means this judge did not distinguish quality at this resolution; a win does not prove general superiority. Any regression remains in the public record. Use this pilot to guide further testing, not as a success badge. See [the full protocol](../../README.md).
