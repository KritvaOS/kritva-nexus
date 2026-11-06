# Kritva Nexus Security Policy

**Repository:** `kritva-nexus`
**Security Owner:** Dinesh (program decision D-032 in kritva-program)

## 1. Scope

Reproducible security vulnerabilities in this repository's tooling, documentation and CI configuration. At present the repository holds planning documents and common repository checks (Python, standard library only); it holds no RTL, simulator, FPGA or physical-design code yet. When such content is added, this scope is updated in the same change. Security properties of the Nexus SoC design (secure domain, secure boot, key handling) are design requirements tracked in the architecture and requirements documents, not claims made by this policy.

## 2. Do not disclose unfixed vulnerabilities publicly

Please do not put details of an unpatched vulnerability in a public issue, pull request, discussion or post.

## 3. Reporting

Reporting route: UNVERIFIED for this repository. GitHub private vulnerability reporting (Security tab, "Report a vulnerability") is the intended first route once the owner has enabled and tested it for `kritva-nexus`; this has not been verified from this repository. Until then, contact the Security Owner (Dinesh) directly through your existing Kritva channel, say only that you have a security report, and ask for a private place to share the details; do not put details in the first message.

Include the affected file or commit, a description, steps to reproduce, observed and expected behaviour, the potential impact and any mitigation you know of. Leave out personal, customer, credential or production data.

## 4. What to expect

The Security Owner will make reasonable efforts to acknowledge a valid report, assess it, coordinate a fix and agree disclosure timing. This policy sets no guaranteed deadlines.

## 5. Secrets

Never commit credentials, tokens, private keys or production data. If one is committed by mistake, tell the Security Owner at once so it can be revoked or rotated.
