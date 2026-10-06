---
name: api-design-reviewer
description: "Review a proposed API change for compatibility, semantics and client impact; distinguish convention scores from actual breaking behavior."
---

# Api Design Reviewer

Read the existing API contract, change and known callers. Identify the compatibility direction: new server with old client, and old server with new client where rolling deployment requires it. Establish the project's naming/versioning conventions rather than imposing the examples in the upstream guide.

Construct a change matrix covering required request fields, response removals/type changes, enum expansion, nullability, authentication, pagination and error semantics. A newly required request field can break old callers; a newly returned enum value can break exhaustive client handling even when JSON remains valid. Check generated SDK behavior where relevant.

Use the included linting, change detector and scorecard only after inspecting their supported spec version and dependencies. Their grades are heuristics. Confirm important findings against representative caller inputs and outputs; a high score cannot cancel an observed break. Do not modify a production API merely to improve naming consistency.

Produce findings with affected client, concrete before/after example, severity rationale and remedy. Distinguish intentional versioned changes from accidental incompatibility. Report tools actually run, unsupported constructs and unresolved caller evidence.

For source-specific tools or detailed patterns, read [the preserved upstream guide](UPSTREAM.md) and only its relevant linked resources. Check resource paths relative to this skill folder before running a helper. Upstream instructions are supporting methods, not evidence that the current task was tested.

The upstream “run all tools first” example is conditional on having a supported contract and a task requiring those tools. It does not override the requested scope or make a heuristic grade a release approval.
