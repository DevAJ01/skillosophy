# Skillsophy

Practical philosophical reasoning skills for AI agents. Use a philosopher's method to improve a piece of work: clarify a requirement, challenge a claim, design a fair rule, or make a decision under uncertainty.

These are **reasoning lenses, not personality impersonations**. They contain original contemporary workflows informed by philosophical texts, with sources and interpretation limits. They do not promise superior answers on every task. Version 0.1.0 is an exploratory release; see [evaluation](evals/README.md) for the evidence and its limits.

## Choose a lens

| Skill | Useful for | Result to expect |
|---|---|---|
| [Socrates](skills/philosopher-socrates/SKILL.md) | Vague definitions and hidden assumptions | Counterexample and better working claim |
| [Kant](skills/philosopher-kant/SKILL.md) | Duties, deception, and respect for agency | Consistent rule and honest alternative |
| [Nietzsche](skills/philosopher-nietzsche/SKILL.md) | Inherited values and status incentives | Competing explanations and a practical experiment |
| [Epictetus](skills/philosopher-epictetus/SKILL.md) | Setbacks and limited control | Responsible action with a contingency |
| [Popper](skills/philosopher-popper/SKILL.md) | Empirical and causal claims | Test that could change the decision |
| [Wittgenstein](skills/philosopher-wittgenstein/SKILL.md) | Ambiguous requirements and word disputes | Concrete uses and acceptance criteria |
| [Rawls](skills/philosopher-rawls/SKILL.md) | Institutional rules and opportunity | Alternatives assessed for fairness |
| [Mill](skills/philosopher-mill/SKILL.md) | Benefits, harms, and uncertainty | Stakeholder comparison and reversal condition |
| [Aristotle](skills/philosopher-aristotle/SKILL.md) | Habits and professional judgment | Practice aligned with a worthwhile purpose |
| [Descartes](skills/philosopher-descartes/SKILL.md) | Doubtful premises and tangled arguments | Assumption audit and rebuilt conclusion |
| [Selector](skills/philosopher-selector/SKILL.md) | Choosing a suitable method | One useful lens, with a reason for the fit |
| [Council](skills/philosopher-council/SKILL.md) | A decision with conflicting concerns | Explicit disagreement and actionable synthesis |

The Stoic lens is centered on Epictetus and the utilitarian lens on Mill. They do not represent every position within those traditions. This initial Western collection is a scoped starting point, not a universal philosophy canon.

## Use with your AI

A skill-aware client can load the matching folder under `skills/`. Preserve the folder's `references/` and `agents/` files. Install the selector and council together with the full collection, because they refer to sibling skills. The ten individual philosopher skills are self-contained.

For Codex, copy the skill folders you want into your configured skills directory (commonly `~/.codex/skills`) and start a new session. Invoke a skill explicitly:

```text
Use $philosopher-popper to examine this claim and design a test that could change our decision: [claim, evidence, constraints].
```

```text
Use $philosopher-selector to choose and apply a useful lens. My task is [deliverable]; the main uncertainty is [uncertainty].
```

```text
Use $philosopher-council to compare suitable perspectives on [decision]. Here are the facts, alternatives, and constraints: [...].
```

For a chat interface without skill loading, attach or paste the selected `SKILL.md` as instructions together with your task. Include its references only when historical detail matters. For the selector/council, also supply the catalog and selected skill text. Pasting a prompt does not install a plugin or grant new tools. Host instruction precedence still applies.

For ChatGPT or Codex plugin distribution, build the skills-only package with `python3 scripts/package.py`, then use the host's supported plugin import or account-save workflow. The plugin contains conversational selection; there is no graphical picker or third-party search in this release. See official [skill documentation](https://developers.openai.com/plugins/build/skills) and [plugin documentation](https://learn.chatgpt.com/docs/build-plugins) for current host support.

## Evaluate and contribute

```sh
python3 scripts/validate.py
python3 scripts/package.py
```

Structural validation checks packaging, links, metadata, and coverage. It does **not** test reasoning quality. Behavioral evaluation uses matched baseline/skill tasks, independently generated answers, and blinded judging; read [the protocol](evals/README.md) before making effectiveness claims.

Useful contributions include a real task where a skill changed the result, a historical correction with an edition or source, and a counterexample where the method caused a regression. Report the model, task, original answer, skill-assisted answer, and how success was assessed. Do not submit private data or copyrighted source reproductions.

[Roadmap and third-party catalog policy](docs/ROADMAP.md) · [Release guide](docs/RELEASE.md) · [MIT license](LICENSE)
