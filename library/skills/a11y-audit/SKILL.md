---
name: a11y-audit
description: "Audit a supplied interface through keyboard, focus, semantics and task completion; separate automated findings from manual coverage."
---

# A11Y Audit

Define the pages/components and user tasks actually in scope. Establish the intended accessibility standard when supplied. Review the rendered interface rather than concluding from source syntax alone.

Exercise keyboard entry, navigation, activation, escape and return focus for dialogs and menus. Assess accessible names, roles, labels, error association and announcements for changing state. Check whether the whole task can be completed, including validation and recovery.

Use available automated tooling to find supported failures, then manually inspect behavior the tool does not establish. A zero-violation report is not proof of compliance. Avoid claiming a screen-reader result unless that interaction was actually tested; describe source/semantic inspection separately.

For each finding, supply reproduction, affected task, evidence and a targeted correction. Recheck the correction through the same interaction. Preserve intended behavior and report untested devices, assistive technologies or pages. Do not invent conformance percentages from a small page sample.

For source-specific tools or detailed patterns, read [the preserved upstream guide](UPSTREAM.md) and only its relevant linked resources. Check resource paths relative to this skill folder before running a helper. Upstream instructions are supporting methods, not evidence that the current task was tested.
