---
name: migration-architect
description: "Plan a staged migration with compatibility, data reconciliation and recovery criteria appropriate to the actual system."
---

# Migration Architect

Establish the source/target contract, data volume, downtime budget, writer versions and deployment constraints. Enumerate which old and new producers/consumers coexist at each phase. Explain what makes cutover reversible; a generated rollback file is not proof of recovery.

Design expand, backfill, verify, switch and contract stages only where the system needs them. Backfills need restartability, stable boundaries and a policy for writes arriving during copying. A dual-write plan must handle partial success and ordering; do not assume independent writes are atomic.

Define reconciliation around counts, keys, checksums or domain invariants as appropriate. Counts alone can miss corrupted values. Set concrete stop/cutover criteria, who makes the decision and the recovery window. After destructive contraction, rollback may require a backup or a forward fix rather than an inverse DDL statement.

Use included planners/checkers as aids after checking their schemas and assumptions. Deliver a phase runbook with prerequisites, validation, failure response and recovery limits. Planning does not authorize running migrations or reconnecting production services.

For source-specific tools or detailed patterns, read [the preserved upstream guide](UPSTREAM.md) and only its relevant linked resources. Check resource paths relative to this skill folder before running a helper. Upstream instructions are supporting methods, not evidence that the current task was tested.
