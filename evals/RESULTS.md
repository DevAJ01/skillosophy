# Skillsophy evaluation evidence

The initial collection is usable and passed the tested tasks, but these experiments **do not establish a meaningful general improvement over a strong AI baseline**.

| Pilot | Paired tasks | Score wins / ties / losses | Blinded preferences for skills | Baseline / skill mean |
|---|---:|---|---:|---|
| [Initial](results/initial/REPORT.md) | 24 | 3 / 21 / 0 | 3 | 9.875 / 10.000 |
| [Harder transfer](results/transfer/REPORT.md) | 12 | 0 / 12 / 0 | 2, despite equal coarse scores | 10.000 / 10.000 |

No material skill-assisted failure was flagged by either judge. That is an observation about these tasks, not a guarantee. The remaining pairwise preferences were ties; neither judge preferred the baseline.

The initial advantages concerned explicit rule testing, use clarification, and an investigation stopping condition. The transfer preferences concerned a reviewable budget allocation and a comparative trial design. These are useful details to inspect, but their inclusion is not evidence of a measurable real-world gain. The rubric's ceiling effects prevent interpreting its small deltas as strong evidence.

Both pilots used separate instances of the same session model and one fresh blinded model judge per suite. No independent humans, alternative model families, repeated runs, neutral equal-length prompt control, or real-user outcomes were included. The skill condition had additional instruction text. The harder cases were designed by a baseline-only agent that had never loaded the skills; they were tested against unchanged version 0.1.0 skill text.

An [independent philosophical review](../docs/PHILOSOPHY_REVIEW.md) found one low-severity Rawls ambiguity. Version 0.1.1 clarifies that an improvement over the status quo alone does not satisfy the difference principle: among arrangements meeting the prior principles, the greatest feasible benefit to the least advantaged matters. The broad pilot results above belong to the earlier text. The affected cases and a focused comparative regression are [checked separately for the revision](results/rawls-revision/REPORT.md); they are not additional paired-effectiveness results.

Before describing a skill as reliably improving agents, evaluate held-out real tasks across models with repeated runs and domain review, and measure the requested outcome and user effort. Until then, present these as practical reasoning workflows with preliminary evidence, not a proven performance upgrade.

[Protocol and reproducibility files](README.md)
