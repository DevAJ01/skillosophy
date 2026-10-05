# Release and publishing

1. Run structural validation and build the ZIP. Review the actual behavioral report and unresolved regressions.
2. Check each skill's description, examples, and historical pointers. Do not advertise “proven improvement” on the strength of the initial pilot.
3. Publish the source repository and provide standalone `skills/<name>/SKILL.md` folders. When listing on a skills directory, follow its current submission rules and confirm it indexes nested `skills/` directories. Do not assume a GitHub push automatically publishes a directory listing.
4. For ChatGPT/Codex, use the skills-only `plugin.json` package. Saving to a private account/workspace does not submit a public listing or establish installation success.
5. Before public OpenAI directory submission, prepare the required icon, listing metadata, examples, support/contact details, and any requested attestations in the current submission portal. Use official [submission documentation](https://developers.openai.com/plugins/deploy/submission) and [plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines). Review portal requirements at release time; this repository is not a claim that public review has passed.
6. Record the exact package checksum, Git revision, plugin release ID if saved, and evaluation configuration. Tag the release only after review. Keep raw evaluation evidence so users can examine the basis of claims.

This initial package has no MCP server, third-party app bindings, external dependencies, graphical picker, or claimed directory approval. It contains the implemented philosopher workflows and conversational routing.
