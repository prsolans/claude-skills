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

## Step 0 — Anchor the user's position

Before reading anything, ask:

> "Before we convene the panel — what's your current position? What do you believe or plan to do right now? One sentence."

Wait for the response. If the user has a position, reference it explicitly in at least one expert critique ("you said you're leaning toward X — here's why that's worth questioning"). If they say they don't have one yet, proceed without it.

This is the anchor the panel pushes against. Without it, the experts have no target.

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
- Give each a name, a **specific bio grounded in real experience** — not just a role title. Include the kind of work they've shipped, the failures they've lived through, or the context that shaped their bias. "A senior engineer who debugged production Kafka lag" activates more differentiated thinking than "a senior engineer."
- State their bias explicitly (what they're known for caring about)

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
- **Each expert after the first must explicitly contradict at least one claim made by a prior expert.** If all three experts reach compatible conclusions via different paths, the panel isn't diverse enough — recalibrate.
- Critiques should be **specific to the actual content**, not generic advice. Reference specific items from the plan/doc.
- Each expert's voice should feel different — the skeptic should sound skeptical, the practitioner should sound pragmatic, etc.
- **Gut check scores should diverge.** If all three give 7/10, that's false precision. Push experts toward genuinely different confidence levels and require them to explain the gap.

## Step 4 — Synthesis

After all three critiques, synthesize. The synthesis surfaces the decision — it does not make it. Your job is to map the terrain clearly enough that the user can decide confidently.

```
## Brain Trust Synthesis

### Where all three agree
- [consensus items — act on these with confidence]

### Where they disagree
- [conflict] — [Expert A] says X, [Expert B] says Y
  _The trade-off:_ [what's actually at stake in this disagreement — not who's right]

### Blind spots surfaced
- [things the experts raised that weren't in the original plan or subject matter]

### What to drop
- [things experts agreed aren't worth the effort right now]

### Your decision
The panel has done its job. Here's the landscape:
- **Clear:** [2–3 consensus items the user can act on now]
- **Contested:** [1–2 items where reasonable people disagree — these need your call]

What do you want to do?
```

## Step 5 — Follow through

After the user responds:

- If they want to act on specific items, help them execute or update `_PLAN.md`.
- If they want to go deeper on one expert's perspective, re-engage that persona for a focused dive.
- If they're still undecided on a contested item, offer to explore the specific trade-off rather than re-running the full panel.

## Key rules

- **Experts must be domain-specific.** A plan about API architecture gets a distributed systems engineer, not a "business strategist." A GTM plan gets a field seller, not a "software architect."
- **Disagreement is the point.** If all three experts agree on everything, the panel isn't diverse enough. Recalibrate.
- **Stay concrete.** "You should think about scalability" is useless. "Your event-driven approach will bottleneck at the message broker when you hit 10K concurrent users — consider partitioning by tenant ID" is useful.
- **No sycophancy.** The experts are here to make the plan better, not to validate it. At least one expert should find something meaningfully wrong.
- **The synthesis presents — it doesn't decide.** Surface what's clear and what's contested. The user makes the call.
- **These are synthetic experts.** They pattern-match from training data, not lived experience. They have no accountability for being wrong. Hold the output accordingly — useful for framing, not authoritative on facts.

## When not to use brain-trust

- **Factual or technical correctness is the primary need** — synthetic experts generate confident opinions from training data. If you need ground truth (specific API behavior, legal accuracy, medical guidance), use a real expert.
- **High-stakes irreversible decisions** — the false confidence from a synthetic panel is most costly when you can't undo the outcome. A panel that sounds authoritative isn't.
- **You need real stakeholder buy-in** — a synthetic panel can't substitute for getting actual humans aligned. It can help you *prepare* for that conversation, not replace it.
- **You already know what you want to do** — if you have a strong pre-existing preference, you'll route toward whichever expert agrees with you. Notice if you're shopping for validation rather than pressure-testing.
