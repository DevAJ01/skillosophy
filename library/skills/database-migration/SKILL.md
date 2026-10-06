---
name: database-migration
description: "Prepare and validate database changes with writer compatibility, restartable backfills and explicit recovery limits."
---

# Database Migration

Inspect the existing schema, desired change, database/version and migration tooling. Determine table size, write load and lock constraints where available. A development migration that succeeds on empty data does not establish production feasibility.

Make the change compatible with the application versions that coexist during rollout. Separate additive schema, data backfill, application switch and destructive cleanup where required. Define repeat/retry behavior and account for partially completed runs.

Validate values and domain invariants, not only row counts. Determine how concurrent writes are included and how cutover consistency is established. Explain whether rollback can preserve new writes; dropping the new column is not a complete data recovery strategy.

Produce proposed migration and verification/recovery steps. Inspect generated SQL before execution and state which environment was actually tested. Do not claim zero downtime or reversibility without evidence supporting those properties.

For source-specific tools or detailed patterns, read [the preserved upstream guide](UPSTREAM.md) and only its relevant linked resources. Check resource paths relative to this skill folder before running a helper. Upstream instructions are supporting methods, not evidence that the current task was tested.
