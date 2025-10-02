# Example prompts for FakeBank datasets

These prompts are phrased so they can be converted into SQL-like queries over the generated Parquet tables. Use `as_of_date` for monthly snapshots and join on keys like `customer_id`, `loan_id`, and `position_id` as needed.

Tip: Unless stated, “latest month” means the maximum `as_of_date` in the relevant table.

## Credit risk

- Which geography has the highest increase month-over-month in RWA concentration (rwa / ead) over the last 6 months?
- Show top 10 industries by year-over-year growth in total RWA.
- List the customers with the largest downgrade in `credit_rating` between the last two snapshots, and show their EAD and RWA changes.
- Summarise the most recent customer interactions for the 3 customers who had the largest downgrade in `credit_rating` in the latest month.
- What’s the distribution of `credit_rating` and `lgd_rating` by product_type for the latest month?
- Compute the CAR (sum(capital) / sum(rwa)) for the latest month and show the 12‑month trend.
- What is the arrears ratio (sum(arrears) / sum(loan_amount)) by geography and product_type for the latest month?
- Show the provision coverage ratio (sum(provisions) / expected losses proxy using EAD × mapped PD × mapped LGD) by industry.
- Trend of write-offs (count and sum(amount_written_off)) by reason over the past 24 months.
- What share of loan balances is originated via each `sales_channel`, and how has the channel mix shifted in the last 12 months?
- Which 10 customers have the largest increase in EAD in the last quarter? Include industry, geography, and product_type.
- Give me a PD/LGD migration matrix (credit_rating and lgd_rating transition counts) over the last 12 months.
- Show loans maturing in the next 6 months with current `arrears > 0` and `credit_rating` of C or worse.
- Which product_type has the highest weighted average interest_rate, weighted by loan_amount, in the latest month?
- List collateral_type mix and average LTV proxy (loan_amount / security_value) for loans with `collateral_type != 'Unsecured'`.
- Which origination cohorts (by quarter) have the highest current arrears rate?
- What is the average time from `application_date` to approval for approved loan applications by product_type?
- Show write_off rate (sum(amount_written_off) / sum(loan_amount)) by geography, last 12 months.

## Liquidity risk

- Show the LCR, NSFR, cash_inflows, and cash_outflows for each month in the past 24 months.
- Identify months where LCR < 100% or NSFR < 100% and flag them as breaches.
- Which funding source_type contributes the most to total funding amount in the latest month? Show concentration share by source_type.
- Trend of funding cost (weighted average `cost` by source_type) over the last 12 months.
- Which asset_type holds the largest share of liquidity positions in the latest month? Provide amounts and percentages.
- For each geography, show cash_outflows trend and correlate with liquidity_events counts.
- Which 10 customers have the largest liquidity_positions amounts and how has that changed over the last 6 months?
- Show maturity ladder buckets (e.g., <=30d, 31–90d, 91–365d, >365d) for liquidity_positions by amount in the latest month.
- Which liquidity_events types (Stress/Withdrawal/Deposit) occurred most frequently in the last 12 months? Show counts by month.
- Identify the top 5 days (months) with the largest net cash outflows and show contributing funding_sources.
- Compute survival horizon proxy given HQLA (from LCR inputs) and net cash outflows; show monthly trend.
- Which funding source_type had the largest month-over-month decrease in amount in the latest month?

## Market risk

- What is my Value at Risk by desk for the latest month? Include SVaR and Expected Shortfall.
- Show the 12‑month trend of VaR by desk and highlight desks exceeding an internal limit threshold.
- Which instrument has the highest volatility in the last 6 months? Show top 10 instruments by average volatility.
- Mark‑to‑market change by desk: show month-over-month change in total `market_value` for the last 12 months.
- Which positions have the largest notional exposure in the latest month? Include desk and instrument.
- VaR density: show the distribution (quantiles) of VaR at the position level for the latest month by desk.
- Which desks show rising volatility with flat market_value (potential risk build-up) over the last 6 months?
- Cross-check: for instruments with adverse market_events (Shock/Regulatory), show average change in `market_value` around those months.
- Correlate instrument_prices changes with position-level `market_value` changes for instruments traded by the Fixed Income desk.
- Show positions in FX with largest positive and negative `market_value` changes in the last 3 months.
- Compute desk-level concentration: top instrument `market_value` / total desk `market_value` for the latest month.
- For each desk, show the VaR-to-notional ratio by month and flag outliers.

## Customer and interactions

- Summarise most recent customer interactions for the top 10 customers by EAD in the latest month.
- Show interaction counts by interaction_type per customer segment for the last 6 months.
- Which customers had an increase in `arrears` and more than 3 support interactions in the last 90 days?
- For SME customers, list common themes in `interaction_text` in months preceding a downgrade in `credit_rating`.
- Show customer tenure (`customer_since`) cohorts and their average product mix (product_type) and `interest_rate`.
- For customers in NSW, compare average `loan_amount` and `arrears` to VIC for the latest month.
- Which 20 customers have both high EAD and high number of interactions (top decile in both) in the last 6 months?
- Summarise complaints (if detectable via `interaction_text` keyword heuristics) by month and geography.

## Cross-domain governance and policy‑aligned prompts

- Compute and trend Capital Adequacy Ratio (sum(capital) / sum(rwa)) and flag green/amber/red vs policy thresholds.
- Trend LCR and NSFR and flag months with breaches (<100%).
- Desk VaR vs internal limit: flag desks with VaR ≥ 80% of limit and those breaching 100%.
- Funding concentration: show largest source_type share and flag if >20%.
- Single customer exposure: top EAD / total capital; flag if >5%.
- Provision coverage ratio: sum(provisions) / expected losses proxy; show by industry and geography.
- Position concentration: top instrument `market_value` share within each desk; flag if >10%.
- Escalation events list: months where any governance metric enters amber/red and count impacted metrics.
- Policy dashboard for latest month: CAR, LCR, NSFR, VaR-by-desk, funding concentration, with status icons.
- Breach timeline: show chronological list of any CAR/LCR/NSFR/desk VaR breaches in the last 24 months.

## Templates with placeholders (for programmatic generation)

- For the latest month, show {metric} by {dimension} ranked descending. Table: {table}.
- Show the {n} entities with the largest month-over-month increase in {measure} filtered by {filters}.
- Trend of {metric} by month for the last {k} months filtered by {filters}.
- Compute ratio {numerator}/{denominator} by {dimension} for the latest month.
- Compare {dimension} mix share for the latest two months and show absolute/relative change.
- Show cohort outcomes for entities originated in {period}, measured by {metric} at {horizon} months.
- List all records where {metric} breaches {operator} {threshold} in the last {k} months.
- Show top {n} contributors to change in {metric} between {start_month} and {end_month}.
- For {desk}, list instruments with highest {metric} and show {related_metric}.
- Summarise the most recent {n} interactions for customers matching {filters}.


