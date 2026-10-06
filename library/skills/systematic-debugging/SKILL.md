---
name: systematic-debugging
description: "Diagnose a reproducible failure through competing hypotheses, discriminating observations and a verified minimal correction."
---

# Systematic Debugging

Capture the observed failure, expected behavior, reproduction and environment. Identify which observations are reliable before explaining a cause. A plausible narrative is a hypothesis, not a diagnosis.

Form a small set of materially different causes and identify a check that would separate them. Inspect the smallest relevant path and test assumptions at boundaries: inputs, state, dependency responses and concurrency. Preserve logs/source data when needed for diagnosis.

Change the cause rather than suppressing the symptom. Compare the original reproducer before and after the fix and add a regression check that would fail under the original defect when appropriate. Do not add a test that merely repeats the new implementation.

If reproduction or execution is unavailable, provide a bounded hypothesis and next discriminating check; do not claim the fix was verified. Deliver the cause supported by evidence, correction, checks run and practical limits.

For source-specific tools or detailed patterns, read [the preserved upstream guide](UPSTREAM.md) and only its relevant linked resources. Check resource paths relative to this skill folder before running a helper. Upstream instructions are supporting methods, not evidence that the current task was tested.
