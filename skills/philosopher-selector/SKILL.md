---
name: philosopher-selector
description: "Choose a suitable philosophical reasoning skill from a user's task, explain the fit, and apply it or provide a portable invocation. Use when the user needs help selecting a lens."
---

# Skillsophy Philosopher Selector

Choose the smallest useful set of lenses for the user's actual work. The current catalog contains ten philosophical lenses; it does not yet search or recommend third-party skills.

## Selection

Identify the deliverable, the main obstacle to a good answer, and any material constraints. Infer these from the request when possible; ask a single focused question only if it would change the recommendation. Do not force users to learn philosophical terminology or choose among ten names before helping them.

Read [the routing catalog](references/catalog.md). Match the obstacle to a method, not a keyword or a fashionable philosopher. Recommend one primary lens and explain what useful change it should produce. Offer a second lens only if it addresses a distinct weakness. Suggest the council when a genuine conflict among perspectives warrants comparison, rather than reflexively loading every skill.

For a straightforward calculation, transcription, factual lookup, or implementation whose requirements are settled, recommend direct execution when philosophy would add no value. Preserve an explicitly requested lens while acknowledging a weak fit; use its relevant move lightly.

## Apply or hand off

If the selected skill is available, load its SKILL.md and follow it to complete the user's task. When the package is accessible by files, the catalog provides relative paths. When it is available through the host's skill loader, use the exact skill identifier. Read only the selected skill and references required for the task.

If a skill cannot be loaded, explain that limitation and give its exact name plus a copy-ready invocation; do not pretend it was loaded or silently substitute an invented version. Recommendation alone is sufficient when the user asks only what to choose. Otherwise apply the selected lens and deliver the requested work.

## User-facing result

Give the selected name, one sentence explaining fit, and the resulting answer or invocation. Label the fit as a judgment, not an effectiveness score. Do not describe any skill as proven better without evidence for the relevant model and task.

Example: For “Our retention improved after launch; did the tutorial cause it?”, choose philosopher-popper because the obstacle is competing causal explanations. For “What does intelligent mean in this specification?”, choose philosopher-wittgenstein. For “Convert 18°C to Fahrenheit”, do the conversion directly.

## Future catalog boundary

Third-party discovery is planned, not implemented. A future catalog must distinguish measured improvements from popularity, testimonials, or author claims, check licensing and provenance, and preserve user authorization before installation. Until that catalog exists, do not claim to search it or give fabricated success rankings.
