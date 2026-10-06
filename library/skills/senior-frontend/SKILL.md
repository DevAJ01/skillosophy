---
name: senior-frontend
description: "Build or review React, Next.js and TypeScript frontends within the existing stack, with accessible interactions, functional states and measured performance."
---

# Senior Frontend

Inspect the existing app, dependency versions, design conventions and requested flow before scaffolding. Reuse its framework and component system. Scaffolding and dependency substitution are appropriate only when the requested work calls for them.

Implement observable states: loading, empty, error, success and relevant permissions. Use native semantics where they fit: a clickable action needs a button, not a styled div. For forms, connect labels/errors and verify focus behavior. Keep authorization and secrets on the trusted server side; hiding controls is not an access check.

Choose client/server boundaries from interaction and data needs in the installed framework version. Read only the relevant upstream pattern references. Inspect generators before use; generated component names do not guarantee correct HTML semantics or a functioning user flow.

For performance work, reproduce the user-visible bottleneck and measure a representative build/interaction. Dependency size tables and static health grades are hints, not the project's measured bundle size. Check delivered chunks, rendering work and network behavior before replacing a dependency. Verify the requested flow and describe actual evidence and remaining limitations.

For source-specific tools or detailed patterns, read [the preserved upstream guide](UPSTREAM.md) and only its relevant linked resources. Check resource paths relative to this skill folder before running a helper. Upstream instructions are supporting methods, not evidence that the current task was tested.

The upstream guide also describes a separately installed frontend agent and sibling specialties. Those optional host-specific routes are not supplied here and are not prerequisites for ordinary component work. Apply the bounded workflow above; do not follow its scaffold, framework-selection or agent-launch examples when they exceed the user's requested change.
