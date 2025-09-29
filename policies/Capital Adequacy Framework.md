```markdown
# Capital Adequacy Framework

Version: 1.0
Effective Date: 2025-10-01

## Purpose
Define how the Bank measures, monitors and governs capital adequacy. The framework translates regulatory concepts into precise, auditable calculations that are computable from the FakeBank dataset so policy breaches and stress scenarios can be tested automatically.

## Scope & Data Sources
Primary dataset fields:
- `data/loans.parquet`: `ead`, `rwa`, `capital`, `loan_id`, `as_of_date`, `industry`, `geography`
- `data/market_risk_metrics.parquet`: desk-level market RWA proxies or VaR-derived capital
- Optional: `data/global_capital.parquet` for aggregate capital line items

## Definitions and Core Calculations
- Total RWA (RWA_total): the sum of credit RWAs and market RWAs at each `as_of_date`.
- Bank Capital (Capital_total): aggregate of capital-eligible items; in the synthetic dataset use aggregated `capital` plus any global capital rows.
- Capital Adequacy Ratio (CAR): CAR = Capital_total / RWA_total. Measured monthly for every `as_of_date` snapshot.

## Limit Framework and Aggregation Rules
All limits are expressed with clear aggregation rules so calculations are reproducible.

- CAR thresholds (monthly, by `as_of_date`):
  - Green: CAR >= 12.0% — normal operations
  - Amber: 10.5% <= CAR < 12.0% — Executive review required
  - Red: CAR < 10.5% — immediate remediation and Board escalation

- Single customer exposure limit: compute exposure_i = sum(EAD) for customer i at `as_of_date`. Limit: max_i(exposure_i) <= 5% * Capital_total. Alert when > 90% of limit (4.5%).

- RWA movements: measure month-on-month % change in RWA_total and attribute to dimensions (industry, geography) by aggregating loans.rwa grouped by those dimensions.

## Measurement Frequency & Ownership
- Frequency: Monthly (aligned to `as_of_date`). Ad-hoc after stress tests.
- Owner: CRO (accountable); Risk Analytics (calculations and reports); CFO (capital actions).

## Escalation & Remediation Procedures
- Amber breach (CAR between 10.5% and 12%):
  - Notify: CRO, CFO, Head of Risk Analytics within 2 business days.
  - Actions: freeze non-essential dividend or buyback activity; prepare capital plan within 30 calendar days.

- Red breach (CAR < 10.5%):
  - Notify: CRO, CFO, CEO, Board Risk Committee immediately (within 1 business day).
  - Actions (immediate): restrict new high-risk originations by product_type; invoke contingency capital measures (e.g., capital raising); produce 7-day and 30-day remediation plans.

## Stress Testing & Scenario Design
- Required monthly scenario set: credit migration shock, market SVaR shock and combined liquidity-driven capital hits. Recompute CAR under each scenario and report the earliest `as_of_date` where CAR crosses Amber/Red.

## Data Governance & Auditability
- All capital calculations must be stored as reproducible scripts with dataset versioning. Use the seeded generator (`SEED=42`) for repeatable test runs.
- Validation: reconcile Capital_total against known capital line-items; verify no null RWAs for material exposures.

--
This framework is synthetic and intended for testing, analytics and training with the FakeBank dataset.
```
```markdown
# Capital Adequacy Framework

Version: 1.0
Effective Date: 2025-10-01

## Purpose
Define how the Bank measures, monitors and governs capital adequacy. The framework translates regulatory concepts into precise, auditable calculations that are computable from the FakeBank dataset so policy breaches and stress scenarios can be tested automatically.

## Scope & Data Sources
Primary dataset fields:
- `data/loans.parquet`: `ead`, `rwa`, `capital`, `loan_id`, `as_of_date`, `industry`, `geography`
- `data/market_risk_metrics.parquet`: desk-level market RWA proxies or VaR-derived capital
- Optional: `data/global_capital.parquet` for aggregate capital line items

## Definitions and Core Calculations
- Total RWA (RWA_total): the sum of credit RWAs and market RWAs at each `as_of_date`.
- Bank Capital (Capital_total): aggregate of capital-eligible items; in the synthetic dataset use aggregated `capital` plus any global capital rows.
- Capital Adequacy Ratio (CAR): CAR = Capital_total / RWA_total. Measured monthly for every `as_of_date` snapshot.

## Limit Framework and Aggregation Rules
All limits are expressed with clear aggregation rules so calculations are reproducible.

- CAR thresholds (monthly, by `as_of_date`):
  - Green: CAR >= 12.0% — normal operations
  - Amber: 10.5% <= CAR < 12.0% — Executive review required
  - Red: CAR < 10.5% — immediate remediation and Board escalation

- Single customer exposure limit: compute exposure_i = sum(EAD) for customer i at `as_of_date`. Limit: max_i(exposure_i) <= 5% * Capital_total. Alert when > 90% of limit (4.5%).

- RWA movements: measure month-on-month % change in RWA_total and attribute to dimensions (industry, geography) by aggregating loans.rwa grouped by those dimensions.

## Measurement Frequency & Ownership
- Frequency: Monthly (aligned to `as_of_date`). Ad-hoc after stress tests.
- Owner: CRO (accountable); Risk Analytics (calculations and reports); CFO (capital actions).

## Escalation & Remediation Procedures
- Amber breach (CAR between 10.5% and 12%):
  - Notify: CRO, CFO, Head of Risk Analytics within 2 business days.
  - Actions: freeze non-essential dividend or buyback activity; prepare capital plan within 30 calendar days.

- Red breach (CAR < 10.5%):
  - Notify: CRO, CFO, CEO, Board Risk Committee immediately (within 1 business day).
  - Actions (immediate): restrict new high-risk originations by product_type; invoke contingency capital measures (e.g., capital raising); produce 7-day and 30-day remediation plans.

## Stress Testing & Scenario Design
- Required monthly scenario set: credit migration shock, market SVaR shock and combined liquidity-driven capital hits. Recompute CAR under each scenario and report the earliest `as_of_date` where CAR crosses Amber/Red.

## Data Governance & Auditability
- All capital calculations must be stored as reproducible scripts with dataset versioning. Use the seeded generator (`SEED=42`) for repeatable test runs.
- Validation: reconcile Capital_total against known capital line-items; verify no null RWAs for material exposures.

--
This framework is synthetic and intended for testing, analytics and training with the FakeBank dataset.
```
```markdown
# Capital Adequacy Framework

Version: 1.0
Effective Date: 2025-10-01

## Purpose
This framework defines how the Bank measures, monitors and governs capital adequacy for the hypothetical dataset. It translates regulatory concepts into precise, repeatable calculations based on the synthetic data model (see `specs/credit_risk.md` and `specs/risk_policies.md`).

## Scope
Applies to all credit, market and operational exposures captured in the dataset. Primary data sources are:
- `data/loans.parquet` (columns of interest: `loan_id`, `customer_id`, `as_of_date`, `ead`, `rwa`, `provisions`, `capital`, `loan_amount`)
- `data/market_risk_metrics.parquet` and `data/market_positions.parquet` (market exposures)
- `data/liquidity_metrics.parquet` (for concentration and stress tests impacting capital)

## Core Metrics and Definitions
- Risk Weighted Assets (RWA): use `loans.rwa` aggregated by `as_of_date`. RWA_total = sum(loans.rwa) + market_RWA (as computed in market risk tables).
- Regulatory Capital (Capital): use `loans.capital` and any global capital allocations stored in dataset-level metadata. CET1_proxy = sum(capital_eligible_items) — in this synthetic dataset, use `capital` as capital allocation per exposure and aggregate as BankCapital = sum(loans.capital).
- Capital Adequacy Ratio (CAR): CAR = BankCapital / RWA_total. Measure monthly at each `as_of_date`.

## Minimum Standards and Thresholds
- Internal minimum CAR: 10.5% (Pillar 2 buffer included). Trigger levels:
  - Green: CAR >= 12% — normal operations
  - Amber: 10.5% <= CAR < 12% — executive review and capital planning
  - Red: CAR < 10.5% — immediate remediation and escalation to Board
- Single customer exposure limit: max exposure to a single customer <= 5% of BankCapital (enforced monthly using `loans.ead` aggregated by `customer_id` and `as_of_date`).

## Calculation Frequency and Ownership
- Frequency: Monthly, at each `as_of_date` snapshot (align with synthetic panel data frequency).
- Owner: Chief Risk Officer (CRO) is accountable; Risk Analytics team produces monthly reports.

## Data Mapping and Reconciliation
- Primary calculation fields:
  - RWA_total = sum(`loans.rwa`) + sum(market_RWA from `market_risk_metrics`)
  - BankCapital = sum(`loans.capital`) + any capital items in `data/global_capital.parquet` (if present)
  - Single customer exposure = sum(`loans.ead`) by `customer_id`
- Reconciliation checks:
  - Row counts and null checks for `rwa`, `capital`, `ead` each month.
  - Sensitivity check: applying a +10% shock to RWAs and verifying CAR movement.

## Stress Testing and Scenario Analysis
- Run monthly stress scenarios using the synthetic time series across `as_of_date`:
  - Micro shock: 25% increase in RWAs by industry (use loans.industry distribution).
  - Market shock: apply 99% SVaR scenario from `market_risk_metrics` and re-run RWA calculation.
  - Combined: liquidity stress (30-day outflow) + credit shock (migration of 10% of B/C ratings to D/E) to measure capital depletion.

## Escalation and Remediation
- Amber breach: CRO to produce remediation plan within 30 calendar days; limit new originations by product types identified in `loans.product_type`.
- Red breach: immediate capital raising or balance sheet actions; Board notification within 3 business days.

## Model and Data Governance
- Document all calculation scripts and SQL used to derive RWA and capital from source tables.
- Maintain versioning for synthetic policy tests and keep the seed (`SEED=42`) to reproduce scenario runs.

## Audit and Reporting
- Provide monthly Capital Adequacy report that includes:
  - Time series of CAR per `as_of_date`
  - Top 20 customers by `ead`
  - RWA and capital by industry and geography (use `loans.industry`, `loans.geography`)

--
This is a synthetic Capital Adequacy Framework mapped to the FakeBank dataset and aligned with APRA-style monitoring for testing and educational use only.
```
Capital Adequacy Framework
1. Purpose

Ensure the bank maintains sufficient capital to absorb unexpected losses and continue operating under stress, in line with regulatory requirements and the bank’s risk appetite.

2. Key Objectives

Regulatory Compliance: Meet or exceed APRA minimum capital requirements (CET1, Tier 1, Total Capital).

Internal Capital Adequacy Assessment: Hold capital consistent with the bank’s risk profile and strategic plan (ICAAP).

Support Growth: Ensure capital is sufficient to fund new lending, trading activity, and business expansion.

Market Confidence: Maintain capital ratios that reassure depositors, counterparties, and rating agencies.

3. Governance
Level	Responsibilities
Board / Risk Committee	Approves capital risk appetite, ICAAP, recovery plan
ALCO / Capital Committee	Reviews capital position, sets buffers, allocates capital
Risk Management	Independent measurement of RWA, stress testing, capital attribution
Finance / Treasury	Manages capital instruments, dividend policy, capital issuance
Internal Audit	Provides assurance over capital adequacy process
4. Regulatory Capital Components
Capital Type	Composition	Purpose
CET1 (Common Equity Tier 1)	Ordinary shares, retained earnings	Primary loss-absorbing capital
Tier 1 Capital	CET1 + Additional Tier 1 instruments (hybrid capital)	Going-concern capital
Total Capital	Tier 1 + Tier 2 instruments (subordinated debt)	Includes gone-concern capital
5. Key Ratios & Minimums
Ratio	Formula	Regulatory Minimum (APRA)
CET1 Ratio	CET1 Capital ÷ RWA	4.5% + capital conservation buffer (typically 10.25% effective minimum for major banks)
Tier 1 Ratio	Tier 1 Capital ÷ RWA	6.0%
Total Capital Ratio	Total Capital ÷ RWA	8.0%
Leverage Ratio	Tier 1 Capital ÷ Total Exposures	≥ 3%

Banks typically hold buffers above minimums to absorb volatility and meet market expectations.

6. Risk-Weighted Assets (RWA)

Capital adequacy depends on RWA, calculated for:

Credit Risk: Standardised or IRB approach (APS 112/113)

Market Risk: Standardised approach or IMA (APS 116)

Operational Risk: Standardised Measurement Approach (SMA)

Interest Rate Risk in Banking Book (IRRBB): APRA capital add-on

Formula:

Capital Ratio
=
Eligible Capital
RWA
Capital Ratio=
RWA
Eligible Capital
	​

7. Capital Planning & ICAAP

A robust Internal Capital Adequacy Assessment Process (ICAAP) includes:

Capital Forecasting: 3–5 year forward-looking projections under baseline and stress scenarios.

Stress Testing: Severe but plausible scenarios (e.g. recession, property price shock, funding stress).

Capital Allocation: Economic capital attribution by business line and risk type.

Recovery Plan: Actions to restore capital if thresholds are breached (e.g., raise equity, cut dividends).

8. Early Warning Triggers

Define trigger levels below Board-approved risk appetite:

Management Buffer Breach: Enhanced monitoring, restrictions on growth.

Recovery Trigger Breach: Activate recovery plan (capital raise, risk-weight optimisation).

Regulatory Minimum Breach: Immediate regulator notification, capital restoration plan.

9. Monitoring & Reporting

Daily/Weekly: CET1 ratio tracking, capital utilisation vs. limits.

Monthly: RWA movements, capital attribution by business.

Quarterly: ICAAP report, stress testing results, Board reporting.

Regulatory: Quarterly APRA ARF_110 returns, annual ICAAP supervisory review (SREP).