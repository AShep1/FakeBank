📑 Market Risk Management Framework
1. Purpose and Scope

This framework defines how the Bank identifies, measures, monitors, and manages market risk — the risk of losses from movements in market prices (interest rates, FX rates, equity prices, credit spreads, and commodity prices).

It applies to all trading desks — Equities, Fixed Income, FX, Commodities, and Derivatives — and covers all market risk exposures in the trading book and mark-to-market banking book positions.

The framework is consistent with:

APRA CPS 220 (Risk Management)

APRA APS 116 (Market Risk Standard)

Basel III market risk guidelines (FRTB alignment)

ASIC obligations for conduct and transparency

2. Governance Structure

Board Risk Committee (BRC): Approves market risk appetite and reviews breaches quarterly.

CRO: Owns the market risk policy and ensures aggregate risk remains within appetite.

Market Risk Function: Monitors VaR, SVaR, Expected Shortfall, and other limits daily; escalates breaches.

Trading Desks: Own positions, comply with limits, and execute stop-loss procedures where required.

3. Market Risk Identification & Measurement
Metric	Definition	Frequency
VaR (99%, 1-day)	Maximum expected loss under normal conditions	Daily
SVaR (99%)	Maximum expected loss under stressed conditions	Daily
Expected Shortfall	Average loss beyond VaR	Daily
Volatility	Realized or implied volatility	Daily
Position Concentration	% of notional in single instrument	Daily
Desk Exposure	Total market value per desk	Daily

Metrics are sourced from the market_positions and market_risk_metrics tables, aggregated by desk, instrument, customer segment, and geography.

4. Concentration Risk Measurement

Market risk concentration is explicitly monitored along the following dimensions:

Dimension	Metric	Limit
Desk	Desk-level VaR	≤ AUD 10M
Instrument	Max exposure per instrument type	≤ 10% of total trading book value
Customer Segment	Max exposure per segment (Retail, SME, Corporate)	≤ 40%
Geography	Max exposure per state	≤ 35%
Single Position	Notional per position ÷ total notional	≤ 5%

An HHI concentration index is also calculated monthly at desk level to detect emerging concentration.

5. Monitoring & Reporting

Daily Market Risk Dashboard:

Desk-level VaR, SVaR, ES, volatility vs limits

Top 10 instrument exposures

Concentration metrics by desk/instrument/segment/geography

Intraday Monitoring:

Alerts triggered if any desk reaches ≥ 90% of VaR limit

Breaches escalated to CRO within 1 hour

Monthly Aggregated Report:

Trend analysis of VaR/SVaR

Concentration HHI trend

Stress test impact per desk/instrument

6. Stress Testing & Scenario Analysis

Historical Scenarios: GFC 2008, COVID-19 March 2020, RBA emergency rate cuts

Hypothetical Scenarios: AUD depreciation 10%, ASX −15%, credit spread widening +200 bps

Reverse Stress Testing: Identify scenarios that breach capital buffer

Results must be reviewed by the CRO and BRC each quarter.