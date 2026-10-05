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

## Initial catalog

The catalog has **22 installable entries**, while the plugin packages 17 workflows including its startup entry.

| Collection | Included capabilities |
|---|---|
| Original project workflows | [Project brief](skills/skillosophy-project-brief/SKILL.md), [evidence plan](skills/skillosophy-evidence-plan/SKILL.md), [delivery plan](skills/skillosophy-delivery-plan/SKILL.md), [acceptance review](skills/skillosophy-acceptance-review/SKILL.md) |
| Pinned upstream skills | Playwright browser work, PDF work, GitHub CI repair, security best practices, Jupyter notebooks, Vercel deployment |
| Reasoning lenses | Socrates, Kant, Nietzsche, Epictetus, Popper, Wittgenstein, Rawls, Mill, Aristotle, Descartes |
| Reasoning selection | [Philosopher selector](skills/philosopher-selector/SKILL.md) and [council](skills/philosopher-council/SKILL.md) |

Upstream entries point to checked, immutable revisions of [openai/skills](https://github.com/openai/skills), with per-skill licenses and prerequisites. They are fetched only when selected for installation. Provenance and popularity do not establish measured effectiveness. The [catalog](skills/skillosophy-start/references/catalog.json) records that distinction.

Coverage is intentionally finite. For a missing specialty, Skillosophy can inspect a suitable licensed source or use the host's skill-creator workflow to author a focused project skill. The bundled installer accepts reviewed catalog entries; it does not install arbitrary unreviewed URLs.

## Development and verification

```sh
python3 scripts/validate.py
python3 -B -m unittest discover -s tests -v
python3 scripts/package.py
```

Version 0.2.0 adds project setup and installation. Integration tests cover actual writes, repeat installation, preservation, dependencies, source failures, hostile paths, license checks, and rollback. A real pinned upstream skill installation is also checked in a temporary project. Live host invocation remains separate from package validation.

The earlier philosopher pilots mostly tied a strong baseline and do not establish reliable overall improvement. New project workflows and upstream entries are not represented as proven performance upgrades. Read [evaluation evidence](evals/RESULTS.md), [installation verification](docs/INSTALLATION_VERIFICATION.md), and [the protocol](evals/README.md).

[Product direction](docs/ROADMAP.md) · [Release guide](docs/RELEASE.md) · [MIT license](LICENSE)
