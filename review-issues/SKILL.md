---
name: review-issues
description: Use when the user asks to review open Linear issues for a project or milestone, do backlog grooming, plan a sprint, or get a health check on a project's Linear backlog. Triggers on "review issues", "groom backlog", "what should I work on", "sprint planning", "milestone review".
disable-model-invocation: true
---

# `/review-issues` Skill

Review open Linear issues for a project or milestone. Surfaces prioritization reasoning, phase gaps, stale issues, and suggests specific actions. Optionally applies changes in Linear with explicit per-action confirmation.

---

## Argument handling

Parse the user's invocation:

- **No args** → look for `PROJECT.md` in the current repo root; read `linear_project` field to resolve the project. If no `PROJECT.md` in repo root, check `~/.claude/projects/`. If still missing, ask the user to specify a project name.
- **`[project name]`** → use that project's open issues directly (skip PROJECT.md lookup).
- **`[project name] milestone:[name]`** → filter to issues matching that milestone; use case-insensitive partial match on milestone name.

---

## Step 1 — Load project context

1. Find PROJECT.md: repo root first, then `~/.claude/projects/[slug]/PROJECT.md`.
2. If found, extract:
   - `linear_project` (from `## Meta` section)
   - `staleness_days` (from `## Meta`; default 7 if absent)
   - Goal, current milestone, stakeholders, feature shape checklist, current focus, open questions, not-doing list
3. Note the file's last modification date. If it's older than `staleness_days`, flag it in the output.
4. If no PROJECT.md found: proceed with a **reduced review** (no phase gap detection). Note this limitation explicitly in the output header.

---

## Step 2 — Resolve project and confirm ID

1. Call `list_projects` to find the project by name (case-insensitive partial match).
2. Display the resolved project name and ID before fetching any issues — this is the write guardrail.
3. If multiple projects match, list them and ask the user to confirm which one.

---

## Step 3 — Fetch issues

1. Call `list_issues` filtered to: open state, resolved project, limit 250.
2. If a milestone filter was specified, apply it now (filter the returned list by milestone name, case-insensitive partial match).
3. For any issue that appears to be a phase-level issue (title contains "phase", "stage", or matches phase names from PROJECT.md), call `get_issue` with `includeRelations: true` to retrieve blocker/blocking relationships.
4. For other issues with sparse descriptions, call `get_issue` selectively to get full details before analysis.

---

## Step 4 — Analyze and output

Produce this report structure:

```
## Issue Review: [Project Name] — [today's date]
[N] open issues · staleness threshold: [N] days
⚠️ PROJECT.md last modified [X days ago] — may be stale   ← only if applicable
⚠️ No PROJECT.md found — gap detection skipped            ← only if no PROJECT.md

### Open questions (from PROJECT.md)
List each open question from the ## Open questions section.
Flag any that appear directly related to a blocked or stale issue.

### Milestone health
Assess whether the right issues exist for the current milestone.
Are they correctly sequenced? Is there anything missing that the
milestone goal clearly requires?

### Phase gap detection
(Skip this section entirely if no PROJECT.md was found.)

Against the ## Feature shape checklist from PROJECT.md, evaluate each phase:
✅ Phase 1 — issue exists, inputs/outputs defined, blocker to Phase 2 set, criteria present
⚠️ Phase 2 — issue exists but blocker relationship to Phase 1 not set in Linear
❌ Phase 3 — no Linear issue found

Use "appears to be missing" not "is missing" — acknowledge uncertainty.

### Priority assessment
Explicit reasoning for each priority call. Not just "P0" — explain why.
Example: "Phase 1 is P0 because Phases 2 and 3 are both blocked on it."

### Issues needing attention
List issues that are:
- Stale: no update in >[staleness_days] days
- Missing description or acceptance criteria
- Unassigned
- Have no blocker relationships when they should

### Suggested actions
Number each action. Be specific — include issue titles and what to change.
Example:
1. Set "Phase 2: Configure custom extractions" blocked by "Phase 1: Audit standard extractions" — blocker relation appears missing
2. Create issue for Phase 3 (Navigator API integration) — not found in Linear
3. Add acceptance criteria to "[issue title]" — description is present but no verifiable criteria
```

---

## Step 5 — Offer to apply

After the report, ask:

> "Want me to apply any of these in Linear? List the numbers you'd like applied, or say 'none'."

Wait for user response. Then:

1. Re-verify the project ID (re-read from memory, do not assume it's unchanged).
2. For each confirmed action, explain exactly what you're about to do before calling any write tool.
3. Apply only the confirmed actions via `save_issue` (or appropriate tool).
4. After each action, report what changed: "✅ Set blocker: Phase 2 now blocked by Phase 1."
5. For declined actions, acknowledge: "Skipped: [action description]."

---

## Key rules

- **Always show reasoning** — not just labels, but why.
- **Never apply changes without explicit per-action confirmation.**
- **Frame uncertainty honestly** — "appears to be missing" not "is missing."
- **Guard all writes** — resolve and display project ID at the start; re-verify before any `save_issue` call.
- **Reduced mode** — if no PROJECT.md, skip gap detection and note the limitation at the top of the report. The rest of the review (staleness, priority, missing descriptions) still runs.
