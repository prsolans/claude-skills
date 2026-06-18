# docgen document types (snapshot)

Authoritative source is always `uv run docgen list types`. This is a convenience snapshot.
Each type is used as a `documents[].type`; set `params` from the KEY PARAMS column.

## Core / standard
| type | what it is | key params |
|---|---|---|
| `nda` | Bilateral NDA (mutual confidentiality, exceptions, term, governing law). | `term_years` |
| `msa` | Master Services Agreement; auto/manual renewal, liability cap, termination + general provisions. Recital frames the **primary as the buyer engaging the counterparty to provide services**. | `initial_term_years`, `renewal_type`, `renewal_notice_days`, `liability_cap_months` |
| `amendment` | Numbered amendment referencing an underlying doc by name + date, with a free-text change summary. | `amendment_number`, `underlying_agreement`, `summary` (also `underlying_date`) |
| `exhibit_service_description` | Services list + optional SLA metrics table (usually Exhibit A to an MSA/SaaS). | `exhibit_id`, `services`, `sla_metrics` |
| `exhibit_pricing` | Line-item pricing table with quantities/unit prices/totals + payment terms. | `exhibit_id`, `line_items`, `payment_terms` |
| `sow` | Statement of Work. | (see `list types`) |
| `renewal_notice` | Formal renewal/non-renewal notice with current term end + action deadline. | `agreement_name`, `current_term_end`, `renewal_type` |
| `service_order` | Committed services order (NRC/MRC), CPE schedule, term; incorporates a parent MSA. | `order_id`, `services`, `term_years` |
| `custom` | Free-form doc via DocumentBuilder (title, recitals, articles). | `title`, `recitals`, `articles` |
| `bespoke` | Renders an external bespoke spec file alongside standard docs. | `spec_file` |

## Technology
| type | what it is | key params |
|---|---|---|
| `saas_agreement` | Cloud subscription agreement; uptime SLA, data privacy, IP. Recital frames the **primary as the Vendor providing the platform to the Customer** (right direction for a SaaS vendor). | `initial_term_years`, `platform_name`, `uptime_percent` (numeric, e.g. `99.5`) |
| `software_license` | On-prem/subscription license; delivery, updates, audit rights, IP. | `license_type`, `license_scope`, `term_years` |
| `data_processing_addendum` | GDPR/CCPA DPA; controller/processor, sub-processors, transfers, breach. | `parent_agreement`, `purposes` |

## Banking
`credit_agreement` (`facility_amount`, `interest_rate`, `interest_type`, `term_years`) ·
`promissory_note` (`principal_amount`, `interest_rate`, `maturity_date`) ·
`security_agreement` (`collateral_description`) · `guaranty` (`guaranteed_amount`) ·
`correspondent_agreement` (`services`, `minimum_balance`) ·
`compliance_certificate` (`agreement_name`, `period_end`, `covenant_results`).

## Investment
`ima` (`discretionary`, `management_fee`, `performance_fee`) ·
`lpa` (`fund_name`, `target_size`, `management_fee`, `carried_interest`) ·
`subscription_agreement` (`fund_name`, `commitment_amount`) ·
`side_letter` (`fund_name`, `include_mfn`, `include_co_invest`, `include_excuse`) ·
`custody_agreement` (`annual_fee`) · `administration_agreement` (`services`, `annual_fee`).

## Healthcare
`baa` (`primary_function`) · `data_use_agreement` (`data_description`, `permitted_uses`) ·
`provider_services_agreement` (`services`, `term_years`) ·
`provider_participation_agreement` (`network_name`, `term_years`) ·
`telemedicine_agreement` (`platform_name`, `term_years`).

## Government
`government_fixed_price_contract` (`contract_number`, `period_of_performance_years`, `ceiling_amount`) ·
`government_idiq` (`contract_number`, `ordering_period_years`, `ceiling_amount`).

## Notes
- Pass arrays/objects for structured params (`services`, `sla_metrics`, `line_items`) as YAML lists/maps — see `references/example-configs.md`.
- Numeric params must be numbers, not strings (`uptime_percent: 99.5`, not `"99.5%"`).
- Link docs with `id` on a base agreement and `parent_id` on its exhibits/amendments.
