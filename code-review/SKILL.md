---
name: code-review
description: >
  Pre-deploy sanity check for AI-generated code. Catches the specific failure modes AI
  tends to produce: debug artifacts, hardcoded values, unresolved placeholders, dead
  scaffolding, over-engineering, hallucinated APIs, missing error handling, and security
  basics. Use when the user asks to review, check, or audit code before shipping — or
  says anything like "is this ready?", "check this before I push", "review what Claude wrote".
  Not a general code quality audit — focused specifically on AI code failure modes.
---

# AI Code Pre-Flight Check

A fast, targeted review for AI-generated code before it ships.

---

## Step 1: Orient

Check what's new:

```bash
git diff --name-only HEAD~1 2>/dev/null || git status --short
```

If the user pointed at specific files, skip this — just review those files directly.

Check for CLAUDE.md. If present, read it for project-specific conventions that affect what counts as a problem.

---

## Step 2: Run the checklist

Read each changed or specified file. Flag anything matching the categories below.

Use `Read` and `Grep` tools — not bash grep.

### 🔴 Ship blockers

Things that will embarrass you or break production:

- **Hardcoded secrets** — API keys, tokens, passwords, anything that should be in env vars
  - Grep: `password|secret|api_key|apikey|bearer|token\s*=\s*['"]`
- **Debug artifacts** — left-in logging and breakpoints
  - Grep: `console\.log|print\(|debugger|pdb\.set_trace|binding\.pry|dd\(|var_dump`
- **Placeholder content** — fake data, lorem ipsum, test values in non-test code
  - Grep: `TODO|FIXME|HACK|lorem|placeholder|example\.com|foo@bar|test@test`
- **Hallucinated APIs** — method calls or imports that don't exist in your actual stack. Read the file and check: does every imported module exist? Does every called method actually exist on that object?
- **Missing error handling on critical paths** — unhandled promise rejections, bare `except: pass`, DB calls with no error handling, API calls that assume 200

### 🟡 Fix soon

Things that won't break immediately but will cause pain:

- **Dead scaffolding** — unused imports, variables declared but never read, functions generated but never called
- **Over-engineering** — AI loves to add abstraction layers, config systems, factory patterns, and base classes for things that only get used once. Flag anything that looks like it was designed for hypothetical future requirements.
- **Magic values** — hardcoded strings, numbers, or URLs that should be named constants or config
- **Inconsistent conventions** — naming style or patterns that don't match the surrounding codebase (AI writes to its training data defaults, not your conventions)

---

## Step 3: Output

No tables, no report, no executive summary. Just this:

```
## Pre-flight: [filename or "changed files"]

🔴 Fix before shipping:
- [file:line] — what it is and why it matters (one line)

🟡 Fix soon:
- [file:line] — what it is (one line)

✅ Looks clean / nothing flagged
```

If there's nothing in a category, omit it. Keep each line tight — you know your codebase.

---

## Step 4: Offer to fix

After the output, ask:

> "Want me to fix the 🔴 items now?"

Only offer to fix the ship blockers. Don't auto-apply anything — show the diff and confirm first.
