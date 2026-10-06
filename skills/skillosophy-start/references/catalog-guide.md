# Catalog guidance

The directly installable curated catalog is complemented by the broader discovery library and reviewed extensions described in [the library guide](library-guide.md). The catalog covers practical project workflows, optional philosopher lenses, and selected external skills. Selection is a judgment of task fit, not an automatic score. Do not assign ratings that the catalog does not contain.

Start from the artifact and obstacle. A browser application may need browser-flow verification; a notebook needs reproducible notebook work; PDF layout needs rendering checks. A purely local script does not need a deployment skill. A permission or scheduling dispute can benefit from a philosopher, but routine implementation does not need ten philosophical lenses.

The upstream entries are checked source and license pointers from openai/skills at an immutable revision. Their evidence status is provenance-only: they are not independently established performance improvements. Keep them unchanged, retain licenses and notices, and inspect their task-specific prerequisites. Some helper examples assume global skill locations; resolve helpers from the actual project-local skill folder or use the documented helper-path environment variable. Do not change CODEX_HOME to make examples work.

Prefer already-available capabilities when they fit. Installation creates project portability; it does not make unavailable browser tools, connectors, system dependencies, credentials, or APIs available. Do not install dependencies or connect services merely because the selected skill mentions them.

Catalog expansion requires a scoped description, source and license, immutable revision for external files, dependencies, prerequisites, and evidence status. More entries do not imply better coverage. A missing specialty should lead to a focused source search or new skill, not a weak recommendation dressed as certainty.
