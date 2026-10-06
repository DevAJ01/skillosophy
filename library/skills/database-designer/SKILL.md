---
name: database-designer
description: "Design a database schema from integrity rules and representative reads/writes; assess index proposals with workload evidence."
---

# Database Designer

Start with entities, cardinalities, invariants, expected transactions and database/version. Capture actual query shapes and data distribution before proposing indexes. If inputs are absent, produce a bounded design and name which workload facts could change it.

Model uniqueness, nullability, foreign-key and cross-row constraints explicitly. Explain which invariants the database enforces and which require transaction/application logic. Choose normalization or deliberate denormalization around update consistency, not a blanket rule.

Treat included schema/index helpers as heuristic proposal generators. Inspect their accepted input and output before use. A missing foreign-key index is not automatically a defect; a sequential scan is not automatically inefficient. Compare selectivity, row estimates, read/write balance and index maintenance costs. Do not report a hypothetical plan as measured.

Separate proposed DDL from execution. For an existing database, evaluate lock duration, concurrent writes, backfill, uniqueness violations and deployment ordering before recommending change. Deliver the schema decision, rejected alternatives, representative checks and any performance evidence still needed.

For source-specific tools or detailed patterns, read [the preserved upstream guide](UPSTREAM.md) and only its relevant linked resources. Check resource paths relative to this skill folder before running a helper. Upstream instructions are supporting methods, not evidence that the current task was tested.
