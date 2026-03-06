---
name: work-issue
description: Work autonomously on a Linear issue end-to-end
user-invocable: true
---

Work autonomously on the Linear issue: **$ARGUMENTS**

## Your process

**1. Load context**
- Fetch the issue from Linear MCP using the identifier provided (e.g. PRS-39)
- Read `PLAN.md` in the project root to understand the current plan and where this issue fits
- Read `CLAUDE.md` in the project root (and `~/.claude/CLAUDE.md` for global preferences) to understand conventions, architecture, and constraints
- Read any files or artifacts referenced in the issue description

**2. Understand the task**
- State back what the issue is asking for in 2-3 sentences
- Identify any blockers or missing information before proceeding
- If the task is ambiguous, ask one clarifying question — do not guess and proceed

**3. Mark as In Progress**
- Set the Linear issue status to "In Progress"

**4. Do the work**
- Work through all subtasks described in the issue
- Follow the conventions in CLAUDE.md — file structure, commit style, tooling preferences
- Commit incrementally with clear messages as you complete logical chunks
- If you discover a meaningful subtask not already in the issue, add it to PLAN.md

**5. Definition of done**
- All steps in the issue description are complete
- PLAN.md checkbox for this issue is checked off
- Any output artifacts are committed
- Linear issue status is set to "Done"
- Give a concise summary of what was completed and any follow-on items to be aware of

## Rules
- Do not mark Done until every step is genuinely complete
- Do not invent scope — work only what the issue describes
- If you hit a blocker you cannot resolve (missing credentials, external dependency, UI interaction required), stop, report the blocker clearly, and leave the issue In Progress
- Prefer editing existing files over creating new ones
- Do not push to remote unless the issue explicitly asks for it
