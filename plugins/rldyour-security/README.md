# rldyour-security

`rldyour-security` is a skills-only security plugin for Codex.

It does not configure MCP servers, does not add hooks, and does not block normal implementation work. It adds security guidance and review workflows that help the agent produce comments, findings, and remediation recommendations. The agent decides how to apply those comments within the current task unless normal Codex safety rules require refusal or confirmation for explicit destructive or malicious actions.

User-facing conversation stays in Russian unless the owner asks otherwise. Repository documentation is written in English.

## Auto Invocation

The plugin is optimized for automatic security skill selection. Codex should route security work to these skills when a task mentions security, secure coding, OWASP, ASVS, vulnerability review, audit, auth/authz, permissions, secrets, injection, crypto, dependency risk, security headers, logging, error handling, or `$ry-sec-review`.

`policy.allow_implicit_invocation` is enabled for every skill. The primary trigger surface is each `SKILL.md` frontmatter `description`; plugin manifest descriptions and `agents/openai.yaml` metadata mirror the same intent for marketplace and UI discovery.

## Scope

- Keep implementation work aligned with OWASP Top 10 2025.
- Use ASVS 5.0.0 and OWASP secure coding checklist principles as deeper verification references.
- Provide non-blocking security comments during implementation.
- Provide `$ry-sec-review` for defensive, evidence-based security review of a full implementation or diff.
- Avoid exploit weaponization, credential exposure, destructive command guidance, and unsafe proof-of-concept generation.

## Skills

- `owasp-top-10-implementation`: non-blocking secure implementation guidance mapped to OWASP Top 10 2025.
- `ry-sec-review`: defensive security review workflow with hypothesis generation, data-flow tracing, confidence ranking, concrete remediation, and verification.

## Trigger Map

- Security-relevant implementation work, secure coding comments, OWASP alignment, auth/authz, inputs/outputs, files, secrets, crypto, dependencies, logging, errors, or external integrations: use `owasp-top-10-implementation`.
- Explicit security review, vulnerability audit, `$ry-sec-review`, PR/diff audit, sensitive code path review, source-to-sink tracing, exploitability assessment, or remediation report: use `ry-sec-review`.

## Safety Boundary

This plugin should not stop ordinary work. It should surface security comments and recommend fixes.

Hard safety boundaries remain for explicit destructive or harmful requests, such as deleting protected paths, credential exfiltration, malware behavior, persistence, stealth, or exploit weaponization. In those cases, follow Codex safety and approval rules rather than treating the plugin as an override.

## Sources

- OWASP Top 10 2025: https://owasp.org/Top10/2025/
- OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/
- OWASP Secure Coding Practices Checklist: https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/stable-en/02-checklist/05-checklist
- OWASP Code Review Guide: https://owasp.org/www-project-code-review-guide/
- OWASP Web Security Testing Guide: https://owasp.org/www-project-web-security-testing-guide/
- Mythos Agent public description: https://www.mythos-agent.com/
