# Liquidity Risk Data Model

## Overview
This data model covers the liquidity risk domain for a hypothetical bank. It consists of 5 tables, each designed for panel data over 24 months, with an `as_of_date` column for month-end snapshots. Referential integrity is enforced.

## Tables

### 1. liquidity_positions
- **position_id** (PK): Unique position identifier
- **as_of_date**: Month-end date
- **customer_id** (FK): References customers.customer_id
- **asset_type**: Cash, deposit, security, etc.
- **amount**: Amount held
- **maturity_date**: Maturity date (if applicable)

### 2. funding_sources
- **funding_id** (PK): Unique funding identifier
- **as_of_date**: Month-end date
- **source_type**: Interbank, retail, wholesale
- **amount**: Amount sourced
- **cost**: Cost of funds

### 3. liquidity_metrics
- **metric_id** (PK): Unique metric identifier
- **as_of_date**: Month-end date
- **LCR**: Liquidity Coverage Ratio
- **NSFR**: Net Stable Funding Ratio
- **cash_inflows**: Total inflows
- **cash_outflows**: Total outflows


### 4. customers
See [customer.md](./customer.md) for the customer data model. Reference `customer_id` in other tables for referential integrity.

### 5. liquidity_events
- **event_id** (PK): Unique event identifier
- **as_of_date**: Month-end date
- **event_type**: Stress/Withdrawal/Deposit
- **event_details**: Description

## Allowed Values for Dimensional Columns

### Asset Type
- Allowed values: [Cash, Deposit, Security, Government Bond, Corporate Bond]

### Funding Source Type
- Allowed values: [Interbank, Retail, Wholesale]

### Liquidity Metric Type
- Allowed values: [LCR, NSFR, Cash Inflows, Cash Outflows]

### Event Type (Liquidity Events)
- Allowed values: [Stress, Withdrawal, Deposit]

### Customer Segment
- Allowed values: [Retail, Corporate, SME]

### Geography
- Allowed values: Australian states [NSW, VIC, QLD, WA, SA, TAS, ACT, NT]

## Data Population Guidelines
- For each month-end, generate liquidity positions for customers and funding sources.
- Metrics should reflect realistic liquidity ratios and cash flows.
- Events should be plausible and affect liquidity positions.
- Ensure referential integrity between positions and customers.
- Use Faker for names and synthetic data.
- Ensure all dimensional columns use only the allowed values listed above.
- Use realistic Australian asset types and funding sources.
- Document all allowed values in the data generation scripts for consistency.

---

## Australian Context
- All data and scenarios should reflect the Australian banking market.
- Regulatory references: APRA, ASIC.
- Liquidity metrics (LCR, NSFR) should follow APRA standards.
- Funding sources should include Australian interbank, retail, and wholesale markets.
- Customer segments and products should reflect Australian banking practices.
- All monetary values in AUD.
- Compliance with Australian privacy and data protection standards.
