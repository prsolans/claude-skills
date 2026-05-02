---
name: daily-plan
description: Use when the user wants to start their day, get a morning briefing, plan their work session, reprioritize mid-day, capture a task or note, or wrap up the day. Triggers on phrases like "start my day", "daily plan", "what should I work on", "morning briefing", "reprioritize", "capture this", "end of day", "wrap up", "/daily", "/eod".
disable-model-invocation: true
---

# daily-plan Skill

A personal operating layer that sits above Linear. Synthesizes your Linear issues, Google Calendar, and a local `TODAY.md` scratch file into a daily plan. Supports morning kickoff, mid-session reprioritization, task capture, and end-of-day handoff.

---

## Argument Handling

`$ARGUMENTS` can be:
- Empty or `morning` / `start` → run full morning briefing
- `reprioritize` or `replan` → re-run prioritization against current state mid-day
- `capture [text]` → append a task or note to TODAY.md
- `eod` or `wrap` or `end` → run end-of-day summary and write tomorrow's carryover

---

## File Convention: `TODAY.md`

Located at `~/TODAY.md`. This is your personal scratch layer — things that don't belong in Linear (quick personal tasks, ad-hoc notes, things to remember today).

### Structure

```markdown
# TODAY — [DATE]

## Focus
[One sentence: what does a good day look like today?]

## Personal Tasks
- [ ] Task one
- [ ] Task two

## Captures
- [timestamp] Note or task added mid-session

## Carryover from Yesterday
- Item that didn't get done
```

If `~/TODAY.md` does not exist, create it with today's date and empty sections before proceeding.

---

## Skill Flow

### Mode: Morning Briefing (default)

1. **Read `~/TODAY.md`**
   - Note any carryover items from yesterday
   - Note any personal tasks already listed
   - If file doesn't exist, create it with today's date

2. **Fetch Calendar** (Google Calendar MCP)
   - Get today's events: titles, times, duration
   - Identify: total meeting time, largest focus blocks, any hard deadlines mentioned in event titles
   - Flag if today is meeting-heavy (>3 hrs) — this changes how much deep work is realistic

3. **Fetch Linear Issues** (Linear MCP)
   - Pull open issues assigned to the user, priority High and Urgent first
   - Also pull any issues with due dates today or this week
   - If a `CLAUDE.md` is present in the current directory, use it to filter to the active project
   - For each issue, note: project name, milestone name (if set), and status
   - Limit: top 15 issues max

4. **Synthesize and Output**

```
## Good morning. Here's your day — [WEEKDAY, DATE]

### Calendar
[List today's events with times. Call out focus blocks explicitly.]
Total meeting time: Xh | Largest focus block: Xh (TIME–TIME)

### Linear: What to Work On Today
[3–5 prioritized issues, grouped by project, with milestone and one-line rationale each]

**[Project Name]** — [milestone name if set]
1. [Issue ID] [Title] — [why today: due date / blocking / high priority]
2. ...

**[Project Name]** — [milestone name if set]
3. [Issue ID] [Title] — [why today]

### Personal Tasks
[From TODAY.md personal tasks section]
- [ ] ...

### Carryover
[Any unfinished items from yesterday's TODAY.md, if present]

### Today's Reality Check
[One honest sentence: e.g. "You have 4 hours of meetings — plan for 1 deep work block around 2pm."]
```

5. **Ask**: "Want me to update TODAY.md with this plan, or adjust anything?"
   - If yes: write the Focus line and today's Linear picks into TODAY.md
   - Never overwrite existing personal tasks or captures

---

### Mode: Reprioritize

Triggered by: `reprioritize`, `replan`, or mid-day request.

1. Re-fetch Linear issues (in case status has changed)
2. Read current TODAY.md — note what's been checked off
3. Re-fetch remaining calendar for the rest of the day
4. Output revised priority order with rationale
5. Ask if TODAY.md should be updated

---

### Mode: Capture

Triggered by: `capture [text]`

1. Read `~/TODAY.md`
2. Append to `## Captures` section with timestamp: `- [HH:MM] [text]`
3. Confirm: "Captured."
4. Optionally ask: "Want me to also create a Linear issue for this?"
   - If yes: create issue in Linear with title = capture text, ask for project assignment

---

### Mode: End of Day

Triggered by: `eod`, `wrap`, `end of day`

1. Read `~/TODAY.md`
2. Fetch Linear issues touched today (updated_at = today) via Linear MCP
3. Output summary:

```
## EOD Summary — [DATE]

### Completed
[Checked items from TODAY.md + Linear issues moved to Done today]

### In Progress / Carryover
[Unchecked items + Linear issues still In Progress]

### Captures to Action
[Any mid-session captures that haven't been addressed]

### Tomorrow: Top 3
[Suggested top 3 issues for tomorrow based on priority + what's still open]
```

4. Ask: "Want me to write the carryover to a new TODAY.md for tomorrow?"
   - If yes: create tomorrow's TODAY.md with carryover section pre-filled
   - Never delete today's file — rename it to `~/daily-logs/YYYY-MM-DD.md` if `~/daily-logs/` exists

---

## Key Rules

- **Never delete or overwrite TODAY.md captures or personal tasks** — only append or update specific sections
- **Never apply Linear changes without explicit confirmation**
- **Calendar data is read-only** — never create, modify, or delete calendar events
- **If Linear MCP is unavailable**, proceed with calendar + TODAY.md only; note Linear is offline
- **If Calendar MCP is unavailable**, proceed with Linear + TODAY.md only; note calendar is offline
- **Meeting-heavy days** (>3h meetings): reduce Linear recommendations to 2 items, flag explicitly
- **Prioritization order**: Urgent > High > due today > due this week > blocking other issues > High with recent activity
- **Keep output scannable** — this is a morning tool, not a report. No paragraph prose. Lists and short callouts only.

---

## MCP Dependencies

| Tool | Purpose |
|------|---------|
| Linear MCP | Fetch assigned issues, priorities, due dates |
| Google Calendar MCP | Fetch today's events, identify focus blocks |
| File system (bash) | Read/write `~/TODAY.md`, `~/daily-logs/` |

---

## Verification Checklist

1. `/daily-plan` with no args → morning briefing with all three sources
2. `/daily-plan capture buy coffee beans` → appended to TODAY.md Captures with timestamp
3. `/daily-plan reprioritize` → re-fetches Linear + calendar, revised list
4. `/daily-plan eod` → summary + carryover offer
5. Linear MCP offline → graceful degradation, calendar + TODAY.md only
6. No TODAY.md exists → creates file, proceeds with briefing
