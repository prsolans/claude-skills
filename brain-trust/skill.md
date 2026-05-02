---
name: brain-trust
description: >
  Assemble a virtual advisory panel of 3 domain experts to pressure-test a plan,
  architecture, or deliverable. Each expert critiques independently, then their
  perspectives are synthesized into an actionable plan. Use when the user says
  "brain trust", "get expert opinions", "panel review", "advisory council",
  "what would experts think", or invokes /brain-trust.
---

# Brain Trust

Assemble three domain-relevant experts to critique, prioritize, and sharpen your plan before you build.

## Arguments

The user may provide:
- A file path to a plan, spec, or document to review
- A description of what they're building or deciding
- Both a file and additional context

If nothing is provided, look at the current conversation context and `_PLAN.md` for the subject matter. If still unclear, ask: "What are we brain-trusting today?"

## Step 1 — Read the subject matter

1. If a file path was given, read it.
2. If `_PLAN.md` exists in the repo root, read it for additional context.
3. Scan any recent conversation context for what the user is working on.
4. Identify the **domain** (e.g., enterprise SaaS go-to-market, distributed systems architecture, data pipeline design, UX research methodology).

## Step 2 — Assemble the panel

Based on the domain, select **3 expert personas** that would bring genuinely different lenses to this work. These should NOT be generic roles — they should be specific, opinionated archetypes.

**Selection criteria:**
- Each expert must bring a **distinct perspective** (not three variations of the same viewpoint)
- At least one should be a **contrarian or skeptic** — someone who'll push back
- At least one should be a **practitioner** — someone who's shipped this exact kind of thing
- At least one should represent the **end user or stakeholder** who'll be affected by the output
- Give each a name, a one-line bio, and a stated bias (what they're known for caring about)

**Present the panel to the user before proceeding:**

```
## Your Brain Trust

1. **[Name]** — [One-line bio]
   _Known for:_ [Their stated bias or lens]

2. **[Name]** — [One-line bio]
   _Known for:_ [Their stated bias or lens]

3. **[Name]** — [One-line bio]
   _Known for:_ [Their stated bias or lens]

Convening the panel...
```

## Step 3 — Individual critiques

For each expert, generate their independent review. Each expert should speak in a distinct voice and stay in character. Structure each review as:

```
### [Expert Name]'s Take

**What I'd prioritize (top 3):**
1. [thing] — [why, in their voice]
2. [thing] — [why]
3. [thing] — [why]

**What I'd cut or avoid:**
- [thing] — [why]
- [thing] — [why]

**The thing nobody's talking about:**
[One insight or blind spot they see that the others probably won't raise]

**Gut check (1-10):** [N]/10 — [one sentence on overall confidence in this plan]
```

**Important:**
- Experts should **disagree with each other** where their perspectives naturally conflict. Don't make them all agree.
- Critiques should be **specific to the actual content**, not generic advice. Reference specific items from the plan/doc.
- Each expert's voice should feel different — the skeptic should sound skeptical, the practitioner should sound pragmatic, etc.

## Step 4 — Synthesis

After all three critiques, synthesize:

```
## Brain Trust Synthesis

### Where all three agree
- [consensus items — these are high-confidence moves]

### Where they disagree
- [conflict] — [Expert A] says X, [Expert B] says Y
  _Recommendation:_ [your call on which perspective wins and why]

### Revised priorities (synthesized)
1. [highest priority action] — [why, drawing on expert input]
2. [next]
3. [next]
4. [next]
5. [next]

### Blind spots surfaced
- [things the experts raised that weren't in the original plan]

### What to drop
- [things experts agreed aren't worth the effort right now]
```

## Step 5 — Offer next steps

After the synthesis, ask:

> "Want me to update _PLAN.md with these priorities, or just keep this as a reference?"

If the user wants more depth on a specific expert's perspective, re-engage that persona for a deeper dive.

## Key rules

- **Experts must be domain-specific.** A plan about API architecture gets a distributed systems engineer, not a "business strategist." A GTM plan gets a field seller, not a "software architect."
- **Disagreement is the point.** If all three experts agree on everything, the panel isn't diverse enough. Recalibrate.
- **Stay concrete.** "You should think about scalability" is useless. "Your event-driven approach will bottleneck at the message broker when you hit 10K concurrent users — consider partitioning by tenant ID" is useful.
- **No sycophancy.** The experts are here to make the plan better, not to validate it. At least one expert should find something meaningfully wrong.
- **The synthesis is opinionated.** Don't just list the disagreements — make a recommendation on who's right and why.
