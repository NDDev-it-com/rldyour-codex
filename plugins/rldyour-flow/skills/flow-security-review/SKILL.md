---
name: flow-security-review
description: "Оркестрирует security review для explicit ry-start review/ry-review: auth, secrets, OWASP, injection, SSRF/XSS. EN: security review, OWASP, sensitive scope."
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
