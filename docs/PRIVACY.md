# Skillosophy privacy policy

Effective date: 6 October 2026. Publisher: Ashan Jeevanathan. [Support and privacy questions](https://github.com/DevAJ01/skillosophy/blob/main/docs/SUPPORT.md).

## Project context and local records

Skillosophy provides instructions and a local installer for selecting project skills and defining specialist roles. The AI host may read project context to perform the requested task. Your ChatGPT/Codex environment and any tools you use process that context according to their own settings and policies.

The installer writes selected skill files into your project's `.agents/skills` directory. It stores a project plan, role instructions, source information, and file hashes in `.skillosophy/setup-<hash>`. Plans may contain the project information you supply, and receipts include the absolute project path. These files remain in the chosen project until you change or remove them. If you synchronize or share the project, its files may also be shared through that system.

The Skillosophy installer does not upload project files or plans to a publisher server. The current plugin includes no publisher-operated analytics endpoint, automatic telemetry, hosted application backend, or separate user account system. Automatic data collection for improving Skillosophy has not been implemented.

## External services

Skill discovery can query the skills.sh community directory using task keywords, and can resolve public GitHub repository commits and download skill sources. Those services receive the query or repository identifiers and ordinary network connection information. Use generic public keywords; do not send private project names, confidential requirements, code, or secrets as search terms. The bundled library supports offline search without network requests. Skillosophy does not run the community Skills CLI or its telemetry system.

When you select a cataloged upstream skill, the installer downloads its source archive at a pinned GitHub revision. GitHub receives ordinary network connection information associated with that request. Project plans and files are not sent in the archive request. Downloaded helpers are not executed during installation.

An installed skill may later use external tools or services for a task you request. Copying the skill does not connect those services. Review the instructions and the applicable service's data practices before using them.

OpenAI governs its host services under its [privacy policy](https://openai.com/policies/privacy-policy/). GitHub governs downloads, accounts, and issues under its [privacy statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement).

## Voluntary feedback and deletion

You can voluntarily report problems or suggestions through [GitHub Issues](https://github.com/DevAJ01/skillosophy/issues). That information is public and may be used by the maintainer to improve the plugin. Do not post secrets or confidential project information. GitHub controls the issue platform, its retention, and its account or content-deletion mechanisms.

Local Skillosophy records are under your control. You can remove local setup records and installed skill folders when you no longer need them. That does not remove copies held by a synchronization service, AI host, public issue tracker, or backups; use those services' controls for those copies.

Future analytics would require a defined data-handling design and an updated policy before being introduced. This policy describes the current distributed implementation.
