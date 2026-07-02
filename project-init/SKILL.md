---
name: project-init
description: Use when the user wants to create a _PROJECT.md file for the current repository. Triggers on "project init", "init project", "create PROJECT.md", "set up project file", "write project context".
disable-model-invocation: true
---

# `/project-init` Skill

Interactively create a `_PROJECT.md` file for the current repo. Gathers context from existing repo files and Linear before asking questions, so you confirm or correct rather than type from scratch.

---

## Before starting

Check for an existing `_PROJECT.md` in the repo root. If one exists, stop immediately and tell the user:

> "_PROJECT.md already exists in this repo. This skill only creates new files — edit it directly or delete it to start fresh."

Do not proceed.

---

## Step 1 — Gather context silently

Before asking anything, read all of the following that exist. Do not show this work to the user — just build your internal picture of the project.

- `CLAUDE.md` in repo root — project purpose, architecture, key files
- `_PLAN.md` — tasks, phases, current focus
- `_LINEAR_TODO.md` — backlog items
- `POST_SIGN_EXTRACTION_BRIEF.md` or any `*BRIEF*` / `*SPEC*` / `*README*` files in root
- Recent git log: `git log --oneline -20`
- List Linear projects: call `list_projects` — find the best match for this repo by name similarity

From this, prepare a **draft proposal** for each section. Some sections will have confident proposals (e.g. goal from CLAUDE.md); others will be empty or uncertain.

---

## Step 2 — Meta section

Present the proposed `linear_project` name (from the best Linear match) and `staleness_days` (default: 7).

Ask:
> **Section 1 of 7 — Meta**
>
> Here's what I found for the project metadata:
> - `linear_project`: [proposed name] ← from Linear ([ID])
> - `staleness_days`: 7 (default — increase for slower-moving projects, e.g. 30 or 90)
>
> Correct the project name if wrong, or change staleness_days if needed. Otherwise just say "ok".

Wait for confirmation or corrections before continuing.

---

## Step 3 — Goal section

Present a draft goal drawn from CLAUDE.md or README context. Keep it to 2-3 sentences: what the project proves or builds, for whom, using what.

Ask:
> **Section 2 of 7 — Goal**
>
> Draft:
> "[proposed goal]"
>
> Edit this or say "ok".

Wait for response.

---

## Step 4 — Current milestone

This is rarely inferrable — don't guess unless PLAN.md has an explicit milestone heading. Ask:

> **Section 3 of 7 — Current milestone**
>
> What's the current milestone called, and what's its scope?
> - **Name:** (e.g. "PoC → Product input → Scope decision")
> - **In scope:** What work is included in this milestone? (bullet points)
> - **Done when:** What specific condition marks this milestone complete?

If PLAN.md has a clear milestone block, propose it. Otherwise ask open.

Wait for response.

---

## Step 5 — Success metrics

Propose 2-4 metrics derived from the milestone done-when criteria and goal. Frame as specific, observable outcomes — not tasks.

Ask:
> **Section 4 of 7 — Success metrics**
>
> Draft metrics:
> - [metric 1]
> - [metric 2]
> - [metric 3]
>
> Add, remove, or reword. Say "ok" to keep as-is.

Wait for response.

---

## Step 6 — Stakeholders

Ask:
> **Section 5 of 7 — Stakeholders**
>
> Who needs to know about or act on this project? For each person, I need:
> - Name + role/title
> - One line on their stake (what they need from this project)
>
> List them, or say "none" if this is internal-only.

If CLAUDE.md or any brief mentions names, propose them first.

Wait for response.

---

## Step 7 — Feature shape (phases)

This is the checklist that `review-issues` uses for gap detection. Each phase maps to a Linear issue.

If PLAN.md or CLAUDE.md has a clear phase structure, propose it. Otherwise ask:

> **Section 6 of 7 — Feature shape**
>
> List the phases of this project in order. Each phase should be a discrete unit of work that maps to a Linear issue.
>
> [If proposing:] Draft phases from your plan:
> 1. [phase 1 name]
> 2. [phase 2 name]
> 3. [phase 3 name]
>
> Add, reorder, or rename. Say "ok" to keep as-is.

Wait for response.

---

## Step 8 — Open questions + Not doing

Combine these into one ask to keep it efficient:

> **Section 7 of 7 — Open questions and scope boundaries**
>
> **Open questions:** What decisions are still unresolved that could change the direction or scope?
> (Leave blank if none)
>
> **Not doing this milestone:** What's explicitly out of scope right now?
> (Parking lot items, future phases, things that came up but were deferred)
>
> **Decisions made:** Any key decisions already locked that reviewers should know?
> (e.g. tech choice, build-vs-buy, key constraint accepted)

Wait for response.

---

## Step 9 — Preview and confirm

Compose the full `_PROJECT.md` content using all confirmed answers. Show it in a fenced markdown block.

Then ask:
> Here's the full _PROJECT.md. Want me to write it to the repo root, or make any changes first?

Wait for explicit confirmation before writing.

---

## Step 10 — Write the file

Write `_PROJECT.md` to the repo root using the confirmed content.

---

## Step 11 — Scaffold context structure

After writing `_PROJECT.md`, create the following folder structure using `.gitkeep` files:

```
_context/
├── reference/     # PDFs, research, data files, brand assets brought in from outside
├── transcripts/   # Meeting/call recordings and their text versions
└── samples/       # Example documents, templates, sample data
_prompts/           # AI/LLM instructions and workflows
```

Create each folder by writing a `.gitkeep` file into it:
- `_context/reference/.gitkeep`
- `_context/transcripts/.gitkeep`
- `_context/samples/.gitkeep`
- `_prompts/.gitkeep`

If any of these folders already exist, skip them silently.

---

## Step 11b — Ensure `_context/` is gitignored

`_context/` holds working inputs (reference, transcripts, samples) and generated artifacts — it must **never** be committed. Always make sure the repo-root `.gitignore` excludes it:

- If `.gitignore` is missing, create it. If it exists but lacks `_context/`, append it.
- Baseline entries:
  ```
  # Working context — never committed
  _context/

  # OS / editor cruft
  .DS_Store
  **/.DS_Store
  ~$*
  ```
- If `_context/` was already committed, untrack it: `git rm -r --cached _context` (files stay on disk, out of the repo).
- Verify with `git check-ignore _context` (should print `_context`).

(The `_context/.gitkeep` files from Step 11 only scaffold the local folders; once `_context/` is ignored they aren't tracked — that's intended. `_prompts/` and `_docs/` remain tracked.)

---

## Step 12 — Scaffold docs structure

Also create the following docs folder structure using `.gitkeep` files:

```
_docs/
├── architecture/   # What's built — system diagrams, component overviews, data models
├── specs/          # Feature specs, design briefs, scope documents
├── setup/          # How to install, configure, run — builder-facing
└── guides/         # End-user how-tos and walkthroughs
```

Create each folder by writing a `.gitkeep` file into it:
- `_docs/architecture/.gitkeep`
- `_docs/specs/.gitkeep`
- `_docs/setup/.gitkeep`
- `_docs/guides/.gitkeep`

If any of these folders already exist, skip them silently.

Confirm:
> ✅ _PROJECT.md written and project structure scaffolded. Run `/review-issues` to check how the issues align with it.

---

## Output format

The file must follow this exact structure:

```markdown
# [Repo/project title] — PROJECT.md

## Meta
linear_project: [name]
staleness_days: [N]

## Goal
[2-3 sentences]

## Current milestone
**[Milestone name]** — [date or "no hard date yet"]
- In scope: [bullet list]
- Done when: [specific condition]

## Success metrics
- [metric]
- [metric]

## Stakeholders
- [Name] ([Role]) — [their stake]

## Feature shape (per phase)
A complete phase requires:
- [ ] A Linear issue exists for this phase
- [ ] Inputs and outputs are defined in the issue description
- [ ] Blocker relationship to the next phase is set in Linear
- [ ] Acceptance criteria are specific and verifiable

Current phases (in order):
1. [Phase 1]
2. [Phase 2]
3. [Phase 3]

## Current focus
[One sentence on what's actively being worked on]

## Open questions
- [question]

## Decisions made
- **[Decision name]** — [rationale]

## Not doing (this milestone)
- [item]
```

Omit `## Decisions made` entirely if the user provided none. Omit `## Open questions` if none. Do not add placeholder text for empty sections — omit them.

---

## Key rules

- Never write the file without explicit user confirmation in Step 9.
- Don't invent stakeholder names — only propose names found in repo files.
- Keep proposals short and editable — the user should be correcting, not reading.
- If a section has nothing to propose, ask open rather than guessing.
- The feature shape phases must map 1:1 to expected Linear issues — don't list sub-tasks as phases.
