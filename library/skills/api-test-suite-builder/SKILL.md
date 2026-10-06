---
name: api-test-suite-builder
description: "Build API tests around contracts and state transitions with reproducible fixtures, semantic assertions and isolated side effects."
---

# Api Test Suite Builder

Read the actual contract, implementation boundary and existing test tooling. Identify user-visible behaviors, state transitions and failure cases before selecting a test framework.

Cover representative success, malformed inputs, authorization boundaries, not-found/conflict conditions and idempotency where promised. An HTTP 200 assertion alone does not establish correct behavior. Check response values and durable state with the right actor/tenant context.

Use isolated data and deterministic fixture setup/cleanup. Distinguish mocked contract tests from live integration tests; mocks cannot establish service connectivity. Avoid sending destructive test calls to a production URL merely because one appears in a configuration file.

Run the appropriate available suite and capture actual results. Report skips and unresolved prerequisites separately. For asynchronous behavior, assert the eventual contract with bounded waiting and useful diagnostics instead of arbitrary sleeps. Preserve the project's existing framework unless a change is required by the task.

For source-specific tools or detailed patterns, read [the preserved upstream guide](UPSTREAM.md) and only its relevant linked resources. Check resource paths relative to this skill folder before running a helper. Upstream instructions are supporting methods, not evidence that the current task was tested.
