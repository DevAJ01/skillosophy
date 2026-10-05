# Release and publishing

The current product name is **Skillosophy**, and the repository is [DevAJ01/skillosophy](https://github.com/DevAJ01/skillosophy). The 0.1.x philosopher releases retain their original historical names and evidence. Version 0.2.0 changes the primary workflow to project startup, selection, role instructions, and project-local installation.

Before a release, run package validation and installer integration tests, inspect the actual behavioral artifacts, and build the ZIP with `python3 scripts/package.py`. Verify the uploaded release against the local package checksum. A private plugin save does not establish installation or live invocation success, and it does not submit a public listing.

The existing private account plugin has the immutable machine identifier `skillsophy`. Its update service rejects a renamed manifest. To update that same plugin without creating a duplicate, build `python3 scripts/package.py --account-name skillsophy` and upload the resulting account ZIP. Only the machine identifier and ZIP root differ; the visible name, default prompt, skills, and project records all use **Skillosophy**. The public source and portable release ZIP use `skillosophy`.

Publish standalone skill folders with their references and scripts. The startup workflow uses the complete bundled collection for its local-source selections. The six external catalog entries are source pointers; the installer fetches selected skills at pinned revisions and retains their licenses and notices.

For public OpenAI directory submission, follow the current [submission documentation](https://developers.openai.com/plugins/deploy/submission) and [plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines), including required icons, listing details, examples, support/contact information, and attestations. Public directory review has not been completed. For other skills directories, verify their current rules; a GitHub push does not automatically submit a listing.

## Hosted CI status

The initial GitHub Actions run did not start because GitHub reported that the owner's account is locked due to a billing issue. Local checks passed; this is an account blocker, not a verified hosted code check. Restore Actions access and rerun [the workflow](https://github.com/DevAJ01/skillosophy/actions/workflows/validate.yml).
