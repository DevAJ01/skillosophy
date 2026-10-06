---
name: performance-profiler
description: "Investigate a measured application bottleneck with representative profiling and controlled comparisons, preserving output correctness."
---

# Performance Profiler

Specify the slow operation, environment, workload and metric: end-to-end latency, throughput, resource use or tail behavior. Reproduce it before choosing an optimization. Keep test input and output semantics stable across comparisons.

Profile the relevant layer rather than inferring the bottleneck from code appearance. Separate CPU, I/O, allocation, contention and external-service time. Check whether instrumentation or debug builds materially alter the result. Use traces/profiles actually available; request missing evidence rather than inventing it.

Test one causal proposal at a time when practical. Use repeated measurements appropriate to variance and account for warm-up, caches and concurrency. Report distributions/sample size where available, not one favorable run. A faster path that changes correctness, durability or security is a different product decision.

Deliver the observed bottleneck, proposed change, representative before/after evidence, correctness checks and remaining uncertainty. Do not use upstream benchmark numbers as this project's measured gains.

For source-specific tools or detailed patterns, read [the preserved upstream guide](UPSTREAM.md) and only its relevant linked resources. Check resource paths relative to this skill folder before running a helper. Upstream instructions are supporting methods, not evidence that the current task was tested.
