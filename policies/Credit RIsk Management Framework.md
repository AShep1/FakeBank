```markdown
# Credit Risk Management Framework

Version: 1.0
Effective Date: 2025-10-01

## Purpose
Establish the Bank's policy for identification, measurement, monitoring and control of credit risk. All limits and thresholds below are metricated and mapped to dataset columns so calculations are auditable and automatable.

## Scope & Data Sources
Primary tables and fields (examples):
- `data/loans.parquet`: `loan_id`, `customer_id`, `as_of_date`, `ead`, `rwa`, `provisions`, `credit_rating`, `lgd_rating`, `arrears`, `loan_amount`, `industry`, `geography`, `product_type`, `origination_date`, `maturity_date`
- `data/loan_applications.parquet`, `data/write_offs.parquet`, `data/loan_securities.parquet`, `data/credit_events.parquet`.

## Limit Framework (measurable with aggregation rules)
Each limit specifies: metric definition, aggregation method, measurement frequency and escalation triggers.

- Portfolio average credit rating (EAD-weighted):
  - Metric: avg_score = sum(EAD * rating_score) / sum(EAD), mapping A=1..E=5
  - Frequency: Monthly (per `as_of_date`)
  - Appetite: Target <= 2 (B or better). Alert if > 2.2; escalate if > 3.0.

- Provision coverage ratio:
  - Metric: sum(provisions) / sum(expected_losses) (EL derived from PD*LGD*EAD proxies)
  - Appetite: >= 1.5% of loan book. Amber if between 1.2% and 1.5%; Red if < 1.2%.

- Arrears ratio:
  - Metric: sum(arrears) / sum(loan_amount) across portfolio
  - Appetite: escalate if > 5% (portfolio-level). Monitor by product_type and geography.

- Single customer concentration:
  - Metric: exposure_i = sum(EAD) by customer_id; compute concentration = exposure_i / Capital_total
  - Appetite: exposure_i <= 5% of Capital_total. Alert when concentration > 90% of limit (4.5%).

- Industry / Geography concentration:
  - Metric: EAD aggregated by `industry` or `geography` divided by total EAD
  - Appetite: soft limit 15% per industry, hard review at 20%; geography soft limit 20%, hard trigger 25%.

## Monitoring, Reporting & Frequency
- Frequency: Monthly (per `as_of_date`) unless otherwise noted.
- Required reports:
  - Credit portfolio dashboard (EAD, RWA, provisions, avg credit rating, LGD distribution, arrears, PD migrations)
  - Concentration roll-up by customer, industry, geography, product_type
  - Top 20 EAD exposures and write-off drivers
- Owners: Head of Credit (operational), Risk Analytics (calculations), CRO (oversight).

## Escalation Framework (actions & timelines)
- Green → Amber (example: PD migration > 2% or provisioning ratio slips into Amber):
  - Notification: Head of Credit, Risk Analytics within 2 business days
  - Action: Produce remediation plan in 15 business days; restrict discretionary new originations in affected segment

- Amber → Red (example: provision coverage < 1.2% or single customer exposure > 5%):
  - Notification: CRO, CFO, CEO and Board Risk Committee immediately (within 1 business day)
  - Action: Immediate remediation steps (restrict origination, raise additional provisions, seek capital actions), Board briefing within 3 business days

## Stress Testing & Validation
- Monthly stress runsets: migration shocks (10% B/C->D/E), LGD uplift ( +20pp ), and idiosyncratic industry shocks. Measure impact on provisions, CAR and capital needs.
- Backtesting: compare predicted PDs and LGDs to realized defaults and write-offs over rolling 12-month windows.

## Data Quality & Governance
- Mandatory fields for credit metrics: `loan_id`, `customer_id`, `as_of_date`, `ead`, `rwa`, `credit_rating`, `lgd_rating`, `provisions`, `arrears`, `loan_amount`.
- Data checks at each run: completeness (>99%), referential integrity (no orphan FK), null rate thresholds (<1% for critical numeric fields).

--
This Credit Risk Management Framework is synthetic and intended for testing, analytics and training using the FakeBank datasets.
```
```markdown
# Credit Risk Management Framework

Version: 1.0
Effective Date: 2025-10-01

## Purpose
Establish the Bank's policy for identification, measurement, monitoring and control of credit risk. All limits and thresholds below are metricated and mapped to dataset columns so calculations are auditable and automatable.

## Scope & Data Sources
Primary tables and fields (examples):
- `data/loans.parquet`: `loan_id`, `customer_id`, `as_of_date`, `ead`, `rwa`, `provisions`, `credit_rating`, `lgd_rating`, `arrears`, `loan_amount`, `industry`, `geography`, `product_type`, `origination_date`, `maturity_date`
- `data/loan_applications.parquet`, `data/write_offs.parquet`, `data/loan_securities.parquet`, `data/credit_events.parquet`.

## Limit Framework (measurable with aggregation rules)
Each limit specifies: metric definition, aggregation method, measurement frequency and escalation triggers.

- Portfolio average credit rating (EAD-weighted):
  - Metric: avg_score = sum(EAD * rating_score) / sum(EAD), mapping A=1..E=5
  - Frequency: Monthly (per `as_of_date`)
  - Appetite: Target <= 2 (B or better). Alert if > 2.2; escalate if > 3.0.

- Provision coverage ratio:
  - Metric: sum(provisions) / sum(expected_losses) (EL derived from PD*LGD*EAD proxies)
  - Appetite: >= 1.5% of loan book. Amber if between 1.2% and 1.5%; Red if < 1.2%.

- Arrears ratio:
  - Metric: sum(arrears) / sum(loan_amount) across portfolio
  - Appetite: escalate if > 5% (portfolio-level). Monitor by product_type and geography.

- Single customer concentration:
  - Metric: exposure_i = sum(EAD) by customer_id; compute concentration = exposure_i / Capital_total
  - Appetite: exposure_i <= 5% of Capital_total. Alert when concentration > 90% of limit (4.5%).

- Industry / Geography concentration:
  - Metric: EAD aggregated by `industry` or `geography` divided by total EAD
  - Appetite: soft limit 15% per industry, hard review at 20%; geography soft limit 20%, hard trigger 25%.

## Monitoring, Reporting & Frequency
- Frequency: Monthly (per `as_of_date`) unless otherwise noted.
- Required reports:
  - Credit portfolio dashboard (EAD, RWA, provisions, avg credit rating, LGD distribution, arrears, PD migrations)
  - Concentration roll-up by customer, industry, geography, product_type
  - Top 20 EAD exposures and write-off drivers
- Owners: Head of Credit (operational), Risk Analytics (calculations), CRO (oversight).

## Escalation Framework (actions & timelines)
- Green → Amber (example: PD migration > 2% or provisioning ratio slips into Amber):
  - Notification: Head of Credit, Risk Analytics within 2 business days
  - Action: Produce remediation plan in 15 business days; restrict discretionary new originations in affected segment

- Amber → Red (example: provision coverage < 1.2% or single customer exposure > 5%):
  - Notification: CRO, CFO, CEO and Board Risk Committee immediately (within 1 business day)
  - Action: Immediate remediation steps (restrict origination, raise additional provisions, seek capital actions), Board briefing within 3 business days

## Stress Testing & Validation
- Monthly stress runsets: migration shocks (10% B/C->D/E), LGD uplift ( +20pp ), and idiosyncratic industry shocks. Measure impact on provisions, CAR and capital needs.
- Backtesting: compare predicted PDs and LGDs to realized defaults and write-offs over rolling 12-month windows.

## Data Quality & Governance
- Mandatory fields for credit metrics: `loan_id`, `customer_id`, `as_of_date`, `ead`, `rwa`, `credit_rating`, `lgd_rating`, `provisions`, `arrears`, `loan_amount`.
- Data checks at each run: completeness (>99%), referential integrity (no orphan FK), null rate thresholds (<1% for critical numeric fields).

--
This Credit Risk Management Framework is synthetic and intended for testing, analytics and training using the FakeBank datasets.
```
```markdown
# Credit Risk Management Framework

Version: 1.0
Effective Date: 2025-10-01

## Purpose
Establish the Bank's policy for identification, measurement, monitoring and control of credit risk. All limits and thresholds below are metricated and mapped to dataset columns so calculations are auditable and automatable.

## Scope & Data Sources
Primary tables and fields (examples):
- `data/loans.parquet`: `loan_id`, `customer_id`, `as_of_date`, `ead`, `rwa`, `provisions`, `credit_rating`, `lgd_rating`, `arrears`, `loan_amount`, `industry`, `geography`, `product_type`, `origination_date`, `maturity_date`
- `data/loan_applications.parquet`, `data/write_offs.parquet`, `data/loan_securities.parquet`, `data/credit_events.parquet`.

## Limit Framework (measurable with aggregation rules)
Each limit specifies: metric definition, aggregation method, measurement frequency and escalation triggers.

- Portfolio average credit rating (EAD-weighted):
  - Metric: avg_score = sum(EAD * rating_score) / sum(EAD), mapping A=1..E=5
  - Frequency: Monthly (per `as_of_date`)
  - Appetite: Target <= 2 (B or better). Alert if > 2.2; escalate if > 3.0.

- Provision coverage ratio:
  - Metric: sum(provisions) / sum(expected_losses) (EL derived from PD*LGD*EAD proxies)
  - Appetite: >= 1.5% of loan book. Amber if between 1.2% and 1.5%; Red if < 1.2%.

- Arrears ratio:
  - Metric: sum(arrears) / sum(loan_amount) across portfolio
  - Appetite: escalate if > 5% (portfolio-level). Monitor by product_type and geography.

- Single customer concentration:
  - Metric: exposure_i = sum(EAD) by customer_id; compute concentration = exposure_i / Capital_total
  - Appetite: exposure_i <= 5% of Capital_total. Alert when concentration > 90% of limit (4.5%).

- Industry / Geography concentration:
  - Metric: EAD aggregated by `industry` or `geography` divided by total EAD
  - Appetite: soft limit 15% per industry, hard review at 20%; geography soft limit 20%, hard trigger 25%.

## Monitoring, Reporting & Frequency
- Frequency: Monthly (per `as_of_date`) unless otherwise noted.
- Required reports:
  - Credit portfolio dashboard (EAD, RWA, provisions, avg credit rating, LGD distribution, arrears, PD migrations)
  - Concentration roll-up by customer, industry, geography, product_type
  - Top 20 EAD exposures and write-off drivers
- Owners: Head of Credit (operational), Risk Analytics (calculations), CRO (oversight).

## Escalation Framework (actions & timelines)
- Green → Amber (example: PD migration > 2% or provisioning ratio slips into Amber):
  - Notification: Head of Credit, Risk Analytics within 2 business days
  - Action: Produce remediation plan in 15 business days; restrict discretionary new originations in affected segment

- Amber → Red (example: provision coverage < 1.2% or single customer exposure > 5%):
  - Notification: CRO, CFO, CEO and Board Risk Committee immediately (within 1 business day)
  - Action: Immediate remediation steps (restrict origination, raise additional provisions, seek capital actions), Board briefing within 3 business days

## Stress Testing & Validation
- Monthly stress runsets: migration shocks (10% B/C->D/E), LGD uplift ( +20pp ), and idiosyncratic industry shocks. Measure impact on provisions, CAR and capital needs.
- Backtesting: compare predicted PDs and LGDs to realized defaults and write-offs over rolling 12-month windows.

## Data Quality & Governance
- Mandatory fields for credit metrics: `loan_id`, `customer_id`, `as_of_date`, `ead`, `rwa`, `credit_rating`, `lgd_rating`, `provisions`, `arrears`, `loan_amount`.
- Data checks at each run: completeness (>99%), referential integrity (no orphan FK), null rate thresholds (<1% for critical numeric fields).

--
This Credit Risk Management Framework is synthetic and intended for testing, analytics and training using the FakeBank datasets.
```
```markdown
# Credit Risk Management Framework

Version: 1.0
Effective Date: 2025-10-01

## Purpose
This framework defines how credit risk is identified, measured, controlled and governed using the FakeBank synthetic dataset. It maps policy metrics to data columns so metrics are directly computable from `data/` outputs.

## Scope
Applies to all credit exposures captured in:
- `data/loans.parquet` (key fields: `loan_id`, `customer_id`, `as_of_date`, `ead`, `rwa`, `provisions`, `credit_rating`, `lgd_rating`, `arrears`, `loan_amount`, `industry`, `geography`, `product_type`)
- `data/loan_applications.parquet`, `data/write_offs.parquet`, `data/loan_securities.parquet`, `data/credit_events.parquet`.

## Key Risk Metrics (measurable)
- Portfolio average credit rating (EAD-weighted) — compute by mapping {A:1,B:2,C:3,D:4,E:5} and aggregating: avg_score = sum(EAD*score)/sum(EAD). Target <= 2 (B or better).
- Provision coverage ratio = sum(provisions) / sum(expected_losses) — target >= 1.5% (report monthly by `as_of_date`).
- LGD concentration: flag exposures where `lgd_rating` == 'High' or implied LGD > 40%.
- Arrears ratio = sum(arrears) / sum(loan_amount) — escalate if portfolio-level ratio > 5%.
- PD migration rate = percent of loans that downgrade month-on-month (based on `credit_rating`) — escalate if downgrade rate > 2% in a month for aggregated portfolios.

## Concentration Limits (metricated)
- Single customer exposure: max(sum(ead) by customer_id) <= 5% of BankCapital (BankCapital sourced from `Capital Adequacy Framework` calculations). Alert if >4.5%.
- Industry exposure (ANZSIC): soft limit 15% of total EAD per industry; hard review trigger at 20%.
- Geography limit: soft limit 20% of total EAD in any one state; hard trigger 25%.

## Underwriting & Origination Controls
- Approval quality: monitor `loan_applications.status` by `product_type` and `sales_channel`. Trigger investigation if approval rate increases >10% month-on-month for any segment.
- Origination PD backtest: compare predicted origination PD proxy to observed defaults / downgrades over a 12-month rolling window.

## Collateral & Recovery
- Reconciling `loan_securities` to `loans` monthly. Compute Loan-to-Value (LTV) where `security_value` exists; flag residential mortgages with LTV > 90%.
- Prioritise recoveries by `lien_type` (First Lien preferred) and record write-off drivers from `write_offs` table.

## Monitoring, Reporting & Frequency
- Frequency: Monthly (aligned to `as_of_date`). Key outputs:
  - Credit portfolio dashboard: EAD, RWA, provisions, avg credit rating, LGD distribution, arrears, PD migrations.
  - Top 20 customers by EAD and top industries/geographies by exposure.
- Owner: Head of Credit (operational), CRO (oversight). Risk Analytics produces report and maintains code used for calculations.

## Escalation & Remediation
- Early Warning: PD migration > 2% or arrears ratio increase >50% vs prior month — require remediation plan within 15 business days.
- Material Breach: Provision coverage ratio < 1.5% or single customer exposure > 5% of capital — immediate escalation to CRO and Board notification within 3 business days.

## Data Quality & Validation
- Mandatory fields: `loan_id`, `customer_id`, `as_of_date`, `ead`, `rwa`, `credit_rating`, `lgd_rating`, `provisions`, `arrears`.
- Monthly reconciliation: row counts, null checks, FK integrity (no orphan `loan_id` or `customer_id`). Seeded generator (`SEED=42`) used to reproduce test cases.

## Stress Testing & Scenario Examples
- Industry shock: increase default rates for one industry by +10 percentage points, recalculate provisions and capital impact.
- Migration shock: force 10% of B/C ratings to downgrade to D/E and measure provision and CAR impact.

## Example SQL / pandas snippets (reference)
- EAD-weighted average rating (pandas):

  ratings_map = {'A':1,'B':2,'C':3,'D':4,'E':5}
  loans['rating_score'] = loans['credit_rating'].map(ratings_map)
  avg_score = (loans['ead'] * loans['rating_score']).sum() / loans['ead'].sum()

--
This document is a synthetic credit risk framework intended for testing and demonstration with the FakeBank dataset.
```
```markdown
# Credit Risk Management Framework

Version: 1.0
Effective Date: 2025-10-01

## Purpose
This framework defines how credit risk is identified, measured, controlled and governed using the FakeBank synthetic dataset. It maps policy metrics to data columns so metrics are directly computable from `data/` outputs.

## Scope
Applies to all credit exposures captured in:
- `data/loans.parquet` (key fields: `loan_id`, `customer_id`, `as_of_date`, `ead`, `rwa`, `provisions`, `credit_rating`, `lgd_rating`, `arrears`, `loan_amount`, `industry`, `geography`, `product_type`)
- `data/loan_applications.parquet`, `data/write_offs.parquet`, `data/loan_securities.parquet`, `data/credit_events.parquet`.

## Key Risk Metrics (measurable)
- Portfolio average credit rating (EAD-weighted) — compute by mapping {A:1,B:2,C:3,D:4,E:5} and aggregating: avg_score = sum(EAD*score)/sum(EAD). Target <= 2 (B or better).
- Provision coverage ratio = sum(provisions) / sum(expected_losses) — target >= 1.5% (report monthly by `as_of_date`).
- LGD concentration: flag exposures where `lgd_rating` == 'High' or implied LGD > 40%.
- Arrears ratio = sum(arrears) / sum(loan_amount) — escalate if portfolio-level ratio > 5%.
- PD migration rate = percent of loans that downgrade month-on-month (based on `credit_rating`) — escalate if downgrade rate > 2% in a month for aggregated portfolios.

## Concentration Limits (metricated)
- Single customer exposure: max(sum(ead) by customer_id) <= 5% of BankCapital (BankCapital sourced from `Capital Adequacy Framework` calculations). Alert if >4.5%.
- Industry exposure (ANZSIC): soft limit 15% of total EAD per industry; hard review trigger at 20%.
- Geography limit: soft limit 20% of total EAD in any one state; hard trigger 25%.

## Underwriting & Origination Controls
- Approval quality: monitor `loan_applications.status` by `product_type` and `sales_channel`. Trigger investigation if approval rate increases >10% month-on-month for any segment.
- Origination PD backtest: compare predicted origination PD proxy to observed defaults / downgrades over a 12-month rolling window.

## Collateral & Recovery
- Reconciling `loan_securities` to `loans` monthly. Compute Loan-to-Value (LTV) where `security_value` exists; flag residential mortgages with LTV > 90%.
- Prioritise recoveries by `lien_type` (First Lien preferred) and record write-off drivers from `write_offs` table.

## Monitoring, Reporting & Frequency
- Frequency: Monthly (aligned to `as_of_date`). Key outputs:
  - Credit portfolio dashboard: EAD, RWA, provisions, avg credit rating, LGD distribution, arrears, PD migrations.
  - Top 20 customers by EAD and top industries/geographies by exposure.
- Owner: Head of Credit (operational), CRO (oversight). Risk Analytics produces report and maintains code used for calculations.

## Escalation & Remediation
- Early Warning: PD migration > 2% or arrears ratio increase >50% vs prior month — require remediation plan within 15 business days.
- Material Breach: Provision coverage ratio < 1.5% or single customer exposure > 5% of capital — immediate escalation to CRO and Board notification within 3 business days.

## Data Quality & Validation
- Mandatory fields: `loan_id`, `customer_id`, `as_of_date`, `ead`, `rwa`, `credit_rating`, `lgd_rating`, `provisions`, `arrears`.
- Monthly reconciliation: row counts, null checks, FK integrity (no orphan `loan_id` or `customer_id`). Seeded generator (`SEED=42`) used to reproduce test cases.

## Stress Testing & Scenario Examples
- Industry shock: increase default rates for one industry by +10 percentage points, recalculate provisions and capital impact.
- Migration shock: force 10% of B/C ratings to downgrade to D/E and measure provision and CAR impact.

## Example SQL / pandas snippets (reference)
- EAD-weighted average rating (pandas):

  ratings_map = {'A':1,'B':2,'C':3,'D':4,'E':5}
  loans['rating_score'] = loans['credit_rating'].map(ratings_map)
  avg_score = (loans['ead'] * loans['rating_score']).sum() / loans['ead'].sum()

--
This document is a synthetic credit risk framework intended for testing and demonstration with the FakeBank dataset.
```
```markdown
# Credit Risk Management Framework

Version: 1.0
Effective Date: 2025-10-01

## Purpose
This framework defines how credit risk is identified, measured, controlled and governed using the FakeBank synthetic dataset. It maps policy metrics to data columns so metrics are directly computable from `data/` outputs.

## Scope
Applies to all credit exposures captured in:
- `data/loans.parquet` (key fields: `loan_id`, `customer_id`, `as_of_date`, `ead`, `rwa`, `provisions`, `credit_rating`, `lgd_rating`, `arrears`, `loan_amount`, `industry`, `geography`, `product_type`)
- `data/loan_applications.parquet`, `data/write_offs.parquet`, `data/loan_securities.parquet`, `data/credit_events.parquet`.

## Key Risk Metrics (measurable)
- Portfolio average credit rating (EAD-weighted) — compute by mapping {A:1,B:2,C:3,D:4,E:5} and aggregating: avg_score = sum(EAD*score)/sum(EAD). Target <= 2 (B or better).
- Provision coverage ratio = sum(provisions) / sum(expected_losses) — target >= 1.5% (report monthly by `as_of_date`).
- LGD concentration: flag exposures where `lgd_rating` == 'High' or implied LGD > 40%.
- Arrears ratio = sum(arrears) / sum(loan_amount) — escalate if portfolio-level ratio > 5%.
- PD migration rate = percent of loans that downgrade month-on-month (based on `credit_rating`) — escalate if downgrade rate > 2% in a month for aggregated portfolios.

## Concentration Limits (metricated)
- Single customer exposure: max(sum(ead) by customer_id) <= 5% of BankCapital (BankCapital sourced from `Capital Adequacy Framework` calculations). Alert if >4.5%.
- Industry exposure (ANZSIC): soft limit 15% of total EAD per industry; hard review trigger at 20%.
- Geography limit: soft limit 20% of total EAD in any one state; hard trigger 25%.

## Underwriting & Origination Controls
- Approval quality: monitor `loan_applications.status` by `product_type` and `sales_channel`. Trigger investigation if approval rate increases >10% month-on-month for any segment.
- Origination PD backtest: compare predicted origination PD proxy to observed defaults / downgrades over a 12-month rolling window.

## Collateral & Recovery
- Reconciling `loan_securities` to `loans` monthly. Compute Loan-to-Value (LTV) where `security_value` exists; flag residential mortgages with LTV > 90%.
- Prioritise recoveries by `lien_type` (First Lien preferred) and record write-off drivers from `write_offs` table.

## Monitoring, Reporting & Frequency
- Frequency: Monthly (aligned to `as_of_date`). Key outputs:
  - Credit portfolio dashboard: EAD, RWA, provisions, avg credit rating, LGD distribution, arrears, PD migrations.
  - Top 20 customers by EAD and top industries/geographies by exposure.
- Owner: Head of Credit (operational), CRO (oversight). Risk Analytics produces report and maintains code used for calculations.

## Escalation & Remediation
- Early Warning: PD migration > 2% or arrears ratio increase >50% vs prior month — require remediation plan within 15 business days.
- Material Breach: Provision coverage ratio < 1.5% or single customer exposure > 5% of capital — immediate escalation to CRO and Board notification within 3 business days.

## Data Quality & Validation
- Mandatory fields: `loan_id`, `customer_id`, `as_of_date`, `ead`, `rwa`, `credit_rating`, `lgd_rating`, `provisions`, `arrears`.
- Monthly reconciliation: row counts, null checks, FK integrity (no orphan `loan_id` or `customer_id`). Seeded generator (`SEED=42`) used to reproduce test cases.

## Stress Testing & Scenario Examples
- Industry shock: increase default rates for one industry by +10 percentage points, recalculate provisions and capital impact.
- Migration shock: force 10% of B/C ratings to downgrade to D/E and measure provision and CAR impact.

## Example SQL / pandas snippets (reference)
- EAD-weighted average rating (pandas):

  ratings_map = {'A':1,'B':2,'C':3,'D':4,'E':5}
  loans['rating_score'] = loans['credit_rating'].map(ratings_map)
  avg_score = (loans['ead'] * loans['rating_score']).sum() / loans['ead'].sum()

--
This document is a synthetic credit risk framework intended for testing and demonstration with the FakeBank dataset.
```
```markdown
# Credit Risk Management Framework

Version: 1.0
Effective Date: 2025-10-01

## Purpose
This framework defines how credit risk is identified, measured, controlled and governed using the FakeBank synthetic dataset. It maps policy metrics to data columns so metrics are directly computable from `data/` outputs.

## Scope
Applies to all credit exposures captured in:
- `data/loans.parquet` (key fields: `loan_id`, `customer_id`, `as_of_date`, `ead`, `rwa`, `provisions`, `credit_rating`, `lgd_rating`, `arrears`, `loan_amount`, `industry`, `geography`, `product_type`)
- `data/loan_applications.parquet`, `data/write_offs.parquet`, `data/loan_securities.parquet`, `data/credit_events.parquet`.

## Key Risk Metrics (measurable)
- Portfolio average credit rating (EAD-weighted) — compute by mapping {A:1,B:2,C:3,D:4,E:5} and aggregating: avg_score = sum(EAD*score)/sum(EAD). Target <= 2 (B or better).
- Provision coverage ratio = sum(provisions) / sum(expected_losses) — target >= 1.5% (report monthly by `as_of_date`).
- LGD concentration: flag exposures where `lgd_rating` == 'High' or implied LGD > 40%.
- Arrears ratio = sum(arrears) / sum(loan_amount) — escalate if portfolio-level ratio > 5%.
- PD migration rate = percent of loans that downgrade month-on-month (based on `credit_rating`) — escalate if downgrade rate > 2% in a month for aggregated portfolios.

## Concentration Limits (metricated)
- Single customer exposure: max(sum(ead) by customer_id) <= 5% of BankCapital (BankCapital sourced from `Capital Adequacy Framework` calculations). Alert if >4.5%.
- Industry exposure (ANZSIC): soft limit 15% of total EAD per industry; hard review trigger at 20%.
- Geography limit: soft limit 20% of total EAD in any one state; hard trigger 25%.

## Underwriting & Origination Controls
- Approval quality: monitor `loan_applications.status` by `product_type` and `sales_channel`. Trigger investigation if approval rate increases >10% month-on-month for any segment.
- Origination PD backtest: compare predicted origination PD proxy to observed defaults / downgrades over a 12-month rolling window.

## Collateral & Recovery
- Reconciling `loan_securities` to `loans` monthly. Compute Loan-to-Value (LTV) where `security_value` exists; flag residential mortgages with LTV > 90%.
- Prioritise recoveries by `lien_type` (First Lien preferred) and record write-off drivers from `write_offs` table.

## Monitoring, Reporting & Frequency
- Frequency: Monthly (aligned to `as_of_date`). Key outputs:
  - Credit portfolio dashboard: EAD, RWA, provisions, avg credit rating, LGD distribution, arrears, PD migrations.
  - Top 20 customers by EAD and top industries/geographies by exposure.
- Owner: Head of Credit (operational), CRO (oversight). Risk Analytics produces report and maintains code used for calculations.

## Escalation & Remediation
- Early Warning: PD migration > 2% or arrears ratio increase >50% vs prior month — require remediation plan within 15 business days.
- Material Breach: Provision coverage ratio < 1.5% or single customer exposure > 5% of capital — immediate escalation to CRO and Board notification within 3 business days.

## Data Quality & Validation
- Mandatory fields: `loan_id`, `customer_id`, `as_of_date`, `ead`, `rwa`, `credit_rating`, `lgd_rating`, `provisions`, `arrears`.
- Monthly reconciliation: row counts, null checks, FK integrity (no orphan `loan_id` or `customer_id`). Seeded generator (`SEED=42`) used to reproduce test cases.

## Stress Testing & Scenario Examples
- Industry shock: increase default rates for one industry by +10 percentage points, recalculate provisions and capital impact.
- Migration shock: force 10% of B/C ratings to downgrade to D/E and measure provision and CAR impact.

## Example SQL / pandas snippets (reference)
- EAD-weighted average rating (pandas):

  ratings_map = {'A':1,'B':2,'C':3,'D':4,'E':5}
  loans['rating_score'] = loans['credit_rating'].map(ratings_map)
  avg_score = (loans['ead'] * loans['rating_score']).sum() / loans['ead'].sum()

--
This document is a synthetic credit risk framework intended for testing and demonstration with the FakeBank dataset.
```
```markdown
# Credit Risk Management Framework

Version: 1.0
Effective Date: 2025-10-01

## Purpose
Define how credit risk is measured, controlled and governed using the synthetic dataset. The framework maps policy metrics to the `specs/credit_risk.md` data model and `data/` outputs.

## Scope
Applies to all credit exposures captured in `data/loans.parquet`, `data/loan_applications.parquet`, `data/write_offs.parquet`, `data/loan_securities.parquet`, and `data/credit_events.parquet`.

## Key Metrics and Limits
- Minimum average credit rating: B (compute average over exposures weighted by `ead` for each `as_of_date`).
- Provision coverage ratio: provisions / (expected_losses) — internal threshold > 1.5% of total loan book. Use `loans.provisions` and EAD-derived EL.
- LGD threshold: monitor exposures where `lgd_rating` == High and flag where implied LGD > 40%.
- Arrears monitoring: track `loans.arrears` by `as_of_date`. Trigger when arrears / loan_amount > 0.05 (5%) for portfolios.
- PD migration: monitor monthly migration rates (percent of loans changing `credit_rating`) and escalate if downgrade rate > 2% month-on-month for aggregated portfolios.

## Concentration Limits
- Single customer exposure: <= 5% of BankCapital (see Capital Adequacy Framework). Use `loans.ead` aggregated by `customer_id` and `as_of_date`.
- Industry exposure limits: set soft limits per ANZSIC industry (example soft limit 15% of total EAD by industry). Monitor by `loans.industry`.
- Geography limits: set soft limits per state (example soft limit 20% of EAD in any single state). Monitor by `loans.geography`.

## Underwriting and Origination Controls
- Application acceptance rates: monitor `loan_applications.status` by product type and sales channel. Flag unusual approval rate increases (>10% month-on-month) as potential quality degradation.
- Back-testing of credit scoring: simulate scoring drift by comparing origination PD proxies to realized performance over a 12-month lookback.

## Monitoring and Reporting
- Frequency: Monthly by `as_of_date`. Key reports:
  - Credit portfolio dashboard: EAD, RWA, provisions, average credit rating, LGD distribution, arrears, PD migrations.
  - Top contributors to EL (expected loss) by `customer_id`, `industry`, `geography`, `product_type`.
- Ownership: Head of Credit is responsible for monthly reports; Risk Analytics produces the metrics.

## Remediation and Escalation
- Early Warning: If PD migration > 2% (downgrade bias) or arrears ratio increases > 50% vs prior month, restrict new originations in affected product segments; require remediation plan within 15 business days.
- Significant deterioration: Provision coverage ratio < 1.5% or concentration breaches (single customer >5% of capital) escalate to CRO and Board.

## Collateral and Security Management
- Validate `loan_securities` linkage to `loans` and monitor Loan-to-Value (LTV) where `security_value` is available: flag LTV > 90% for residential mortgages.
- Lien position: prioritize recovery strategies based on `lien_type` (First Lien preferred).

## Data Quality and Governance
- Mandatory fields: `loan_id`, `customer_id`, `as_of_date`, `ead`, `rwa`, `credit_rating`, `lgd_rating`, `provisions`, `arrears`.
- Monthly reconciliation: compare row counts by `as_of_date`, null checks, and ensure no orphan foreign keys.

## Testing and Validation
- Backtest loss-given-default assumptions using generated `write_offs` and `credit_events` over the 24-month synthetic window.
- Sensitivity: apply stress scenarios (10% downgrade of B->D in specified industries) and measure provisioning impact.

## Implementation Notes (Mapping to Dataset)
- Average credit rating calculation example (weighted by EAD):

  - avg_rating_score = sum(EAD * rating_score) / sum(EAD)
  - map ratings to scores (A=1, B=2, C=3, D=4, E=5) and invert if needed for interpretation.

--
This Credit Risk Management Framework is synthetic and intended for testing, analytics, and demonstration with the FakeBank dataset. It intentionally references concrete fields to make policy testing straightforward.
```
📑 Credit Risk Management Framework
1. Purpose and Scope

This framework defines how the Bank identifies, measures, monitors, and manages credit risk — the risk of loss due to a counterparty failing to meet its contractual obligations.
It applies to all portfolios, including Retail, SME, and Corporate, and covers all Australian geographies (NSW, VIC, QLD, WA, SA, TAS, ACT, NT).

The framework aligns with:

APRA APS 220 (Credit Risk Management)

APRA CPS 220 (Risk Management)

ASIC responsible lending obligations

Australian Privacy Principles for customer data

2. Governance Structure

Board Risk Committee (BRC): Approves credit risk appetite, reviews portfolio trends, and concentration exposures quarterly.

CRO: Accountable for credit risk policy, monitoring, and escalation.

Credit Risk Function: Owns risk measurement (ratings, LGD, EAD, RWA) and independent review of underwriting standards.

Business Units: Own origination, servicing, and monitoring within approved limits.

3. Credit Risk Identification & Measurement
Core Risk Metrics
Metric	Definition	Frequency
Credit Rating Distribution	% of exposures in A/B/C/D/E	Monthly
LGD	Expected loss severity given default	Monthly
EAD	Total exposure at default	Monthly
RWA	Risk-weighted assets under APS 112	Monthly
Capital Allocation	Regulatory capital allocated to credit	Monthly
Provision Coverage Ratio	Provisions ÷ total loans	Monthly
Arrears	% loans > 30/90 days past due	Monthly
Concentration Risk Metrics

Concentration risk is measured along the following dimensions using Herfindahl-Hirschman Index (HHI) or exposure percentages:

Dimension	Metric	Limit
Single Customer	Exposure ÷ Total Capital	≤ 5%
Industry (ANZSIC)	Max exposure per industry	≤ 20%
Geography	Max exposure per state	≤ 25%
Product Type	Max exposure per product type	≤ 40%
Customer Segment	Max exposure per segment (Retail, SME, Corporate)	≤ 50%

Breaches are escalated and require CRO review and portfolio action (e.g., restrict new lending in breached dimension).

4. Monitoring & Reporting

Monthly Credit Risk Dashboard: Credit rating distribution, LGD trend, EAD growth, provision coverage, and arrears segmented by industry, geography, product, and segment.

Quarterly Concentration Review: Top 10 industries, geographies, and customers by exposure; HHI trend analysis.

Early Warning Triggers: Alerts generated if exposures exceed 90% of dimensional limits.