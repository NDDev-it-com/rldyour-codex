---
name: flow-security-review
description: "Security reviewer workflow for ry-start and ry-review. Use automatically for security-sensitive changes such as auth, authorization, API boundaries, file upload, secrets, dependency/config changes, payments, admin flows, SSRF/XSS/injection risk, or when the user asks for security review. Russian triggers: проверь безопасность, секьюрити ревью, авторизация, права доступа, секреты, OWASP."
---

# Flow Security Review

Use this review for security-sensitive changes and explicit security requests. Coordinate with `rldyour-security` and `ry-sec-review` when deeper source-to-sink security review is needed.

Review:

- Authentication and authorization boundaries.
- Input validation and output encoding.
- Injection, XSS, SSRF, path traversal, insecure deserialization.
- Secrets handling and logs.
- Dependency/config changes.
- Unsafe deployment or rollback operations.

Do not generate weaponized exploit instructions. Report defensive findings with severity, confidence, evidence, impact, and remediation.
