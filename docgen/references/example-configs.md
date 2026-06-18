# docgen example configs

Copy-ready patterns. Also see the tool's own `examples/configs/*.yaml` (e.g.
`fontara_procurement.yaml`) and the live `examples/configs/` directory.

## A. SaaS subscription family with a pinned ~90-day renewal + amendment chain

The pattern used for the Docusign Risk Radar demo: a SaaS vendor (`primary`) and a customer
(`counterparty`), a base subscription agreement + service/pricing exhibits + an amendment that
changes a substantive term (not the renewal date), with the renewal-notice deadline pinned a
calm ~90 days out. Working copies live in the docusign-agents repo at
`_context/demo-docs/configs/fontara-northwind.yaml` and `fontara-evergreen.yaml`.

```yaml
family:
  name: "Fontara–Northwind Subscription Package"
  type: technology
  theme: corporate

parties:
  primary:
    name: "Fontara"
    legal_name: "Fontara, Inc."
    entity_type: "corporation"
    jurisdiction: "State of Delaware"
    address: "23 Main Street, Suite 1800, Seattle, WA 98122"
    signatory: { name: "Alex Rivera", title: "Chief Revenue Officer" }
    defined_term: "Vendor"
  counterparties:
    - name: "Northwind Trading Co."        # == the Salesforce Account.Name, verbatim
      legal_name: "Northwind Trading Co."
      entity_type: "corporation"
      jurisdiction: "State of Illinois"
      address: "410 North Michigan Avenue, Suite 700, Chicago, IL 60611"
      signatory: { name: "Dana Whitfield", title: "VP, Procurement" }
      defined_term: "Customer"

defaults:
  governing_law: "State of Delaware"
  venue: "Wilmington, Delaware"
  auto_dates: false                         # pin dates precisely

documents:
  - type: saas_agreement
    id: saas-1
    params:
      effective_date: "2023-12-14"          # +3yr term => 2026-12-14 expiration
      initial_term_years: 3
      platform_name: "Fontara Subscription Platform"
      uptime_percent: 99.5
  - type: exhibit_service_description
    id: exhibit-a
    parent_id: saas-1
    params:
      exhibit_id: A
      effective_date: "2023-12-14"
      services:
        - { name: "Fontara Subscription Platform", description: "Hosted access to the SaaS platform, updates, and tier-1 support." }
      sla_metrics:
        - { metric: "Platform Availability", target: "99.5%", measurement: "Monthly", remedy: "Service credit per Vendor's standard schedule" }
  - type: exhibit_pricing
    id: exhibit-b
    parent_id: saas-1
    params:
      exhibit_id: B
      effective_date: "2023-12-14"
      line_items:
        - { item: "Fontara Platform Subscription", unit: "Annual", quantity: 1, unit_price: 200000 }
      payment_terms: 60
  - type: amendment
    id: amd-1
    parent_id: saas-1
    params:
      effective_date: "2025-03-01"
      amendment_number: 1
      underlying_agreement: "Software as a Service Agreement"
      underlying_date: "2023-12-14"
      summary: "Increases the liability cap to 36 months of fees and adds a Data Security Addendum. Term and renewal unchanged."

critical_dates:                             # pinned because auto_dates is off
  - type: renewal_notice_deadline
    date: "2026-09-15"                      # ~90 days out: calm, not urgent
    description: "90-day non-renewal notice deadline before the 2026-12-14 expiration."

output:
  directory: ./output
  manifest: { enabled: true, formats: [json, csv] }
```

Generate:
```bash
cd /Users/paul.solans/dev/tools/yaml-doc-generator
uv run docgen generate <path-to-config>.yaml --outdir <output-dir>
```

## B. Quick multi-doc procurement family (auto dates)

When you don't need precise timing, omit `auto_dates` (defaults true) and let the tool date
everything and compute critical dates near "today":

```yaml
family: { name: "Acme–Widget Procurement Package", type: supplier_procurement, theme: corporate }
parties:
  primary:
    name: "Acme Corporation"
    legal_name: "Acme Corporation, Inc."
    entity_type: corporation
    jurisdiction: "State of Delaware"
    address: "100 Main Street, Wilmington, DE 19801"
    signatory: { name: "Jane Smith", title: "VP, Procurement" }
    defined_term: "Customer"
  counterparties:
    - name: "Widget Suppliers"
      legal_name: "Widget Suppliers, Inc."
      entity_type: corporation
      jurisdiction: "State of California"
      address: "200 Tech Drive, San Jose, CA 95134"
      signatory: { name: "John Doe", title: "CRO" }
      defined_term: "Provider"
defaults: { governing_law: "State of New York", venue: "New York, New York" }
documents:
  - { type: nda, params: { term_years: 3 } }
  - { type: msa, params: { initial_term_years: 3, renewal_type: auto, renewal_notice_days: 90, liability_cap_months: 12 } }
output: { directory: ./output, manifest: { enabled: true, formats: [json, csv] } }
```

## Tips
- To make documents joinable to Salesforce/Navigator, set the counterparty `name` to the exact
  account/counterparty string in that system.
- For a vendor→customer subscription story use `saas_agreement` (frames primary as Vendor). For a
  buyer→supplier services story use `msa` (frames primary as engaging the counterparty).
- Keep a pinned `renewal_notice_deadline` consistent with the term math: deadline = expiration −
  notice period.
