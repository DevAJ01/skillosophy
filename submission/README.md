# Skillosophy public submission preparation

Status: **package prepared; not uploaded or submitted**. The account plugin remains private. Public submission preparation is separate from the existing private release.

The user selected Ashan Jeevanathan as an individual publisher, free access, all supported countries, and GitHub Issues for support. The publication country list is explicitly empty, removing country restrictions. Publisher identity still needs verification and selection in the Portal.

The package contains 17 skills, project-start onboarding, a square PNG icon, a default prompt within 128 characters, four verified public listing URLs, release notes, and a false commerce declaration. The manifest's portable and compatibility forms are synchronized. No private app bindings, MCP server, credentials, or unsupported claims are included.

The original collection has 22 installable catalog entries. Roles are specialist instructions, not configured or running subagents. Initial philosopher comparisons mostly tied a strong baseline; installer verification does not establish general performance improvements.

## Policies and feedback

Published [support](../docs/SUPPORT.md), [privacy](../docs/PRIVACY.md), and [terms](../docs/TERMS.md) describe the actual implementation. GitHub Issues collects voluntary public feedback. Automatic analytics is not implemented. The user's interest in future data collection has not been treated as authorization to introduce telemetry or collect project data.

`url-verification.json` records public, unauthenticated access and content checks for the product, support, privacy, and terms URLs on 6 October 2026.

## Build and inspect

Run `python3 submission/build_draft.py`. The output is `dist/skillosophy-0.2.1-submission-DRAFT.zip`. The builder inspects archived manifests, prompt lengths, icons, inventory, and public-upload restrictions. `validation.json` separates completed package checks from pending Portal steps.

The generated listing and composer icon is `assets/skillosophy-icon.png`, a 1254 × 1254 PNG below 5 MiB. Its charcoal mark and opaque ivory background suit both light and dark surfaces. Optional separate dark assets and brand colors are omitted, consistent with neutral styling.

This is a skills-only plugin: no MCP app cases, demo recording, or reviewer credentials are required. Local validation does not replace Portal checks.

## Pending online stage

On 6 October 2026, opening the Plugins dashboard reached the OpenAI Platform sign-in screen. No submission draft was created or uploaded. Sign in at https://platform.openai.com/plugins using the intended publisher account, then inspect the organization, verified individual identity, and any existing submission before uploading.

Upload creates a draft, not a public release. Check imported metadata and automated findings against the exact saved version. The authorized developer must complete identity verification and legal/policy attestations. Submission for review and publication of an approved release are separate states.

The preparation skill requires the authorized developer to complete legal/policy attestations. It does not permit inferring those facts or agreement from a request to publish. See the Plugin Creator prepare-plugin-submission skill.

References: [OpenAI submission documentation](https://developers.openai.com/plugins/deploy/submission), [public source](https://github.com/DevAJ01/skillosophy).
