# Behavioral evaluation

The question is whether a skill improves a useful outcome compared with the same AI doing the same task without the skill. Fluency, longer answers, philosopher names, and correct file formatting are insufficient evidence.

## Current protocol

`cases.json` now contains 34 author-designed fixtures. The original 24 were used in the philosopher pilot; the ten added project-workflow fixtures have not been run as a paired baseline experiment. The original 24 include one application and one regression case for each of the ten philosopher lenses, the selector, and the council. Application cases ask for a concrete deliverable. Regression cases challenge characteristic failure modes and user-constraint handling.

1. Give a fresh generator only the case prompts and ordinary competent-assistant instructions. Obtain a baseline answer for every ID. Do not load skills or show rubrics.
2. Give a separate fresh generator the same case prompts plus the designated skill and required references. Obtain actual answers and log which skills were loaded. Do not show baseline answers or rubrics.
3. Use the same model, configuration, task facts, word limits, and tool availability. A task explicitly asking for a philosopher remains identical in both conditions; this makes the baseline strong. Record configuration you can actually observe. Do not infer unavailable model settings.
4. Prepare a packet with `python3 scripts/blind_eval.py BASELINE.json SKILLED.json OUTPUT_DIR --seed 20261005`. Give the judge only `packet.json`, never `key.json`. Random A/B order reduces position bias; writing style can still reveal the condition.
5. Judge each answer before expressing pairwise preference. Score correctness, evidence handling, practical usefulness, instruction compliance, and relevant insight from 0 to 2 each. Use 0 for absent or materially wrong, 1 for partial, and 2 for strong. Case criteria identify specific behaviors to inspect, not mandatory vocabulary. Do not reward a maxim, philosophical label, or named framework without a useful reasoning contribution.
6. Record a brief reason and any material failure for each answer. Apply exactly the same rubric to both conditions. Unblind only after scores are saved. Report per-case scores, wins/ties/losses, application/regression subsets, and failures. Publish actual answers and judge explanations, not only the aggregate.

A separate model instance with no answer-key access is a blinded model judge, **not** an independent human or a different model family. The generators process cases in a batch, so context carryover cannot be ruled out even when instructed to keep cases separate. Record these limitations.

## What this pilot can establish

It can expose a broken workflow, unsupported claims, missed constraints, or promising specific improvements. It cannot establish general superiority, causal attribution to an individual instruction, philosophical completeness, or performance on other models.

The author knows the skills and cases. Skills are longer than baseline instructions; equal answer budgets do not match input-token costs. There is one generated answer per condition per case, no repeated stochastic sampling, and no model diversity. Do not interpret small score differences as significant. Report ties and regressions honestly. Measure input/output tokens, latency, and cost in a production evaluation where the harness exposes them; this in-chat pilot does not measure those metrics.

## Stronger validation before a proven-improvement claim

Recruit tasks from real users without editing skills to the held-out set. Compare a neutral reasoning prompt of similar length, not only a bare baseline, to separate philosophy-specific value from extra instructions. Run multiple randomized repetitions, diverse models, and human domain review. Define success and acceptable regressions before examining results. Split development and held-out tasks; rerun the latter only for a release decision, and replace them if they become tuning material. Measure outcome quality and interaction burden rather than explanation style alone.

Use paired effect sizes and uncertainty intervals appropriate to the sampling design. Cluster by task when repeated runs share the same prompt. For philosopher-specific improvement claims, use enough independent tasks per lens; two cases per lens are not sufficient. Do not derive a confidence interval from 24 correlated hand-written cases and present it as generalization evidence.

## Artifacts

The initial run's answers, blinding key, scoring records, and [report](results/initial/REPORT.md) live under `results/initial/`. The harder [transfer report](results/transfer/REPORT.md) and its artifacts live under `results/transfer/`. That suite, designed by a baseline-only agent without reading the skills, is evaluated separately against the unchanged skill text. It remains a small single-model exploratory sample, not an externally validated benchmark. Preserve the blinding key for audit after judging. These hypothetical cases contain no customer data. The ZIP is a package test, not a behavioral evaluation result.
