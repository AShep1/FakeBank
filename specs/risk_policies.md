# Risk Policies Specification

## Overview
This document outlines hypothetical bank policies for credit, market, and liquidity risk. It provides a risk framework and metricated risk structures to guide the generation of policy text files.

---

## Credit Risk Policy
- **Risk Framework:**
  - Credit risk is managed through customer due diligence, loan underwriting, and ongoing monitoring.
  - Policies require regular assessment of credit ratings, LGD, EAD, RWA, and capital adequacy.
  - Write-offs and provisions are reviewed monthly.
- **Metricated Structures:**
  - Maximum single customer exposure: 5% of capital
  - Minimum average credit rating: B
  - LGD threshold: < 40%
  - EAD monitored monthly
  - Provision coverage ratio: > 1.5%

## Market Risk Policy
- **Risk Framework:**
  - Market risk is managed through position limits, desk-level controls, and stress testing.
  - Policies require daily monitoring of VaR, SVaR, expected shortfall, and volatility.
  - Market events are tracked and reviewed for impact.
- **Metricated Structures:**
  - Maximum desk VaR: $10M
  - SVaR stress scenario: 99% confidence
  - Volatility threshold: < 20%
  - Position concentration limit: 10% per instrument

## Liquidity Risk Policy
- **Risk Framework:**
  - Liquidity risk is managed through cash flow forecasting, funding source diversification, and stress testing.
  - Policies require monthly monitoring of LCR, NSFR, inflows, and outflows.
  - Liquidity events are tracked and reviewed for impact.
- **Metricated Structures:**
  - Minimum LCR: 110%
  - Minimum NSFR: 105%
  - Maximum single funding source: 20% of total funding
  - Stress scenario outflow coverage: 30 days

---

## Australian Context
- All risk policies should reference APRA and ASIC regulatory requirements.
- Risk frameworks and metrics should align with Australian standards and market practices.
- All monetary values in AUD.
- Compliance with Australian privacy and data protection standards.

## Data Generation Guidance
- Use these policies to generate realistic policy text files for the hypothetical bank.
- Ensure all risk metrics and thresholds are reflected in synthetic data and policy documentation.

---

## Allowed Values for Policy Dimensions

### Credit Rating (Ordered Set)
- Allowed values: [A, B, C, D, E]
- Order: A (highest) to E (lowest)

### Market Risk Metric Type
- Allowed values: [VaR, SVaR, Expected Shortfall, Volatility]

### Liquidity Metric Type
- Allowed values: [LCR, NSFR, Cash Inflows, Cash Outflows]

### Customer Segment
- Allowed values: [Retail, Corporate, SME]

### Geography
- Allowed values: Australian states [NSW, VIC, QLD, WA, SA, TAS, ACT, NT]

---

## Linking Risk Frameworks to Dimensional Values

### Market Risk
- Risk limits and controls should be explicitly linked to dimensional values:
  - **Desk-level limits:** Each desk (e.g., Equities, Fixed Income) must have defined risk limits (e.g., maximum VaR, position size).
  - **Instrument-level limits:** Each instrument within a desk (e.g., ASX Equity, AUD Bond) must have specific limits (e.g., maximum exposure, concentration).
  - **Total market risk limits:** Aggregate limits across all desks and instruments must be set and monitored.
- All risk metrics and policy thresholds should be documented per desk and instrument, with escalation procedures for breaches.

### Credit Risk
- Risk limits and controls should be linked to dimensional values:
  - **Industry limits:** Maximum exposure per industry (ANZSIC code) to avoid concentration risk.
  - **Geography limits:** Maximum exposure per state/region/postcode.
  - **Product and segment limits:** Limits by product type (e.g., mortgage, business loan) and customer segment (retail, SME, corporate).
  - **Total credit risk limits:** Aggregate limits across all dimensions must be set and monitored.
- All credit risk metrics and policy thresholds should be documented per dimension, with escalation procedures for breaches.

---

## Policy Generation Guidelines (Updated)
- Ensure all policy text references only the allowed values and ordered sets listed above.
- Align all risk frameworks and metrics with Australian regulatory standards.
- Document all allowed values in policy generation scripts for consistency.
- Ensure all risk frameworks and policies are explicitly linked to the dimensional values defined in the data models.
- Document desk, instrument, industry, geography, product, and segment limits in policy text and data generation scripts.
- Include escalation and monitoring procedures for breaches of any dimensional limit.
