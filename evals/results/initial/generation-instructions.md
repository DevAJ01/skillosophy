# Generator and judge setup

Each generator started in a fresh subagent context without the project conversation. Both inherited the session model and were given the same case prompts. The complete prompts are in `cases.json`. The metadata records what is known about execution; sampling settings were not exposed independently.

## Baseline generator

Read only a task JSON file containing ID, designated skill name, and prompt. Answer all tasks as a competent helpful AI without loading a skill or adding a philosopher workflow beyond what the user prompt explicitly asks. Treat cases independently, follow word limits, do not browse or take external actions, and write actual final answers. Do not inspect rubrics, project documents, skill content, or another agent's output.

## Skill-assisted generator

Read the same task JSON file. For each case, load its designated `SKILL.md` and references or sibling skills actually required by the workflow. Treat cases independently, follow word limits, do not browse or take external actions, and write actual final answers with a list of loaded skills. Do not inspect rubrics, project documents, or another agent's output.

## Judge

Read only the blinded packet, which includes case prompts, task criteria, and randomized answers A/B. Do not read the key, skill files, project documents, or labeled answer files. Score actual output quality rather than vocabulary, length, or apparent prompting style. Assess correctness, evidence handling, practical usefulness, instruction compliance, and relevant insight, 0–2 each. Criteria identify outcomes to inspect, not mandatory names or phrases. Record reasons and material failures, then express A/B/tie preference. Save scores before unblinding.

The prompts are summarized here for reproducibility; no private deliberation is recorded. The actual answers and full scoring records are published. Independence means distinct model instances without access to the opposing answers, not different model families or independent human reviewers.
