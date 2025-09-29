```markdown
# Market Risk Management Framework

Version: 1.0
Effective Date: 2025-10-01

## Purpose
Define measurable controls for market risk with clear aggregation and escalation rules. All metrics reference the FakeBank market datasets so analyses are directly reproducible.

## Scope & Data Sources
- `data/market_positions.parquet`: `position_id`, `instrument_id`, `desk`, `as_of_date`, `notional`, `market_value`, `currency`, `issuer`
- `data/market_risk_metrics.parquet`: `as_of_date`, `desk`, `VaR`, `SVaR`, `expected_shortfall`, `volatility`
- `data/instrument_prices.parquet`: historical prices for scenario replays and backtesting

## Limit Framework (metricated & aggregation)

- Desk VaR:
  - Metric: VaR (e.g., 99% one-day equivalent) aggregated per `desk` and reported per `as_of_date`.
  - Appetite: limit = AUD 10,000,000 per desk. Alert at 80% of limit; Breach >100%.

- Position concentration:
  - Metric: instrument_share = market_value_of_instrument / total_market_value_of_desk
  - Appetite: no single instrument > 10% of desk exposure; alert at 9%.

- Volatility:
  - Metric: realized or implied volatility per desk or instrument from `market_risk_metrics`.
  - Appetite: alert if volatility > 20% for a desk or instrument.

## Monitoring & Backtesting
- Frequency: daily conceptually; synthetic monthly snapshots for `as_of_date`.
- Required outputs: VaR/SVaR time series, top positions, backtest exceptions count (realized P&L > VaR).

## Escalation & Response
- Early Warning (>=80% of VaR limit): Trading desk to propose hedge plan within 24 hours; Risk Analytics notified.
- Breach (>100%): Immediate de-risking of offending positions, notify CRO and Board Risk Committee within 24 hours, produce remediation plan within 3 business days.

## Stress Testing
- Historical and hypothetical scenarios (ASX -15%, AUD depreciation 10%, credit spread widening) applied to `instrument_prices` to compute P&L impacts and margin calls.

## Data Quality
- Mandatory fields: `as_of_date`, `desk`, `VaR`, `SVaR`, `instrument_id`, `market_value`.
- Validate instrument price histories for material instruments prior to running stress tests.

--
This Market Risk Management Framework is synthetic and intended for testing and training with the FakeBank datasets.
```
