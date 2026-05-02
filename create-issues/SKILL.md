---
name: create-issues
description: Use when the user wants to process a meeting transcript into Linear issues. Reads a transcript file and optional support documents, analyzes them for action items, decisions, and open questions, proposes Linear issues and milestone organization, then waits for human review before creating anything. Triggers on "/create-issues [transcript path] [optional: doc paths or folder paths...]".
disable-model-invocation: true
---

# create-issues Skill

Processes a meeting transcript into a structured Linear backlog. Analyzes the transcript, proposes issues and milestones, waits for explicit human review, then executes only what's confirmed.

---

## Argument Handling

`$ARGUMENTS` is space-separated. The first token is always the transcript or audio file. Any additional tokens are support documents or folders:

```
/create-issues path/to/transcript.txt
/create-issues path/to/recording.m4a
/create-issues path/to/transcript.txt doc1.pdf doc2.md
/create-issues path/to/transcript.txt _context/reference/
```

- The first argument can be an **audio or video file** (mp3, m4a, wav, flac, ogg, webm, mp4, avi, mkv, mov) — transcription runs automatically before analysis (see Step 0).
- Transcript can be any plain text format: Gong export, Zoom transcript, manual notes, etc.
- Support documents can be any readable file type: PDF, markdown, plain text, etc.
- If a support document argument is a folder path, read all files in that folder (one level deep, non-recursive).

### If no arguments are given — interactive file selection

1. List files in `_context/transcripts/` (relative to repo root). Sort by most recently modified first. Show with index numbers and dates.
   > **Found in _context/transcripts/:**
   > 1. gbis-kickoff-2026-04-06.md (today)
   > 2. planning-session-2026-03-28.md
   >
   > Which transcript? Enter a number.

   Wait for the user to pick before continuing.

2. List files in `_context/reference/` the same way.
   > **Found in _context/reference/:**
   > 1. roadmap.md
   > 2. executive-summary.md
   >
   > Include any support docs? Enter numbers, "all", or "none".

   Wait for the user's response.

3. If `_context/transcripts/` doesn't exist or is empty, fall back to asking the user to provide a file path.
4. If `_context/reference/` doesn't exist or is empty, skip the support docs prompt and proceed with transcript only.

---

## Step 0 — Transcribe (if audio input)

If the first argument has an audio or video extension (mp3, m4a, wav, flac, ogg, webm, mp4, avi, mkv, mov):

1. Check dependencies:
   ```bash
   which ffmpeg > /dev/null 2>&1 || echo "NEED_FFMPEG"
   uv tool list 2>/dev/null | grep -q whisper || echo "NEED_WHISPER"
   ```
   If `NEED_FFMPEG`: run `brew install ffmpeg`
   If `NEED_WHISPER`: run `uv tool install openai-whisper --with torch --with setuptools-rust`

2. Run Whisper using the `base` model:
   ```bash
   whisper "<file_path>" --model base --output_format txt --output_dir /tmp/whisper_out
   ```
   Tell the user: "Transcribing with Whisper base model..." and note if this is the first run (model download required).

3. Read the output from `/tmp/whisper_out/<filename_without_ext>.txt`.

4. Save the transcript to `_context/transcripts/` using the same base filename with a `.txt` extension. Create the directory if it doesn't exist.

5. Tell the user: "Transcript saved to `_context/transcripts/<filename>.txt`. Proceeding with analysis..."

6. Use this transcript file as the input for Step 1. Continue the normal flow.

If the first argument is not an audio file, skip this step entirely.

---

## Step 1 — Read all inputs

1. Read the transcript file. If it doesn't exist or can't be read, stop and tell the user.
2. Read each support document. If a path is a folder, read all files in it.
   - For plain text and markdown files: use the Read tool directly.
   - For `.xlsx` / `.xls` files: extract content via Bash using `uv run python -c "import openpyxl; wb = openpyxl.load_workbook('PATH'); [print(sheet.title, [[c.value for c in r] for r in sheet.iter_rows()]) for sheet in wb.worksheets]"`. Install openpyxl inline if needed: `uv run --with openpyxl python -c "..."`.
   - For `.csv` files: read directly with the Read tool.
   - For `.pdf` files: use the Read tool (Claude can read PDFs natively).
   - For other binary formats: note them as unsupported and skip.
3. Before proceeding, show the user a brief inventory:
   > **Inputs loaded:**
   > - Transcript: `[filename]`
   > - Support docs: `[filename1]`, `[filename2]` (or "none")

Scan all inputs fully before drawing any conclusions.

---

## Step 2 — Detect Linear project

1. Check for `_PROJECT.md` in the current repo root.
   - If found, extract `linear_project` from the `## Meta` section.
   - Call `list_projects` to resolve the name to an ID. Display the resolved name and ID.
2. If no `_PROJECT.md` found, call `list_projects` and present the list. Ask the user which project this meeting belongs to.
3. Fetch the project's existing milestones via `list_milestones` so you can assign issues to existing milestones or propose new ones.

---

## Step 3 — Analyze all inputs

Using the transcript, support documents, and project context, extract:

Support documents are full inputs — not just background. Surface action items, gaps, or issues from them directly if they reveal something actionable, even if not explicitly discussed in the transcript. Attribute the source when relevant (e.g. "identified in roadmap.md").

### Decisions made
Concrete choices that were reached in the meeting. Not opinions or discussion — actual "we're going to do X" moments. Each should be one sentence.

### Open questions
Unresolved items explicitly raised but not answered. Things that need follow-up or a decision before work can proceed.

### Action items → candidate issues
For each concrete task or deliverable mentioned:
- Who owns it (if named)
- What needs to happen
- Why it matters (context from the meeting)
- Which existing milestone it belongs to, OR if a new milestone is needed
- Suggested priority: Urgent / High / Medium / Low
  - Urgent: blocks other work or has an immediate external deadline
  - High: directly advances the current milestone
  - Medium: useful but not blocking
  - Low: nice-to-have, future consideration

### Issues to close
Any issues that were discussed and confirmed complete in this meeting, if you can match them to existing Linear issues (via project ID you already have).

### New milestones
If the meeting suggests a new project phase, deliverable, or time-box that doesn't match an existing milestone, propose it. Include a short name and what it covers.

---

## Step 4 — Present the review proposal

Output this exact structure before taking any action:

```
## Meeting Analysis: [filename or first line of transcript as title] — [today's date]

### Summary
[2–3 sentences capturing what the meeting was about and what was resolved]

### Decisions made
- [decision]
- [decision]

### Open questions
- [question]

### Proposed issues
N issues to create in [Project Name]:

1. **[Title]** — [Priority]
   Milestone: [existing milestone name] | [NEW: proposed milestone name]
   > [2–3 bullet description of what and why, drawn from meeting context]

2. **[Title]** — [Priority]
   ...

### New milestones proposed
- **[Milestone name]** — [one sentence: what phase or scope it covers]

(Omit this section if no new milestones are needed.)

### Issues to close
- [PRS-XXX] [Title] — confirmed complete per meeting discussion

(Omit this section if none identified.)

---
Review the above. Reply with:
- **"all"** — apply everything as proposed
- **Issue numbers** (e.g. "1 3 5") — create only those issues
- **"milestones only"** — create new milestones, no issues yet
- **"none"** — cancel, no changes made
- Or tell me what to change before applying
```

Wait for the user's response before proceeding. Do not create anything yet.

---

## Step 5 — Apply confirmed actions

After the user confirms:

1. **Re-verify the project ID** by re-reading from memory or re-fetching — do not assume it's unchanged.
2. **New milestones first** — create any confirmed new milestones before creating issues (issues may need to reference them).
3. **Create issues** for each confirmed item:
   - Title: short, action-oriented (imperative verb, e.g. "Add auth middleware")
   - Description: bullet points from the proposal — no paragraphs
   - Priority: as proposed
   - Assignee: me (the authenticated user)
   - Milestone: set if confirmed
4. **Close confirmed issues** — update their status to Done.
5. Report what was created/closed:

```
✅ Created: [N] issues
✅ Closed: [N] issues
✅ Created milestone: [name] (if applicable)

Issues created:
- [PRS-XXX] [Title]
- [PRS-XXX] [Title]
```

---

## Key rules

- **Never create or close anything without explicit user confirmation** — the review step is mandatory.
- **Never skip the review** even if the transcript is short or the action items seem obvious.
- **Frame uncertainty honestly** — if something might be an action item but is ambiguous, include it as a proposal and flag the ambiguity.
- **Issue titles must be imperative and scannable** — not "We need to look at the auth flow", but "Audit auth flow and identify gaps".
- **Descriptions are bullets only** — no prose paragraphs in issue descriptions.
- **One issue per discrete task** — don't bundle unrelated items into a single issue.
- **Don't invent scope** — only propose issues based on what's explicitly in the transcript.
- **Decisions and open questions are for context** — surface them in the review output but don't create Linear issues for them unless they're also actionable tasks.

---

## Verification checklist

1. `/create-issues` (no args) → lists _context/transcripts/, user picks; lists _context/reference/, user picks; proceeds
2. `/create-issues` + _context/transcripts/ empty → asks user to provide a file path
3. `/create-issues notes/standup.txt` → reads transcript only, shows inventory, proceeds
4. `/create-issues transcript.md doc1.pdf doc2.md` → reads all three, shows inventory, proceeds
5. `/create-issues transcript.md _context/reference/` → reads transcript + all files in folder, shows inventory
6. `/create-issues recording.m4a` → transcribes with Whisper, saves to _context/transcripts/, proceeds with analysis
7. `/create-issues recording.m4a doc1.pdf` → transcribes audio, reads support doc, proceeds
8. Project not found in _PROJECT.md → lists projects, asks user to confirm
9. User replies "2 4" → creates only issues 2 and 4, reports result
10. User replies "all" → creates all issues + milestones + closes confirmed issues
11. User replies "none" → confirms cancelled, nothing written to Linear
12. File not found → clear error, no further action
13. Support doc from folder can't be read → skip it, note it in inventory, continue
