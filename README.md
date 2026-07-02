# claude-skills

A personal collection of [Claude Code](https://claude.com/claude-code) skills — reusable capabilities that Claude can invoke automatically (based on the task) or via an explicit `/slash-command`.

## Skills

### brain-trust
Assembles a virtual panel of 3 domain experts to pressure-test a plan, architecture, or deliverable. Each expert critiques independently, then their perspectives are synthesized into one actionable plan. Trigger: "brain trust", "panel review", or `/brain-trust`.

### code-review
A fast, targeted pre-deploy check for AI-generated code. Catches debug artifacts, hardcoded values, placeholders, dead scaffolding, over-engineering, hallucinated APIs, and missing error handling — not a general quality audit. Trigger: "is this ready?", "review what Claude wrote".

### create-issues
Turns a meeting transcript (plus optional support docs) into a proposed Linear backlog — issues, milestones, action items — and waits for human review before creating anything. Trigger: `/create-issues <transcript> [docs...]`.

### daily-plan
A personal daily-operating layer above Linear. Merges Linear issues, Google Calendar, and a local `TODAY.md` scratch file into a morning briefing, mid-day reprioritization, or end-of-day handoff. Trigger: "start my day", "wrap up", `/daily`, `/eod`.

### docgen
Generates realistic contract/agreement PDFs and .docx CLM templates (MSA, NDA, SOW, amendments, whole document families) from a YAML config — handy for demo data in Docusign Navigator/CLM. Trigger: "generate an MSA/NDA", "make demo contracts".

### find-skills
Helps discover and install skills from the open agent-skills ecosystem when you ask "is there a skill for X" or want to extend Claude's capabilities.

### linear-calendar
Renders a visual HTML week-view calendar of your Linear issues (by due date) and project target dates, with month-end and milestone summaries. Trigger: "linear calendar", "show my calendar".

### pptx
Handles any task touching a `.pptx` file — creating, reading, editing, or restyling slide decks and presentations, always starting from the corporate template. Trigger: mentions of "deck", "slides", or a `.pptx` filename.

### project-init
Interactively creates a `_PROJECT.md` file for the current repo, pulling context from existing repo files and Linear before asking clarifying questions. Trigger: "project init", "create PROJECT.md".

### review-issues
Reviews a project or milestone's open Linear issues, surfacing prioritization gaps, stale tickets, and sprint-planning suggestions, with optional confirmed changes applied in Linear. Trigger: "review issues", "groom backlog".

### skill-creator
Meta-skill for building, editing, and benchmarking other skills — drafts a skill, runs test prompts, and helps evaluate results qualitatively and quantitatively. Trigger: "create a skill", "optimize this skill".

### transcribe
Transcribes audio or video to text locally using OpenAI Whisper. Accepts local files (mp3, m4a, wav, mp4, webm, etc.) or URLs (YouTube, Loom, anything yt-dlp supports). Trigger: "transcribe this".

### work-issue
Works a Linear issue autonomously end-to-end — loads the issue, `_PLAN.md`, and `CLAUDE.md` context, then implements, tests, and reports back. Trigger: `/work-issue <issue-id>`.

## Installation

Claude Code automatically loads any skill folder placed under `~/.claude/skills/`. Each skill is just a directory containing a `SKILL.md` (plus any supporting scripts/assets).

### Install all skills

```bash
git clone https://github.com/prsolans/claude-skills.git ~/.claude/skills
```

If `~/.claude/skills` already exists, clone elsewhere and copy the contents in instead:

```bash
git clone https://github.com/prsolans/claude-skills.git /tmp/claude-skills
cp -R /tmp/claude-skills/. ~/.claude/skills/
```

### Install a single skill

Copy just that skill's folder into your skills directory:

```bash
git clone --depth 1 https://github.com/prsolans/claude-skills.git /tmp/claude-skills
cp -R /tmp/claude-skills/<skill-name> ~/.claude/skills/<skill-name>
```

### Verify

Start a new Claude Code session and run `/help`, or just describe a task that matches a skill's trigger — Claude will invoke it automatically. Skills invoked explicitly are available as `/<skill-name>`.

No restart is required beyond starting a new session; Claude Code reads `~/.claude/skills/` at session start.
