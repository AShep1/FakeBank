# FakeBank: Synthetic Bank Data Generator

This repository creates a completely synthetic bank for semantic prototyping. It generates realistic, referentially consistent data across credit, market, and liquidity risk domains, with profiling charts and sample data for quick inspection.

## Quick Start
- Run `generate_fakebank_data.py` to generate data and charts.
- All outputs are stored in the `data`, `sample`, and `summary` folders.

## Sample Data
- [Sample Customers](sample/customers_sample.csv)
- [Sample Loans](sample/loans_sample.csv)
- [Sample Loan Applications](sample/loan_applications_sample.csv)
- [Sample Write Offs](sample/write_offs_sample.csv)
- [Sample Customer Interactions](sample/customer_interactions_sample.csv)
- [Sample Loan Securities](sample/loan_securities_sample.csv)

## Profiling Charts
Below are example images from the `summary` folder:

![Total Loan Amounts by Date](summary/total_loan_amounts_by_date.png)
![Stacked Loan Amounts by Industry](summary/loans_by_industry_stacked.png)
![Stacked Loan Amounts by Channel](summary/loans_by_channel_stacked.png)
![Liquidity by Asset Type](summary/liquidity_by_asset_type_stacked.png)
![Market by Instrument](summary/market_by_instrument_stacked.png)

---

For more details, see the data specs in the `specs` folder.
