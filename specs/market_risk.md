# Market Risk Data Model

## Overview
This data model covers the market risk domain for a hypothetical bank. It consists of 5 tables, each designed for panel data over 24 months, with an `as_of_date` column for month-end snapshots. Referential integrity is enforced.

## Tables

### 1. market_positions
- **position_id** (PK): Unique position identifier
- **as_of_date**: Month-end date
- **desk**: Trading desk name
- **instrument**: Instrument type (bond, equity, FX, etc.)
- **notional**: Notional value
- **market_value**: Market value
- **customer_id** (FK): References customers.customer_id

### 2. market_risk_metrics
- **metric_id** (PK): Unique metric identifier
- **position_id** (FK): References market_positions.position_id
- **as_of_date**: Month-end date
- **VaR**: Value at Risk
- **SVaR**: Stressed Value at Risk
- **expected_shortfall**: Expected Shortfall
- **volatility**: Volatility measure

### 3. instrument_prices
- **price_id** (PK): Unique price identifier
- **instrument**: Instrument type
- **as_of_date**: Month-end date
- **price**: Closing price
- **currency**: Currency code


### 4. customers
See [customer.md](./customer.md) for the customer data model. Reference `customer_id` in other tables for referential integrity.

### 5. market_events
- **event_id** (PK): Unique event identifier
- **as_of_date**: Month-end date
- **instrument**: Instrument type
- **event_type**: Shock/News/Regulatory
- **event_details**: Description

## Allowed Values for Dimensional Columns

### Desk
- Allowed values: [Equities, Fixed Income, FX, Commodities, Derivatives]

### Instrument
- Allowed values: [ASX Equity, AUD Bond, FX Pair, Commodity, Derivative]

### Market Risk Metric Type
- Allowed values: [VaR, SVaR, Expected Shortfall, Volatility]

### Currency
- Allowed values: [AUD] (default), [USD, EUR, GBP, NZD]

### Event Type (Market Events)
- Allowed values: [Shock, News, Regulatory]

### Customer Segment
- Allowed values: [Retail, Corporate, SME]

### Geography
- Allowed values: Australian states [NSW, VIC, QLD, WA, SA, TAS, ACT, NT]

## Data Population Guidelines
- For each month-end, generate market positions and metrics for a diverse set of instruments and customers.
- Prices should change realistically month-to-month, with some instruments showing volatility.
- Market events should be plausible and affect relevant instruments.
- Ensure referential integrity between positions, metrics, and customers.
- Use Faker for names and synthetic data.
- Ensure all dimensional columns use only the allowed values listed above.
- Use realistic Australian market instruments and desk structures.
- Document all allowed values in the data generation scripts for consistency.

---

## Australian Context
- All data and scenarios should reflect the Australian financial market.
- Regulatory references: APRA, ASIC.
- Market risk metrics (VaR, SVaR, etc.) should follow APRA standards.
- Instruments should include those common in Australia (ASX equities, AUD bonds, FX pairs relevant to AUD).
- Desk and position structures should reflect Australian trading practices.
- All monetary values in AUD.
- Compliance with Australian privacy and data protection standards.
