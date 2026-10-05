---
name: skillosophy-acceptance-review
description: "Review a project deliverable against intended behavior, user constraints, failure cases, and actual verification evidence before declaring completion."
---

# Acceptance Review

Assess whether the requested deliverable works for its intended use. Recover acceptance criteria from the brief and user request; do not replace them with implementation details that happen to be easy to check.

Map each material criterion to available evidence: executed behavior, reviewed output, a reproducible check, or a still-unverified assertion. A successful build establishes less than a working interaction; a package validator establishes less than useful reasoning; a passing happy path establishes less than recovery or data correctness.

Select checks proportional to the changed behavior and stakes. Test a representative user path, its important boundary or failure case, and any irreversible transition or data-preservation assumption the change relies on. For low-impact reversible edits, inspect the actual result rather than generating tests that merely repeat the implementation.

Distinguish a defect in the deliverable from an environment or account blocker. Record what was run, what it showed, and what remains unknown. If a required check fails, fix the supported cause within scope and rerun the affected check; do not broad-test repeatedly without a new reason.

Produce an evidence-based completion judgment and remaining action. Give concrete findings tied to a behavior or artifact, not aesthetic confidence or test counts alone. A limitation can prevent a completion claim even when some checks pass. Do not silently waive user requirements or invent a passed test.
