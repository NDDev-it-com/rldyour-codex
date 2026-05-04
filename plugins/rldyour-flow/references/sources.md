# Source-Backed Design Notes

Primary sources used for this workflow:

- OpenAI Codex AGENTS.md: https://developers.openai.com/codex/guides/agents-md
- OpenAI Codex Skills: https://developers.openai.com/codex/skills
- OpenAI Codex Hooks: https://developers.openai.com/codex/hooks
- OpenAI Codex best practices: https://developers.openai.com/codex/learn/best-practices
- OpenAI Codex Subagents: https://developers.openai.com/codex/subagents
- Git ignore rules: https://git-scm.com/docs/gitignore
- Git push force-with-lease: https://git-scm.com/docs/git-push
- GitHub protected branches: https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- GitHub Flow: https://docs.github.com/en/get-started/using-github/github-flow
- GitHub pull request reviews: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews
- Conventional Commits: https://www.conventionalcommits.org/en/v1.0.0/
- Google code review, what to look for: https://google.github.io/eng-practices/review/reviewer/looking-for.html
- Google code review, small CLs: https://google.github.io/eng-practices/review/developer/small-cls.html
- Google SRE release engineering: https://sre.google/sre-book/release-engineering/
- C4 model: https://c4model.com/
- arc42: https://arc42.org/overview
- Architecture decision records: https://adr.github.io/
- OWASP secure coding and review concepts: https://owasp.org/

Engineering conclusions:

- Skills should stay focused and use references/scripts for progressive disclosure.
- Hooks should be deterministic and non-destructive; they should ask Codex to continue rather than silently mutating code.
- Multiple Stop hooks run independently, so post-task sync must coordinate with Serena using state checks and loop markers.
- Subagents are useful for parallel reviews, but prompts must be self-contained and bounded.
- `AGENTS.md` is Codex-native; `CLAUDE.md` is compatibility documentation and should not be treated as the primary Codex source when both exist.
- `.git/info/exclude` is local exclude state, so it is appropriate for per-repository agent-only files that should exist locally but not in normal branch history.
- Use `--force-with-lease` for generated `fullrepo` snapshots so unexpected remote updates are not overwritten silently.
