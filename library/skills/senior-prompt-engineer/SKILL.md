---
name: senior-prompt-engineer
description: "Revise prompts through controlled task evaluation, measuring useful output and regressions rather than prompt style."
---

# Senior Prompt Engineer

Define the outcome, task distribution, baseline prompt, model/tool configuration and constraints. Preserve the user's requested task and authorization while editing instructions.

Turn observed failures into narrow prompt hypotheses. Separate instruction ambiguity from missing facts, missing tools or model capability limits. Longer prompts and named frameworks are not improvements by themselves.

Split development examples from held-out tasks. Compare baseline and revision on the same inputs with comparable output constraints; use repeated sampling where variance matters. Keep judges blind to the condition where practical and use observable correctness, usefulness and compliance criteria. Do not tune to the held-out answers.

Report actual outputs, wins/ties/regressions, sample size, configuration and available token/latency costs. If no evaluation can run, provide the candidate and executable evaluation plan, labeled unmeasured. Retain prompt provenance and rollback so a regression does not silently replace the working version.

For source-specific tools or detailed patterns, read [the preserved upstream guide](UPSTREAM.md) and only its relevant linked resources. Check resource paths relative to this skill folder before running a helper. Upstream instructions are supporting methods, not evidence that the current task was tested.
