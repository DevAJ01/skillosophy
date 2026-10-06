# Skillosophy

**Start your Codex project with the right skills and a clear way of working.**

Before implementation, Skillosophy examines what you want to build, determines the project's working philosophy, selects useful skills, defines specialist-agent role instructions, and installs the selected skills into that project.

“Project philosophy” means practical decision principles: the outcome that matters, tradeoffs, development approach, evidence needed to move forward, and standards for completion. Philosophical reasoning lenses are available when useful; practical project work drives the selection.

## Start a project

Install the Skillosophy plugin and invoke its entry skill in Codex:

```text
Use $skillosophy-start before building my project.
I want to build [deliverable] for [users] in [project folder].
My constraints are [constraints].
Determine the project's working philosophy, choose useful skills and specialist roles,
and install the selected skills into the project.
```

Skillosophy inspects available context, asks only for information that changes the setup, and produces a small, purposeful selection. A request for advice alone produces recommendations; a request to set up project skills proceeds with installation within the stated scope.

The installer places skill folders in `.agents/skills` and saves the project plan, source/hash receipt, and named role instructions in `.skillosophy/setup-<hash>/`. Codex discovers project skills from that directory. Role instructions specify responsibilities and skills; they are not configured or running subagents. The installer preserves existing guidance and refuses changed destination skills rather than overwriting them.

Installation needs a Codex environment with access to the target project. Chat surfaces without filesystem access can prepare the plan for Codex. Installing a skill does not connect services, install its runtime prerequisites, deploy the project, or launch agents.

## Full repository library

The repository now contains [600 complete skill folders](library/README.md), in addition to the original 17 plugin workflows. Twelve major workflows have authored Skillosophy revisions; the rest are attributed upstream candidates. Full resources, licenses, source revisions and hashes are retained. The [evaluation program](library/EVALUATION.md) tracks the remaining work toward 500 independently evaluated revisions. File validation is separate from AI performance testing.

```sh
python3 scripts/library/select.py search "PostgreSQL schema API compatibility" --limit 8
python3 scripts/library/select.py inspect database-designer
```

## Additional discovery sources

Version 0.3.0 includes **180 discoverable skills from seven source-pinned repositories**, live community search through skills.sh, and indexing of additional public GitHub repositories. The directly installable curated catalog has 22 entries; the plugin packages 17 workflows including its startup entry. Discovery results require source, license, dependency, and compatibility review before installation.

| Collection | Included capabilities |
|---|---|
| Original project workflows | [Project brief](skills/skillosophy-project-brief/SKILL.md), [evidence plan](skills/skillosophy-evidence-plan/SKILL.md), [delivery plan](skills/skillosophy-delivery-plan/SKILL.md), [acceptance review](skills/skillosophy-acceptance-review/SKILL.md) |
| Pinned upstream skills | Playwright browser work, PDF work, GitHub CI repair, security best practices, Jupyter notebooks, Vercel deployment |
| Reasoning lenses | Socrates, Kant, Nietzsche, Epictetus, Popper, Wittgenstein, Rawls, Mill, Aristotle, Descartes |
| Reasoning selection | [Philosopher selector](skills/philosopher-selector/SKILL.md) and [council](skills/philosopher-council/SKILL.md) |

Upstream entries point to checked, immutable revisions of [openai/skills](https://github.com/openai/skills), with per-skill licenses and prerequisites. They are fetched only when selected for installation. Provenance and popularity do not establish measured effectiveness. The [catalog](skills/skillosophy-start/references/catalog.json) records that distinction.

The discovery library spans OpenAI, Anthropic, Vercel, Supabase, Remotion, Superpowers, and Microsoft Azure Skills. It is metadata, not 180 preinstalled or benchmarked packages. Search sends generic public keywords to skills.sh; offline search stays local. Install counts describe popularity, not demonstrated success.

The [library guide](skills/skillosophy-start/references/library-guide.md) explains search, repository indexing, pinned source inspection, and reviewed installation. For a missing specialty, inspect a suitable licensed source or use the host's skill-creator workflow to author a focused project skill. Reviewed extensions preserve source hashes, licenses and notices, and cannot replace existing catalog names.

## Development and verification

```sh
python3 scripts/validate.py
python3 -B -m unittest discover -s tests -v
python3 scripts/package.py
```

Version 0.3.0 adds discovery and reviewed catalog extensions. Thirty-three integration tests cover discovery, review, actual writes, repeat installation, preservation, dependencies, source failures, hostile paths, license checks, and rollback. An independent setup trial found, inspected, and installed a pinned Supabase skill alongside two project workflows, with three named specialist roles. See [library verification](docs/LIBRARY_VERIFICATION.md). Live host invocation remains separate from package validation.

The earlier philosopher pilots mostly tied a strong baseline and do not establish reliable overall improvement. New project workflows and upstream entries are not represented as proven performance upgrades. Read [evaluation evidence](evals/RESULTS.md), [installation verification](docs/INSTALLATION_VERIFICATION.md), and [the protocol](evals/README.md).

[Product direction](docs/ROADMAP.md) · [Release guide](docs/RELEASE.md) · [MIT license](LICENSE)
