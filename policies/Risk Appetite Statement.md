```markdown
# Risk Appetite Statement

Version: 1.0
Effective Date: 2025-10-01

## Overview
This Risk Appetite Statement (RAS) expresses the Bank’s measurable appetite for risk across key dimensions and ties each appetite metric to explicit dataset computations so that breaches are detectible and auditable.

## High-level Appetite Metrics (measurable KPIs)
- Capital: CAR (monthly) Target >=12%, Minimum 10.5%.
- Credit quality: average credit rating (EAD-weighted) Target B or better (avg_score <= 2).
- Provision coverage: >= 1.5% of loan book.
- Liquidity: LCR >= 110%, NSFR >= 105%.
- Market risk: Desk VaR <= AUD 10M; position concentration <= 10% per instrument.
- Concentration metrics: Single customer exposure <= 5% of Capital_total; single funding source <= 20% of funding.

## Appetite by Dimension & Aggregation Rules
- Credit: limits by `industry` and `geography` measured as EAD share of total EAD (soft industry cap 15%, hard cap 20%).
- Liquidity: funding concentration measured as funding source amount / total funding (limit 20%).
- Market: instrument concentration measured as instrument market_value / total desk market_value (limit 10%).

## Monitoring, Escalation & Governance
- Frequency: Monthly (per `as_of_date`) with ad-hoc simulated intraday alerts for early-warning thresholds.
- Any Red breach must be reported to CRO and Board within 24 hours; remediation plan due within 5 business days.

## Review Cycle
- Annual review of RAS or after material changes to business strategy or stress exercises.

--
This RAS is synthetic and intended for testing and demonstration with the FakeBank datasets.
```
