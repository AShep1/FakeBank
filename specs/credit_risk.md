# Credit Risk Data Model

## Overview
This data model covers the credit risk domain for a hypothetical bank. It consists of 6 tables, each designed to support panel data over 24 months. Each table includes an `as_of_date` column to represent the month-end snapshot. Referential integrity is enforced throughout.

## Tables


### 1. customers
See [customer.md](./customer.md) for the customer data model. Reference `customer_id` in other tables for referential integrity.

### 2. loans
- **loan_id** (PK): Unique loan identifier
- **customer_id** (FK): References customers.customer_id
- **as_of_date**: Month-end date
- **loan_amount**: Outstanding principal
- **credit_rating**: Internal rating (A/B/C/D)
- **lgd_rating**: Loss Given Default rating
- **ead**: Exposure at Default
- **rwa**: Risk Weighted Assets
- **capital**: Allocated capital
- **provisions**: Loan loss provisions
- **arrears**: Amount overdue
- **sales_channel**: Branch, broker, online, direct, etc.
- **industry**: ANZSIC industry classification (for business loans)
- **geography**: State, region, postcode (Australian context)
- **product_type**: Mortgage, personal loan, business loan, etc.
- **purpose**: Purchase, refinance, working capital, investment, etc.
- **currency**: AUD (default), but allow for multi-currency if needed
- **origination_date**: Date loan was originated
- **maturity_date**: Date loan matures
- **interest_rate**: Current interest rate
- **repayment_type**: Principal & interest, interest only, etc.
- **collateral_type**: Property, vehicle, deposit, unsecured, etc.

### 3. loan_applications
- **application_id** (PK): Unique application identifier
- **customer_id** (FK): References customers.customer_id
- **application_date**: Date of application
- **amount_requested**: Requested loan amount
- **status**: Approved/Rejected/Pending
- **product_type**: Loan product type

### 4. write_offs
- **write_off_id** (PK): Unique write-off identifier
- **loan_id** (FK): References loans.loan_id
- **as_of_date**: Month-end date
- **amount_written_off**: Amount written off
- **reason**: Reason for write-off

### 5. credit_events
- **event_id** (PK): Unique event identifier
- **loan_id** (FK): References loans.loan_id
- **as_of_date**: Month-end date
- **event_type**: Default/Restructure/Extension
- **event_details**: Description

### 6. loan_securities
- **security_id** (PK): Unique identifier
- **loan_id** (FK): References loans.loan_id
- **as_of_date**: Month-end date
- **security_type**: Property, vehicle, deposit, etc.
- **security_value**: Estimated value of the security
- **address**: Address/location of the security (if applicable)
- **lien_type**: First lien, second lien, etc.
- **ownership_details**: Owner name or entity

## Data Population Guidelines
- For each month-end (`as_of_date`), generate ~100,000 loan records, ensuring customer and loan referential integrity.
- Customer data should be stable, but allow for new customers each month.
- Loan balances should change slightly each month for most customers, with some large movements for a minority.
- Loan applications and write-offs should reference valid customers/loans only.
- Use realistic distributions for credit ratings, LGD, EAD, RWA, capital, provisions, and arrears.
- Ensure no orphan customers (all referenced customers exist).
- Use Faker to generate names, addresses, and other synthetic data.

## Data Population Guidelines for Loan Securities
- Generate securities for a subset of loans, with plausible distribution of security types (e.g., most mortgages have property as security).
- Use Faker for addresses and owner details.
- Ensure referential integrity: all securities reference valid loans.
- Security values should be realistic and may change slightly month-to-month.
- Lien types should reflect typical banking practices (e.g., most are first lien).

---

## Australian Context
- All data and scenarios should reflect the Australian banking market.
- Regulatory references: Australian Prudential Regulation Authority (APRA), Australian Securities and Investments Commission (ASIC).
- Credit ratings, LGD, EAD, RWA, and capital calculations should follow APRA guidelines.
- Loan securities should include common Australian assets (e.g., residential property, commercial property) and lien types as per Australian law.
- Customer segments should reflect Australian demographics and banking products.
- All monetary values in AUD.
- Compliance with Australian privacy and data protection standards.

---

## Month-on-Month Data Generation Logic

To simulate realistic panel data for credit risk, use the following approach for month-end changes:

### Loan Balances
- For 99% of customers, loan balances should change by a small random percentage (e.g., ±2%) each month, reflecting regular repayments and interest accruals.
- For 1% of customers, apply a material change (e.g., >20%) to simulate events such as large repayments, drawdowns, or defaults.
- Use a function such as:

```python
import random

def update_balance(balance, is_material=False):
    if is_material:
        # Material change: large movement
        change_pct = random.uniform(-0.5, 0.5)  # -50% to +50%
    else:
        # Small change: regular movement
        change_pct = random.uniform(-0.02, 0.02)  # -2% to +2%
    return round(balance * (1 + change_pct), 2)
```

### PD and LGD Migration
- Each month, Probability of Default (PD) and Loss Given Default (LGD) ratings should migrate for a small proportion of loans (e.g., 2-5%).
- Migration should follow a plausible transition matrix, with most ratings remaining stable and a small probability of upgrade/downgrade.
- Example logic:

```python
def migrate_rating(current_rating, migration_probs):
    # migration_probs: dict of {new_rating: probability}
    ratings = list(migration_probs.keys())
    probs = list(migration_probs.values())
    return random.choices(ratings, probs)[0]
```

- Use APRA-compliant rating scales and migration probabilities.
- Ensure that changes are reflected in related metrics (EAD, RWA, provisions, etc.).

---

## Allowed Values for Dimensional Columns

### Credit Rating (Ordered Set)
- Allowed values: [A, B, C, D, E]
- Order: A (highest), B, C, D, E (lowest)

### LGD Rating (Ordered Set)
- Allowed values: [Low, Medium, High]
- Order: Low < Medium < High

### Sales Channel
- Allowed values: [Branch, Broker, Online, Direct, Mobile]

### Industry (ANZSIC Codes)
- Allowed values (examples): [Agriculture, Mining, Manufacturing, Construction, Retail Trade, Accommodation & Food Services, Financial & Insurance Services, Health Care & Social Assistance, Education & Training, Information Media & Telecommunications, Professional Services, Public Administration]
- Use official ANZSIC codes for full set.

### Geography
- Allowed values: Australian states [NSW, VIC, QLD, WA, SA, TAS, ACT, NT]
- Regions: Major cities, regional, remote
- Postcodes: Use valid Australian postcodes

### Product Type
- Allowed values: [Mortgage, Personal Loan, Business Loan, Credit Card, Overdraft]

### Purpose
- Allowed values: [Purchase, Refinance, Working Capital, Investment, Debt Consolidation]

### Currency
- Allowed values: [AUD] (default), [USD, EUR, GBP, NZD] (if multi-currency required)

### Repayment Type
- Allowed values: [Principal & Interest, Interest Only]

### Collateral Type
- Allowed values: [Property, Vehicle, Deposit, Unsecured, Equipment]

### Lien Type (Ordered Set)
- Allowed values: [First Lien, Second Lien, Third Lien]
- Order: First < Second < Third

### Loan Application Status
- Allowed values: [Approved, Rejected, Pending]

### Event Type (Credit Events)
- Allowed values: [Default, Restructure, Extension]

---

## Data Population Guidelines (Updated)
- Ensure all dimensional columns use only the allowed values listed above.
- For ordered sets, maintain the correct sequence in data generation and migration logic.
- Use official ANZSIC codes and valid Australian postcodes for industry and geography.
- Document all allowed values in the data generation scripts for consistency.

## Expanded Loan Table Dimensions

Add the following features to the `loans` table for richer credit risk analysis:

- **sales_channel**: Branch, broker, online, direct, etc.
- **industry**: ANZSIC industry classification (for business loans)
- **geography**: State, region, postcode (Australian context)
- **product_type**: Mortgage, personal loan, business loan, etc.
- **purpose**: Purchase, refinance, working capital, investment, etc.
- **currency**: AUD (default), but allow for multi-currency if needed
- **origination_date**: Date loan was originated
- **maturity_date**: Date loan matures
- **interest_rate**: Current interest rate
- **repayment_type**: Principal & interest, interest only, etc.
- **collateral_type**: Property, vehicle, deposit, unsecured, etc.

## Financial Metrics (for business/commercial loans)
- **interest_coverage_ratio**: EBIT / Interest expense
- **debt_to_equity_ratio**: Total debt / Total equity
- **current_ratio**: Current assets / Current liabilities
- **net_profit_margin**: Net profit / Revenue
- **total_assets**: Total assets of the company
- **total_liabilities**: Total liabilities of the company
- **annual_revenue**: Annual revenue

## Data Population Guidelines (Expanded)
- Populate dimensional features using realistic distributions for the Australian market (e.g., ANZSIC codes, state postcodes).
- Financial metrics should be plausible and consistent with company size, industry, and loan characteristics.
- Use Faker and synthetic logic to generate these features, ensuring referential integrity and realistic relationships.
- Document all new features in the data generation scripts and ensure they are used in credit risk analysis and reporting.
