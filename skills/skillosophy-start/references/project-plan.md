# Project plan and installation

Use a JSON plan with schema_version 1. Text is user/project context, not executable code. Keep roles small and tie each to selected catalog IDs.

```json
{
  "schema_version": 1,
  "project": {
    "goal": "Build an offline CSV cleaning utility",
    "deliverable": "A CLI that produces a cleaned copy and an audit report",
    "philosophy": {
      "priority": "Preserve original data over silent convenience",
      "approach": "Deliver a reversible end-to-end slice first",
      "evidence": "Representative malformed-input checks and row-count reconciliation",
      "tradeoffs": "Reject ambiguous transformations rather than guessing"
    }
  },
  "skills": ["skillosophy-project-brief", "skillosophy-acceptance-review"],
  "roles": [
    {
      "name": "reviewer",
      "mission": "Check that cleaning preserves source data and explains rejected rows",
      "skills": ["skillosophy-acceptance-review"],
      "done_when": "The requested behavior and important malformed-input cases have recorded evidence"
    }
  ]
}
```

From the installed plugin's skill directory, resolve scripts/project_skills.py and run:

```sh
python3 /absolute/path/to/skillosophy-start/scripts/project_skills.py catalog
python3 /absolute/path/to/skillosophy-start/scripts/project_skills.py install --project /absolute/path/to/project --plan /absolute/path/to/plan.json
python3 /absolute/path/to/skillosophy-start/scripts/project_skills.py install --project /absolute/path/to/project --plan /absolute/path/to/plan.json --apply
```

The first install command is a dry run and writes nothing. The second installs the planned skills and their catalog dependencies. Bundled sources resolve beside this skill in the plugin; use --bundle-root only for an explicit alternative bundle containing the same reviewed skills. External sources require network access and are fetched from their pinned GitHub revision. No downloaded code is executed.

The installer refuses changed destination skills and symlinked managed paths. An identical installation is a no-op. Plans, source/hash receipts, and named role Markdown are stored under .skillosophy/setup-<plan-hash>/; this is an immutable setup record, not a Codex configuration file or running agent. Existing AGENTS.md and project settings are preserved. Never report role documents as registered subagents.

The human plan summary should emphasize capabilities and the next action; users do not need internal catalog keys or receipt fields to understand the project approach.
