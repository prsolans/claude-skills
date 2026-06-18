# docgen YAML config schema

A config describes one **family** — a set of related documents between the same parties.

```yaml
family:
  name: "Acme–Widget Procurement Package"   # human name; the slug derived from it names the output folder
  type: technology                          # domain/category label (free-form: technology, supplier_procurement, banking, ...)
  theme: corporate                          # PDF visual theme

parties:
  primary:                                  # the initiating party (one)
    name: "Acme Corporation"                # label shown in the doc + filenames; match external systems verbatim if joining by name
    legal_name: "Acme Corporation, Inc."
    entity_type: "corporation"
    jurisdiction: "State of Delaware"
    address: "100 Main Street, Suite 500, Wilmington, DE 19801"
    signatory: { name: "Jane Smith", title: "VP, Procurement" }
    defined_term: "Customer"                # in-contract role label (templates may override, e.g. saas → Vendor/Customer)
  counterparties:                           # one or more
    - name: "Widget Suppliers"
      legal_name: "Widget Suppliers, Inc."
      entity_type: "corporation"
      jurisdiction: "State of California"
      address: "200 Tech Drive, San Jose, CA 95134"
      signatory: { name: "John Doe", title: "CRO" }
      defined_term: "Provider"

defaults:
  governing_law: "State of New York"
  venue: "New York, New York"
  effective_date: null                      # optional global default effective date
  auto_dates: true                          # true: tool back-dates + auto-computes critical dates. false: you pin dates.

documents:                                  # ordered list; each rendered to one PDF
  - type: saas_agreement                    # a real type from `docgen list types`
    id: base-1                              # optional handle for linking
    params:                                 # type-specific; from the type's KEY PARAMS
      effective_date: "2023-12-14"          # honored when auto_dates: false (or as an override)
      initial_term_years: 3
      platform_name: "Acme Platform"
      uptime_percent: 99.9
  - type: exhibit_pricing
    id: ex-b
    parent_id: base-1                       # links this exhibit/amendment to its base agreement
    params:
      exhibit_id: B
      line_items:
        - { item: "Platform License", unit: "Annual", quantity: 1, unit_price: 500000 }
      payment_terms: 30
  - type: amendment
    id: amd-1
    parent_id: base-1
    params:
      amendment_number: 1
      underlying_agreement: "Software as a Service Agreement"
      underlying_date: "2023-12-14"
      summary: "Free-text description of what this amendment changes."

# Optional. Always written to the manifest regardless of auto_dates — use this to PIN a
# renewal/expiration when auto_dates is false (or to add bespoke deadlines).
critical_dates:
  - type: renewal_notice_deadline
    date: "2026-09-15"                      # YYYY-MM-DD
    description: "Deadline to deliver non-renewal notice (90-day notice before expiration)."

output:
  directory: ./output                       # base dir (a <family-slug>/ folder is appended); --outdir overrides
  manifest:
    enabled: true
    formats: [json, csv]
```

## Key behaviors
- **Output path:** `<outdir-or-output.directory>/<family-slug>/`. The slug comes from `family.name`.
- **Filenames:** `<FamilyPrefix>-<Counterparty>-<DocType>-<EffectiveDate>.pdf`.
- **`auto_dates: true`** → effective dates are deterministic-past (seeded by family name) and each
  doc's critical dates are auto-computed (e.g. `term_expiration`, `renewal_notice_deadline`).
- **`auto_dates: false`** → set `effective_date` in each doc's `params`; auto critical-date
  computation is OFF, so add a top-level `critical_dates:` list to surface renewal/expiration.
- **`manifest.json`** holds `documents[]` (each with `effective_date`, `critical_dates`) and a
  family-level `critical_dates` object: `{total, next_30_days, next_60_days, next_90_days, dates[]}`,
  where each `dates[]` entry is `{type, date, date_iso, description}`.
- **Numeric params** must be numbers, not strings. **Structured params** (`services`, `sla_metrics`,
  `line_items`) are YAML lists of maps.
