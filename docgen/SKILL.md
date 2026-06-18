---
name: docgen
description: >
  Generate professional contract/agreement PDFs (and .docx CLM templates) from a
  declarative YAML config using the yaml-doc-generator tool ("docgen"). Use this
  whenever the user wants to create, manufacture, or mock up agreement documents —
  an MSA, NDA, SaaS/subscription agreement, amendment, exhibit, SOW, renewal notice,
  loan/credit agreement, fund/investment doc, BAA/DPA, government contract, or a whole
  document FAMILY between named parties — especially demo/test documents to load into
  Docusign Navigator/CLM or to feed an agreement-lifecycle agent. Triggers include
  "generate an MSA/NDA/agreement", "make demo contracts", "create a document family for
  <party> and <party>", "use docgen", or "use the yaml-doc-generator". Produces real
  PDFs with parties, clauses, and a manifest of critical dates (renewal/expiration).
user_invocable: true
compatibility: >
  Requires the yaml-doc-generator tool at /Users/paul.solans/dev/tools/yaml-doc-generator
  and `uv` (the tool is Python+uv; never use pip). Generates PDFs/.docx locally.
---

# docgen — YAML-driven contract document generation

Drive the `yaml-doc-generator` tool to turn a declarative YAML config into professional
contract PDFs (or `.docx` CLM templates). Define parties once, list the documents you want,
and the tool renders a complete family with a manifest of computed critical dates.

**Tool location:** `/Users/paul.solans/dev/tools/yaml-doc-generator`
**Always run via `uv`** from the tool directory: `cd <tool> && uv run docgen <cmd>`. Never `pip`.

## Prerequisites (check once)

```bash
cd /Users/paul.solans/dev/tools/yaml-doc-generator && uv run docgen --help
```
If that fails, the tool or `uv` isn't set up — tell the user; don't try to install around it.

## Step 1 — Discover capabilities live (don't guess)

The catalog of document types and clauses evolves. Read it from the tool rather than relying
on memory:

```bash
cd /Users/paul.solans/dev/tools/yaml-doc-generator
uv run docgen list types      # every document type + its KEY PARAMS
uv run docgen list clauses    # reusable clause keys
uv run docgen docs <clause-key>   # detail on one clause
uv run docgen list samples    # bespoke sample specs
```

`references/document-types.md` (bundled) is a snapshot for quick reference, but the live
`list types` is authoritative. Match the user's intent to a real `type` and its KEY PARAMS.

## Step 2 — Gather what you need

For a config you need:
- **Parties** — a `primary` and one or more `counterparties`. Each: `name`, `legal_name`,
  `entity_type`, `jurisdiction`, `address`, `signatory {name, title}`, `defined_term`.
  - `name` is what appears as the party label and in filenames. **If these documents will be
    joined to another system by party name (e.g. a Salesforce account, a Navigator
    counterparty), set `name` to match that system's value verbatim.**
  - `defined_term` is the in-contract role label; many templates impose their own (e.g.
    `saas_agreement` uses "Vendor"/"Customer" regardless) — that's fine.
- **Documents** — a list of `{type, params}` (optionally `id` + `parent_id` to link amendments
  and exhibits to a base agreement). Pull `params` from the type's KEY PARAMS.
- **Defaults** — `governing_law`, `venue`, and date behavior (see Step 3).

Ask the user only for what's genuinely missing or ambiguous; infer sensible defaults otherwise.
See `references/yaml-schema.md` for the full schema and `references/example-configs.md` for
copy-ready examples (including a SaaS subscription family with an amendment chain).

## Step 3 — Control the dates deliberately

Dates drive the manifest's `critical_dates` (renewal/expiration), which downstream agents read.
Two modes:
- **`defaults.auto_dates: true`** (default) — the tool picks deterministic past effective dates
  and auto-computes critical dates so a renewal lands near "today". Good for quick demos; you
  don't pick the exact day.
- **`defaults.auto_dates: false`** — you pin `effective_date` per document (precise control), but
  auto critical-date computation is **off**. To still surface a renewal/expiration, add a
  top-level **`critical_dates:`** list of `{type, date, description}` (dates as `YYYY-MM-DD`).

Pick timing to fit the story. For "this renewal is NOT urgent", pin the notice deadline ~90 days
out; for "on fire", a few days out. The renewal-notice deadline conventionally equals
(expiration − notice period), so keep the pinned date consistent with the term math.

## Step 4 — Author the config

Write the YAML to a sensible path (default: a `*/docgen-configs/` dir in the current project, or
`/tmp` for throwaways). Show it to the user before generating if it's non-trivial.

## Step 5 — Generate

```bash
cd /Users/paul.solans/dev/tools/yaml-doc-generator
uv run docgen generate <config.yaml> --outdir <output-dir>
```
Output lands in `<output-dir>/<family-slug>/`: one PDF per document, plus `manifest.json` and
`manifest.csv`. The family-slug subfolder is always appended.

## Step 6 — Report back

Read `<output-dir>/<family-slug>/manifest.json` and summarize: the generated files, parties,
effective dates, and the `critical_dates.dates[]` (with days-from-today if relevant). Point the
user at the output folder. To eyeball a PDF, read its first page.

## Optional — .docx CLM templates & browsing

- `uv run docgen template <type> --outdir <dir>` — emit a `.docx` doc-gen template with Document
  Assembler merge tags and signature anchors (for Docusign CLM generation flows), not a filled PDF.
- `uv run docgen catalog --output <file.json>` — machine-readable catalog of types/clauses.
- `uv run docgen serve` — local web UI to browse the generated document library.

## Error handling

- **`could not convert string to float`** / param type errors — a param expects a number; check
  KEY PARAMS (e.g. `uptime_percent: 99.5`, not `"99.5%"`).
- **Unknown/zero-output document type** — re-run `uv run docgen list types` and use an exact key.
- **`0 documents generated` with an `x <file>: <error>`** — read the printed traceback; usually a
  bad param value or malformed YAML for that one doc.
- **No `critical_dates`** — you set `auto_dates: false` without a top-level `critical_dates:` list
  (see Step 3).
- **Tool/`uv` missing** — surface it to the user; do not pip-install or bypass `uv`.
