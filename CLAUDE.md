# Claude Code Instructions

Start with **[`AGENTS.md`](./AGENTS.md)** — it holds the vendor-neutral agent instructions, journal index, and skill index. Everything here applies to Claude Code as well.

## Claude-specific note: skill shims

Claude Code auto-discovers skills at `.claude/skills/<name>/SKILL.md`. Those files are thin shims (YAML frontmatter + one-line delegate) that point at the vendor-neutral source of truth in [`skills/`](./skills/).

**When editing a skill, update `skills/<name>.md` — not the shim.** The shim only carries the frontmatter Claude's loader needs to know when to trigger.
