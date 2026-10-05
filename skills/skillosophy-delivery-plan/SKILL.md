---
name: skillosophy-delivery-plan
description: "Build a staged implementation plan around dependencies, reversible decisions, risks, and acceptance evidence for a complex project."
---

# Delivery Plan

Turn an agreed deliverable into an ordered sequence of useful increments. Start from the project brief and existing architecture, rather than assuming a new stack or a full rewrite.

Locate dependencies that constrain the order: schema or interface agreements, external access, representative data, recovery, or user validation. Separate reversible choices from commitments that would make later correction expensive. Resolve the latter with a proportionate investigation or spike before widespread implementation.

Choose a first slice that demonstrates an end-to-end user outcome. For each following slice, specify what becomes usable, what it depends on, and the evidence needed to move on. Avoid decomposing work solely into frontend/backend/database buckets if integration would remain untested until the end.

Prioritize a risk only when it threatens the requested outcome or a stated constraint. Translate risk into a check, contingency, or narrower scope. Distinguish work that can proceed independently from work that needs a settled shared contract. Use specialist roles where expertise or separate review materially helps; do not manufacture a large agent team or parallelize edits to the same files without ownership boundaries.

Produce a compact delivery plan with milestones, dependencies, acceptance evidence, decision owners or roles when useful, and explicit deferred work. Do not invent effort estimates, claim an external service is connected, or authorize deployment, spending, or new messages through a plan. Complete already-authorized implementation when the user requested it rather than stopping at a plan.
