# Source-Backed Design Notes

Primary sources used for this plugin:

- OpenAI Codex AGENTS.md: https://developers.openai.com/codex/guides/agents-md
- OpenAI Codex Skills: https://developers.openai.com/codex/skills
- OpenAI Codex Hooks: https://developers.openai.com/codex/hooks
- OpenAI Codex Subagents: https://developers.openai.com/codex/subagents
- Feature-Sliced Design: https://fsd.how/
- Feature-Sliced Design layers: https://fsd.how/docs/reference/layers/
- Feature-Sliced Design public API: https://fsd.how/docs/reference/public-api/
- Vertical Slice Architecture: https://www.jimmybogard.com/vertical-slice-architecture/
- Google Engineering Practices, what to look for in code review: https://google.github.io/eng-practices/review/reviewer/looking-for.html
- Google Engineering Practices, small CLs: https://google.github.io/eng-practices/review/developer/small-cls.html
- Martin Fowler Design Stamina Hypothesis: https://martinfowler.com/bliki/DesignStaminaHypothesis.html
- Architectural Decision Records: https://adr.github.io/
- Semantic Versioning: https://semver.org/
- Conventional Commits: https://www.conventionalcommits.org/en/v1.0.0/
- OWASP Secure Coding Practices: https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/

Engineering conclusions:

- Keep rules as focused skills with references for progressive disclosure.
- Use `AGENTS.md` for durable project instructions, but keep it compact because Codex loads it before work.
- Use FSD and VSA as defaults for new areas, not as forced rewrites of coherent existing projects.
- Prefer advisory-first automatic guidance over blocking hooks for general quality rules.
- Keep hard bans explicit and non-negotiable inside touched scope.
- Use ADRs for decisions future agents must preserve.
