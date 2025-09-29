```markdown
# Risk Management Framework

Version: 1.0
Effective Date: 2025-10-01

## Purpose
Provide the consolidated governance and control framework that ties Credit, Market and Liquidity policies into an auditable program mapped to the FakeBank datasets. It defines owners, reporting cadence, and cross-risk escalation.

## Principles
- Data-first measurement: every limit must reference a dataset field and aggregation method.
- Proportional escalation: three-tiered thresholds (Green/Amber/Red) with defined notifications and remediation timelines.
- Reproducibility: calculation scripts and datasets must be version-controlled. Use seeded generator runs for repeatable scenarios.

## Roles & Responsibilities
- Board: approves the overall risk appetite and materially changes limits.
- CRO: operational owner of the RMF and approves escalation recommendations.
- Risk Analytics: computes metrics, runs stress tests, and prepares reports.
- Business Units: operate within limits and deliver remediation when requested.

## Integrated Reporting
- Monthly Integrated Risk Report (per `as_of_date`) to include CAR, credit risk health, market risk positions, liquidity metrics and top concentration exposures.

## Cross-risk Escalation Examples
- Combined stress (market shock causing collateral calls leading to liquidity stress): automatically trigger Capital Adequacy escalation workflow if CAR would fall below Amber in scenario.

## Data & Model Governance
- Version control for generator code, calculation scripts and scenario definitions.
- Unit tests and sample runs with `SEED=42` to validate calculations.

--
This Risk Management Framework is synthetic and intended for testing, analytics and training.
```
```markdown
# Risk Management Framework

Version: 1.0
Effective Date: 2025-10-01

## Purpose
Provide a consolidated framework for identifying, measuring, monitoring and governing material risks (Credit, Market, Liquidity) using the FakeBank synthetic datasets.

## Principles
- Consistent measurement: use `as_of_date` snapshots and agreed definitions (EAD, RWA, VaR, LCR, NSFR).
- Data-driven governance: every threshold and escalation must be measurable using the dataset fields.
- Proportionality and escalation: three-tier thresholds (Green/Amber/Red) with owners and timelines.

## Roles & Responsibilities
- Board: approves risk appetite and material limits.
- CRO: owns RMF and approves remediation.
- Risk Analytics: produces monthly metrics and stress-test packs.
- Business Units: operate within limits and deliver remediation plans when required.

## Integrated Reporting
- Monthly Integrated Risk Report covering CAR, credit portfolio health, market risk exposures and liquidity metrics, all by `as_of_date`.

## Threshold Mapping Examples
- CAR: Green >=12%, Amber 10.5%-12%, Red <10.5%.
- LCR: Green >=115%, Amber 110%-115%, Red <110%.
- Desk VaR: Green <80% of limit, Amber 80%-100%, Red >100%.

## Stress Testing
- Run reverse stress tests and scenario analysis using the synthetic time series across `as_of_date`.

## Data Governance
- Maintain version control for generator, scripts and calculation logic. Use seeded runs (`SEED=42`) for reproducible tests.
- Data quality targets: >99% completeness for mandatory fields, <1% orphan records.

--
This RMF is tailored for use with the FakeBank synthetic datasets for testing, analytics and training.
```
```markdown
# Risk Management Framework

Version: 1.0
Effective Date: 2025-10-01

## Purpose
Provide a consolidated risk management framework that ties together Credit, Market and Liquidity risk policies and maps them to the synthetic dataset for governance, monitoring and testing.

## Principles
- Risk identification: use `customer`, `loans`, `market_positions`, and `liquidity_positions` tables to identify exposures.
- Risk measurement: adopt consistent risk measures (EAD, RWA, VaR, LCR, NSFR) computed from `as_of_date` snapshots.
- Risk governance: define owners (CRO, Head of Credit, Head of Trading, CFO) and reporting cadence.

## Roles and Responsibilities
- Board: approves risk appetite and material limits.
- CRO: overall risk oversight, approves frameworks and escalation thresholds.
- Risk Analytics: compute metrics, run stress tests, and produce monthly reports.
- Business Units: operate within limits, remediate breaches and report exceptions.

## Integrated Reporting
- Produce a monthly Integrated Risk Report that includes:
  - Capital Adequacy time series (see Capital Adequacy Framework)
  - Credit portfolio health: PD migrations, provision coverage, top exposures
  - Market risk: VaR, SVaR, top concentration exposures
  - Liquidity metrics: LCR, NSFR, funding concentration

## Monitoring and Escalation
- Define three-tier thresholds for all major metrics (Green / Amber / Red) with clear actions and owners.
- Example mapping (apply per `as_of_date`):
  - CAR: Green >=12%, Amber 10.5%-12%, Red <10.5%
  - LCR: Green >= 115%, Amber 110%-115%, Red <110%
  - Desk VaR: Green below 80% of limit, Amber 80%-100%, Red >100%

## Stress Testing Program
- Monthly scenario runs using synthetic time series. Include reverse stress testing to identify scenarios that would breach capital or liquidity thresholds.

## Data and Model Governance
- Version control for synthetic data generator and policy calculation scripts.
- Unit tests: create small reproducible test cases against `generate_fakebank_data.py` outputs to validate calculations.

--
This consolidated Risk Management Framework is tailored to the FakeBank synthetic datasets to facilitate governance, analytics and educational exercises.
```
📑 Risk Management Framework
1. Purpose and Scope

This Risk Management Framework (RMF) sets out the principles, structures, and processes by which the Bank identifies, measures, monitors, and manages material risks.
It covers credit risk, market risk, and liquidity risk, with explicit links to data models and measurable metrics. The RMF applies to all business units, desks, products, and geographies (NSW, VIC, QLD, WA, SA, TAS, ACT, NT).

The RMF is aligned with:

APRA Prudential Standards (APS 220 Credit Risk, APS 210 Liquidity, CPS 220 Risk Management)

ASIC guidance on responsible lending and disclosure

Australian Privacy Principles for handling customer data

2. Governance Structure

Board Risk Committee (BRC) – approves risk appetite, reviews breaches, and monitors aggregate risk profile.

Chief Risk Officer (CRO) – owns the RMF, sets policies, and ensures compliance.

Risk Management Function – independent monitoring, model validation, and escalation.

Business Units / Desks – own day-to-day risk taking within approved limits.

Escalation thresholds, breach reporting, and remediation timelines are documented per risk type.

3. Risk Identification & Measurement

Each material risk is identified and linked to measurable metrics:

Risk Type	Primary Metrics	Frequency	Tools
Credit Risk	Credit rating distribution, LGD, EAD, RWA, provision coverage ratio, single-customer exposure, industry/geography/product exposure	Monthly	Credit data mart (loans, write_offs, credit_events)
Market Risk	VaR, SVaR, Expected Shortfall, Volatility, position concentration	Daily	Risk engine with desk/instrument granularity
Liquidity Risk	LCR, NSFR, cash inflows/outflows, funding source concentration, stress outflow coverage	Monthly & Daily (for LCR)	Liquidity dashboard & cashflow forecasting tool
4. Monitoring & Reporting

Credit Risk Reports: Monthly, segmented by geography, industry, customer segment, product.

Market Risk Reports: Daily desk-level VaR/SVaR, escalated intraday if limits breached.

Liquidity Risk Reports: Monthly LCR/NSFR compliance; daily early-warning triggers if LCR < 115%.

All breaches trigger root-cause analysis and are reported to CRO within 24 hours.

5. Stress Testing & Scenario Analysis

Credit Risk: Simulate rating migrations (2–5% migration rate per month) and LGD shocks (up to +20%).

Market Risk: SVaR 99% confidence scenarios, historical replay, and volatility shocks >30%.

Liquidity Risk: 30-day survival horizon under name-specific and market-wide stress.

6. Data & Model Governance

All risk metrics are calculated from auditable, referentially-intact data (per the credit risk data model).

Models for LGD, EAD, and VaR are independently validated annually.

Data quality thresholds: >99% completeness, <1% orphan records.

🎯 Risk Appetite Statement (RAS)

Our risk appetite defines the amount and type of risk the Bank is willing to accept to achieve its strategic objectives, balancing profitability, resilience, and regulatory compliance.

1. Credit Risk Appetite
Metric	Appetite	Escalation Trigger
Maximum Single Customer Exposure	≤ 5% of Total Capital	> 4.5% alerts CRO
Average Credit Rating (Portfolio)	≥ B	10% of loans migrate to C/D/E in 3 months
LGD (Portfolio)	< 40%	LGD rises > 45%
Provision Coverage Ratio	≥ 1.5%	Drops < 1.7%
Industry Concentration	≤ 20% of Total Portfolio per ANZSIC industry	> 18%
Geographic Concentration	≤ 25% per State	> 22%
Product Concentration	≤ 40% per product type	> 38%
2. Market Risk Appetite
Metric	Appetite	Escalation Trigger
Maximum Desk VaR (99%)	≤ AUD 10M	> 90% of limit intraday
SVaR (99%)	≤ AUD 15M	Exceeds limit 3 days in a row
Volatility Threshold	< 20% (desk level)	> 22% sustained
Position Concentration	≤ 10% per instrument	> 9%
3. Liquidity Risk Appetite
Metric	Appetite	Escalation Trigger
Liquidity Coverage Ratio (LCR)	≥ 110%	Drops < 115%
Net Stable Funding Ratio (NSFR)	≥ 105%	Drops < 107%
Maximum Single Funding Source	≤ 20%	> 18%
Stress Scenario Coverage	≥ 30 days	Falls < 35 days
4. Breach Management

Immediate Action: Desk/business head notifies CRO within 1 business day.

Corrective Plan: Documented within 5 business days and approved by CRO.

Board Notification: For material breaches (≥ 120% of limit or repeated breach within 30 days).

5. Linkage to Strategy

This RAS supports the Bank’s strategy of prudent growth by:

Ensuring portfolio credit quality remains ≥ B on average

Maintaining sufficient liquidity buffers to support customer lending even during market stress

Limiting market risk so trading activity does not compromise capital adequacy