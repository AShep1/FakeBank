import os
import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random
from calendar import monthrange

# Set random seed for reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
fake = Faker('en_AU')
fake.seed_instance(SEED)

# Output folder
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

# Date range
END_DATE = datetime(2025, 9, 30)
MONTHS = 24
DATES = []
for i in reversed(range(MONTHS)):
    d = END_DATE - timedelta(days=30*i)
    last_day = monthrange(d.year, d.month)[1]
    DATES.append(d.replace(day=last_day))

# Print DATES and check for duplicates
print('DATES:', [d.strftime('%Y-%m-%d') for d in DATES])
if len(DATES) != len(set([d.strftime('%Y-%m-%d') for d in DATES])):
    print('Warning: Duplicate dates found in DATES! Removing duplicates.')
    # Remove duplicates while preserving order
    seen = set()
    unique_dates = []
    for d in DATES:
        ds = d.strftime('%Y-%m-%d')
        if ds not in seen:
            seen.add(ds)
            unique_dates.append(d)
    DATES = unique_dates
print('Final DATES:', [d.strftime('%Y-%m-%d') for d in DATES])


# Allowed values (from specs)
CREDIT_RATINGS = ['A', 'B', 'C', 'D', 'E']
LGD_RATINGS = ['Low', 'Medium', 'High']
SALES_CHANNELS = ['Branch', 'Broker', 'Online', 'Direct', 'Mobile']
INDUSTRIES = ['Agriculture', 'Mining', 'Manufacturing', 'Construction', 'Retail Trade', 'Financial & Insurance Services', 'Health Care & Social Assistance', 'Education & Training', 'Information Media & Telecommunications', 'Professional Services']
STATES = ['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'ACT', 'NT']
PRODUCT_TYPES = ['Mortgage', 'Personal Loan', 'Business Loan', 'Credit Card', 'Overdraft']
PURPOSES = ['Purchase', 'Refinance', 'Working Capital', 'Investment', 'Debt Consolidation']
REPAYMENT_TYPES = ['Principal & Interest', 'Interest Only']
COLLATERAL_TYPES = ['Property', 'Vehicle', 'Deposit', 'Unsecured', 'Equipment']
LIEN_TYPES = ['First Lien', 'Second Lien', 'Third Lien']
SEGMENTS = ['Retail', 'Corporate', 'SME']
APPLICATION_STATUS = ['Approved', 'Rejected', 'Pending']

# Liquidity Risk allowed values
ASSET_TYPES = ['Cash', 'Deposit', 'Security', 'Government Bond', 'Corporate Bond']
FUNDING_SOURCE_TYPES = ['Interbank', 'Retail', 'Wholesale']
LIQUIDITY_EVENT_TYPES = ['Stress', 'Withdrawal', 'Deposit']

# Market Risk allowed values
DESKS = ['Equities', 'Fixed Income', 'FX', 'Commodities', 'Derivatives']
INSTRUMENTS = ['ASX Equity', 'AUD Bond', 'FX Pair', 'Commodity', 'Derivative']
CURRENCIES = ['AUD', 'USD', 'EUR', 'GBP', 'NZD']
MARKET_EVENT_TYPES = ['Shock', 'News', 'Regulatory']

# Parameters
N_CUSTOMERS = 10000
N_LOANS = 100000
N_APPLICATIONS = 20000
N_WRITE_OFFS = 1000
N_INTERACTIONS = 50000
N_SECURITIES = 30000
N_LIQUIDITY_POSITIONS = 50000
N_FUNDING_SOURCES = 1000
N_LIQUIDITY_EVENTS = 500
N_MARKET_POSITIONS = 30000
N_MARKET_EVENTS = 500

# Helper functions

def random_choice(seq):
    return random.choice(seq)

def random_postcode():
    return str(random.randint(200, 9999))

def random_credit_rating():
    return np.random.choice(CREDIT_RATINGS, p=[0.2, 0.3, 0.3, 0.15, 0.05])

def random_lgd_rating():
    return np.random.choice(LGD_RATINGS, p=[0.7, 0.2, 0.1])

def random_state():
    return random_choice(STATES)

def random_industry():
    return random_choice(INDUSTRIES)

def random_segment():
    return random_choice(SEGMENTS)

def random_sales_channel():
    return random_choice(SALES_CHANNELS)

def random_product_type():
    return random_choice(PRODUCT_TYPES)

def random_purpose():
    return random_choice(PURPOSES)

def random_repayment_type():
    return random_choice(REPAYMENT_TYPES)

def random_collateral_type():
    return random_choice(COLLATERAL_TYPES)

def random_lien_type():
    return random_choice(LIEN_TYPES)

def random_application_status():
    return random_choice(APPLICATION_STATUS)

def random_financials():
    assets = random.randint(100_000, 10_000_000)
    liabilities = random.randint(50_000, assets)
    equity = assets - liabilities
    revenue = random.randint(50_000, 5_000_000)
    interest_expense = random.randint(1_000, 100_000)
    net_profit = random.randint(-100_000, revenue)
    return {
        'total_assets': assets,
        'total_liabilities': liabilities,
        'annual_revenue': revenue,
        'interest_coverage_ratio': round((revenue / interest_expense) if interest_expense else 0, 2),
        'debt_to_equity_ratio': round((liabilities / equity) if equity else 0, 2),
        'current_ratio': round(random.uniform(0.5, 3.0), 2),
        'net_profit_margin': round((net_profit / revenue) if revenue else 0, 2)
    }

# Generate customers
customers = []
for i in range(N_CUSTOMERS):
    customers.append({
        'customer_id': f'CUST{i+1:05d}',
        'name': fake.name(),
        'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=80),
        'address': fake.address().replace('\n', ', '),
        'customer_since': fake.date_between(start_date='-10y', end_date='today'),
        'segment': random_segment(),
        'state': random_state(),
        'postcode': random_postcode(),
        'industry': random_industry() if random_segment() != 'Retail' else ''
    })
customers_df = pd.DataFrame(customers)
customers_df.to_parquet(os.path.join(DATA_DIR, 'customers.parquet'))

# Generate loans (panel data)
loans = []
for as_of_idx, as_of_date in enumerate(DATES):
    for i in range(N_LOANS):
        cust = customers[i % N_CUSTOMERS]
        financials = random_financials() if cust['segment'] != 'Retail' else {}
        # Balance logic with upward trend and increased volatility
        if as_of_idx == 0:
            balance = random.randint(10_000, 1_000_000)
        else:
            prev = loans[-N_LOANS]
            is_material = (i % 100 == 0)
            # Monthly mean increase of ~0.33% (4% p.a.), std dev 6% for more volatility
            change_pct = np.random.normal(loc=0.0033, scale=0.06) if not is_material else np.random.normal(loc=0.0033, scale=0.35)
            balance = max(0, round(prev['loan_amount'] * (1 + change_pct), 2))
        # PD/LGD migration
        if as_of_idx == 0:
            credit_rating = random_credit_rating()
            lgd_rating = random_lgd_rating()
        else:
            prev = loans[-N_LOANS]
            # Small migration probability
            if random.random() < 0.05:
                credit_rating = random_credit_rating()
            else:
                credit_rating = prev['credit_rating']
            if random.random() < 0.05:
                lgd_rating = random_lgd_rating()
            else:
                lgd_rating = prev['lgd_rating']
        loans.append({
            'loan_id': f'LOAN{i+1:06d}',
            'customer_id': cust['customer_id'],
            'as_of_date': as_of_date.strftime('%Y-%m-%d'),
            'loan_amount': balance,
            'credit_rating': credit_rating,
            'lgd_rating': lgd_rating,
            'ead': round(balance * random.uniform(0.8, 1.2), 2),
            'rwa': round(balance * random.uniform(0.5, 1.5), 2),
            'capital': round(balance * random.uniform(0.08, 0.12), 2),
            'provisions': round(balance * random.uniform(0.01, 0.05), 2),
            'arrears': round(balance * random.uniform(0, 0.1), 2),
            'sales_channel': random_sales_channel(),
            'industry': cust['industry'],
            'geography': cust['state'],
            'product_type': random_product_type(),
            'purpose': random_purpose(),
            'currency': 'AUD',
            'origination_date': fake.date_between(start_date='-10y', end_date=as_of_date),
            'maturity_date': fake.date_between(start_date=as_of_date, end_date='+10y'),
            'interest_rate': round(random.uniform(2.5, 7.5), 2),
            'repayment_type': random_repayment_type(),
            'collateral_type': random_collateral_type(),
            **financials
        })
loans_df = pd.DataFrame(loans)
loans_df.to_parquet(os.path.join(DATA_DIR, 'loans.parquet'))

# Generate loan applications
applications = []
for i in range(N_APPLICATIONS):
    cust = customers[random.randint(0, N_CUSTOMERS-1)]
    applications.append({
        'application_id': f'APP{i+1:06d}',
        'customer_id': cust['customer_id'],
        'application_date': fake.date_between(start_date='-2y', end_date='today'),
        'amount_requested': random.randint(5_000, 500_000),
        'status': random_application_status(),
        'product_type': random_product_type()
    })
applications_df = pd.DataFrame(applications)
applications_df.to_parquet(os.path.join(DATA_DIR, 'loan_applications.parquet'))

# Generate write-offs
write_offs = []
for i in range(N_WRITE_OFFS):
    loan_idx = random.randint(0, N_LOANS-1)
    loan = loans[loan_idx]
    write_offs.append({
        'write_off_id': f'WO{i+1:05d}',
        'loan_id': loan['loan_id'],
        'as_of_date': loan['as_of_date'],
        'amount_written_off': round(loan['loan_amount'] * random.uniform(0.1, 1.0), 2),
        'reason': random_choice(['Default', 'Fraud', 'Bankruptcy', 'Settlement'])
    })
write_offs_df = pd.DataFrame(write_offs)
write_offs_df.to_parquet(os.path.join(DATA_DIR, 'write_offs.parquet'))

# Generate customer interactions
interactions = []
for i in range(N_INTERACTIONS):
    cust = customers[random.randint(0, N_CUSTOMERS-1)]
    interactions.append({
        'interaction_id': f'INT{i+1:07d}',
        'customer_id': cust['customer_id'],
        'interaction_date': fake.date_time_between(start_date='-2y', end_date='now'),
        'interaction_type': random_choice(['Phone Call', 'Email', 'Branch Visit', 'Chat', 'Mobile App']),
        'agent_id': f'AGT{random.randint(1, 100):03d}',
        'interaction_text': fake.sentence(nb_words=20)
    })
interactions_df = pd.DataFrame(interactions)
interactions_df.to_parquet(os.path.join(DATA_DIR, 'customer_interactions.parquet'))

# Generate loan securities
securities = []
for i in range(N_SECURITIES):
    loan = loans[i % len(loans)]
    securities.append({
        'security_id': f'SEC{i+1:06d}',
        'loan_id': loan['loan_id'],
        'as_of_date': loan['as_of_date'],
        'security_type': random_collateral_type(),
        'security_value': round(loan['loan_amount'] * random.uniform(0.5, 1.5), 2),
        'address': fake.address().replace('\n', ', '),
        'lien_type': random_lien_type(),
        'ownership_details': fake.name()
    })
securities_df = pd.DataFrame(securities)
securities_df.to_parquet(os.path.join(DATA_DIR, 'loan_securities.parquet'))

# ==================== LIQUIDITY RISK DATA ====================

print('Generating liquidity risk data...')

# Generate liquidity positions (panel data)
liquidity_positions = []
for as_of_date in DATES:
    for i in range(N_LIQUIDITY_POSITIONS):
        cust = customers[i % N_CUSTOMERS]
        # Amount logic
        if as_of_date == DATES[0]:
            amount = random.randint(10_000, 10_000_000)
        else:
            prev = liquidity_positions[-N_LIQUIDITY_POSITIONS]
            change_pct = random.uniform(-0.1, 0.1)
            amount = max(0, round(prev['amount'] * (1 + change_pct), 2))
        liquidity_positions.append({
            'position_id': f'LP{i+1:06d}',
            'as_of_date': as_of_date.strftime('%Y-%m-%d'),
            'customer_id': cust['customer_id'],
            'asset_type': random_choice(ASSET_TYPES),
            'amount': amount,
            'geography': cust['state'],
            'maturity_date': fake.date_between(start_date=as_of_date, end_date='+5y') if random.random() > 0.3 else None
        })
liquidity_positions_df = pd.DataFrame(liquidity_positions)
liquidity_positions_df.to_parquet(os.path.join(DATA_DIR, 'liquidity_positions.parquet'))

# Generate funding sources (panel data)
funding_sources = []
for as_of_date in DATES:
    for i in range(N_FUNDING_SOURCES):
        # Amount logic
        if as_of_date == DATES[0]:
            amount = random.randint(100_000, 100_000_000)
        else:
            prev = funding_sources[-N_FUNDING_SOURCES]
            change_pct = random.uniform(-0.05, 0.05)
            amount = max(0, round(prev['amount'] * (1 + change_pct), 2))
        
        funding_sources.append({
            'funding_id': f'FS{i+1:05d}',
            'as_of_date': as_of_date.strftime('%Y-%m-%d'),
            'source_type': random_choice(FUNDING_SOURCE_TYPES),
            'amount': amount,
            'cost': round(random.uniform(1.0, 5.0), 2)  # Cost of funds percentage
        })
funding_sources_df = pd.DataFrame(funding_sources)
funding_sources_df.to_parquet(os.path.join(DATA_DIR, 'funding_sources.parquet'))

# Generate liquidity metrics (panel data)
liquidity_metrics = []
metric_id = 1
for as_of_date in DATES:
    # Generate one set of metrics per month
    cash_inflows = random.randint(1_000_000, 100_000_000)
    cash_outflows = random.randint(1_000_000, 100_000_000)
    lcr = round(random.uniform(100, 150), 2)  # LCR should be above 100%
    nsfr = round(random.uniform(100, 130), 2)  # NSFR should be above 100%
    
    liquidity_metrics.append({
        'metric_id': f'LM{metric_id:05d}',
        'as_of_date': as_of_date.strftime('%Y-%m-%d'),
        'LCR': lcr,
        'NSFR': nsfr,
        'cash_inflows': cash_inflows,
        'cash_outflows': cash_outflows
    })
    metric_id += 1
liquidity_metrics_df = pd.DataFrame(liquidity_metrics)
liquidity_metrics_df.to_parquet(os.path.join(DATA_DIR, 'liquidity_metrics.parquet'))

# Generate liquidity events
liquidity_events = []
for i in range(N_LIQUIDITY_EVENTS):
    as_of_date = random_choice(DATES)
    event_type = random_choice(LIQUIDITY_EVENT_TYPES)
    
    # Generate appropriate event details based on type
    if event_type == 'Stress':
        details = random_choice([
            'Market volatility stress test scenario',
            'Regulatory stress test scenario',
            'Internal stress test - severe economic downturn',
            'Liquidity stress test - bank run scenario'
        ])
    elif event_type == 'Withdrawal':
        details = f'Large withdrawal of ${random.randint(100_000, 10_000_000):,} from {random_choice(["corporate", "institutional", "retail"])} customers'
    else:  # Deposit
        details = f'Large deposit of ${random.randint(100_000, 10_000_000):,} from {random_choice(["corporate", "institutional", "retail"])} customers'
    
    liquidity_events.append({
        'event_id': f'LE{i+1:05d}',
        'as_of_date': as_of_date.strftime('%Y-%m-%d'),
        'event_type': event_type,
        'event_details': details
    })
liquidity_events_df = pd.DataFrame(liquidity_events)
liquidity_events_df.to_parquet(os.path.join(DATA_DIR, 'liquidity_events.parquet'))

# ==================== MARKET RISK DATA ====================

print('Generating market risk data...')

# Generate market positions (panel data)
market_positions = []
for as_of_date in DATES:
    for i in range(N_MARKET_POSITIONS):
        cust = customers[i % N_CUSTOMERS]
        # Value logic
        if as_of_date == DATES[0]:
            notional = random.randint(10_000, 50_000_000)
            market_value = notional * random.uniform(0.9, 1.1)
        else:
            prev = market_positions[-N_MARKET_POSITIONS]
            change_pct = random.uniform(-0.15, 0.15)
            notional = max(0, round(prev['notional'] * (1 + change_pct * 0.1), 2))
            market_value = notional * random.uniform(0.9, 1.1)
        
        market_positions.append({
            'position_id': f'MP{i+1:06d}',
            'as_of_date': as_of_date.strftime('%Y-%m-%d'),
            'desk': random_choice(DESKS),
            'instrument': random_choice(INSTRUMENTS),
            'notional': round(notional, 2),
            'market_value': round(market_value, 2),
            'customer_id': cust['customer_id']
        })
market_positions_df = pd.DataFrame(market_positions)
market_positions_df.to_parquet(os.path.join(DATA_DIR, 'market_positions.parquet'))

# Generate market risk metrics (panel data)
market_risk_metrics = []
metric_id = 1
for idx, position in enumerate(market_positions):
    # Generate metrics for each position
    notional = position['notional']
    market_value = position['market_value']
    
    # VaR typically 1-3% of position value
    var = round(market_value * random.uniform(0.01, 0.03), 2)
    # SVaR typically 2-5% of position value
    svar = round(market_value * random.uniform(0.02, 0.05), 2)
    # Expected shortfall typically slightly higher than VaR
    expected_shortfall = round(var * random.uniform(1.1, 1.3), 2)
    # Volatility as percentage
    volatility = round(random.uniform(5, 30), 2)
    
    market_risk_metrics.append({
        'metric_id': f'MRM{metric_id:06d}',
        'position_id': position['position_id'],
        'as_of_date': position['as_of_date'],
        'VaR': var,
        'SVaR': svar,
        'expected_shortfall': expected_shortfall,
        'volatility': volatility
    })
    metric_id += 1
market_risk_metrics_df = pd.DataFrame(market_risk_metrics)
market_risk_metrics_df.to_parquet(os.path.join(DATA_DIR, 'market_risk_metrics.parquet'))

# Generate instrument prices (panel data)
instrument_prices = []
price_id = 1
for as_of_date in DATES:
    for instrument in INSTRUMENTS:
        # Set base price based on instrument type
        if instrument == 'ASX Equity':
            base_price = random.uniform(5, 200)
        elif instrument == 'AUD Bond':
            base_price = random.uniform(95, 105)
        elif instrument == 'FX Pair':
            base_price = random.uniform(0.5, 1.5)
        elif instrument == 'Commodity':
            base_price = random.uniform(50, 500)
        else:  # Derivative
            base_price = random.uniform(10, 100)
        
        # Add some variation
        if as_of_date != DATES[0] and price_id > len(INSTRUMENTS):
            prev_idx = price_id - len(INSTRUMENTS) - 1
            prev_price = instrument_prices[prev_idx]['price']
            change_pct = random.uniform(-0.1, 0.1)
            price = max(0.01, round(prev_price * (1 + change_pct), 2))
        else:
            price = round(base_price, 2)
        
        instrument_prices.append({
            'price_id': f'IP{price_id:06d}',
            'instrument': instrument,
            'as_of_date': as_of_date.strftime('%Y-%m-%d'),
            'price': price,
            'currency': 'AUD' if random.random() > 0.2 else random_choice(CURRENCIES)
        })
        price_id += 1
instrument_prices_df = pd.DataFrame(instrument_prices)
instrument_prices_df.to_parquet(os.path.join(DATA_DIR, 'instrument_prices.parquet'))

# Generate market events
market_events = []
for i in range(N_MARKET_EVENTS):
    as_of_date = random_choice(DATES)
    instrument = random_choice(INSTRUMENTS)
    event_type = random_choice(MARKET_EVENT_TYPES)
    
    # Generate appropriate event details based on type
    if event_type == 'Shock':
        details = random_choice([
            'Market shock - significant price movement',
            'Flash crash event',
            'Volatility spike',
            'Liquidity shock in market'
        ])
    elif event_type == 'News':
        details = random_choice([
            'RBA interest rate announcement',
            'Major economic data release',
            'Corporate earnings announcement',
            'Geopolitical news affecting markets'
        ])
    else:  # Regulatory
        details = random_choice([
            'APRA regulatory update',
            'ASIC market conduct review',
            'New capital requirements announced',
            'Market structure regulatory change'
        ])
    
    market_events.append({
        'event_id': f'ME{i+1:05d}',
        'as_of_date': as_of_date.strftime('%Y-%m-%d'),
        'instrument': instrument,
        'event_type': event_type,
        'event_details': details
    })
market_events_df = pd.DataFrame(market_events)
market_events_df.to_parquet(os.path.join(DATA_DIR, 'market_events.parquet'))

print('Fake bank data generated in ./data as parquet files.')
print('\nGenerated files:')
print('  Credit Risk:')
print('    - customers.parquet')
print('    - loans.parquet')
print('    - loan_applications.parquet')
print('    - write_offs.parquet')
print('    - customer_interactions.parquet')
print('    - loan_securities.parquet')
print('  Liquidity Risk:')
print('    - liquidity_positions.parquet')
print('    - funding_sources.parquet')
print('    - liquidity_metrics.parquet')
print('    - liquidity_events.parquet')
print('  Market Risk:')
print('    - market_positions.parquet')
print('    - market_risk_metrics.parquet')
print('    - instrument_prices.parquet')
print('    - market_events.parquet')

# Purge old .png, .parquet, and .csv files in output folders
import glob
for folder in [DATA_DIR, 'sample', 'summary']:
    for ext in ('*.png', '*.parquet', '*.csv'):
        for f in glob.glob(os.path.join(folder, ext)):
            try:
                os.remove(f)
            except Exception as e:
                print(f'Could not remove {f}: {e}')

# Save head(15) of each table to 'sample' folder as CSV
sample_dir = 'sample'
os.makedirs(sample_dir, exist_ok=True)
for df, name in [
    (customers_df, 'customers'),
    (loans_df, 'loans'),
    (applications_df, 'loan_applications'),
    (write_offs_df, 'write_offs'),
    (interactions_df, 'customer_interactions'),
    (securities_df, 'loan_securities'),
    (liquidity_positions_df, 'liquidity_positions'),
    (funding_sources_df, 'funding_sources'),
    (liquidity_metrics_df, 'liquidity_metrics'),
    (liquidity_events_df, 'liquidity_events'),
    (market_positions_df, 'market_positions'),
    (market_risk_metrics_df, 'market_risk_metrics'),
    (instrument_prices_df, 'instrument_prices'),
    (market_events_df, 'market_events')
]:
    df.head(15).to_csv(os.path.join(sample_dir, f'{name}_sample.csv'), index=False)

# Data profiling and summary charts
import matplotlib.pyplot as plt
import seaborn as sns
summary_dir = 'summary'
os.makedirs(summary_dir, exist_ok=True)

loan_amt_by_date = loans_df.groupby('as_of_date')['loan_amount'].sum().reset_index()
# Remove duplicate as_of_date if any
loan_amt_by_date = loan_amt_by_date.drop_duplicates(subset=['as_of_date'])
plt.figure(figsize=(12,6))
sns.lineplot(data=loan_amt_by_date, x='as_of_date', y='loan_amount')
plt.title('Total Loan Amounts by As-of-Date')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(summary_dir, 'total_loan_amounts_by_date.png'))
plt.close()

# Stacked column chart: loan amount by as_of_date and industry
industry_by_date = loans_df.groupby(['as_of_date', 'industry'])['loan_amount'].sum().unstack(fill_value=0)
industry_by_date = industry_by_date.loc[~industry_by_date.index.duplicated(keep='first')]
industry_by_date.plot(kind='bar', stacked=True, figsize=(14,7))
plt.title('Stacked Loan Amounts by Industry and As-of-Date')
plt.xlabel('As-of-Date')
plt.ylabel('Loan Amount')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(summary_dir, 'stacked_loan_amounts_by_industry.png'))
plt.close()

# Stacked column chart: loan amount by as_of_date and sales_channel
channel_by_date = loans_df.groupby(['as_of_date', 'sales_channel'])['loan_amount'].sum().unstack(fill_value=0)
channel_by_date = channel_by_date.loc[~channel_by_date.index.duplicated(keep='first')]
channel_by_date.plot(kind='bar', stacked=True, figsize=(14,7))
plt.title('Stacked Loan Amounts by Sales Channel and As-of-Date')
plt.xlabel('As-of-Date')
plt.ylabel('Loan Amount')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(summary_dir, 'stacked_loan_amounts_by_channel.png'))
plt.close()

def plot_and_save(df, col, title, filename, kind='bar', rotate_xticks=True):
    plt.figure(figsize=(12,6))
    if kind == 'bar':
        df[col].value_counts().plot(kind='bar')
    elif kind == 'hist':
        df[col].plot(kind='hist', bins=30)
    plt.title(title)
    if rotate_xticks:
        plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(summary_dir, filename))
    plt.close()

# Customers profiling
plot_and_save(customers_df, 'segment', 'Customer Segment Distribution', 'customers_segment.png')
plot_and_save(customers_df, 'state', 'Customer State Distribution', 'customers_state.png')

# Loans profiling
plot_and_save(loans_df, 'credit_rating', 'Loan Credit Rating Distribution', 'loans_credit_rating.png')
plot_and_save(loans_df, 'lgd_rating', 'Loan LGD Rating Distribution', 'loans_lgd_rating.png')
plot_and_save(loans_df, 'industry', 'Loan Industry Distribution', 'loans_industry.png')
plot_and_save(loans_df, 'sales_channel', 'Loan Sales Channel Distribution', 'loans_sales_channel.png')
plot_and_save(loans_df, 'product_type', 'Loan Product Type Distribution', 'loans_product_type.png')
plot_and_save(loans_df, 'loan_amount', 'Loan Amount Distribution', 'loans_loan_amount.png', kind='hist', rotate_xticks=False)

# Loan Applications profiling
plot_and_save(applications_df, 'status', 'Loan Application Status Distribution', 'applications_status.png')
plot_and_save(applications_df, 'product_type', 'Loan Application Product Type Distribution', 'applications_product_type.png')
plot_and_save(applications_df, 'amount_requested', 'Loan Application Amount Requested Distribution', 'applications_amount_requested.png', kind='hist', rotate_xticks=False)

# Write Offs profiling
plot_and_save(write_offs_df, 'reason', 'Write Off Reason Distribution', 'write_offs_reason.png')
plot_and_save(write_offs_df, 'amount_written_off', 'Write Off Amount Distribution', 'write_offs_amount_written_off.png', kind='hist', rotate_xticks=False)

# Customer Interactions profiling
plot_and_save(interactions_df, 'interaction_type', 'Customer Interaction Type Distribution', 'interactions_type.png')

# Loan Securities profiling
plot_and_save(securities_df, 'security_type', 'Loan Security Type Distribution', 'securities_type.png')
plot_and_save(securities_df, 'lien_type', 'Loan Security Lien Type Distribution', 'securities_lien_type.png')
plot_and_save(securities_df, 'security_value', 'Loan Security Value Distribution', 'securities_value.png', kind='hist', rotate_xticks=False)

print('Sample data and summary charts generated.')
print('Profiling charts for all tables generated.')

def plot_stacked_by_dimension(df, value_col, dimension_col, filename, aggfunc='sum'):
    if 'as_of_date' not in df.columns:
        return
    pivot = df.pivot_table(
        index='as_of_date',
        columns=dimension_col,
        values=value_col,
        aggfunc=aggfunc,
        fill_value=0
    )
    pivot.plot(kind='bar', stacked=True, figsize=(12, 6))
    plt.title(f"{value_col} by {dimension_col} and as_of_date")
    plt.ylabel(value_col)
    plt.xlabel("as_of_date")
    plt.tight_layout()
    plt.savefig(os.path.join(summary_dir, os.path.basename(filename)))
    plt.close()

# Update all calls to plot_stacked_by_dimension to use only the filename, not a path
plot_stacked_by_dimension(loans_df, 'loan_amount', 'industry', 'loans_by_industry_stacked.png')
plot_stacked_by_dimension(loans_df, 'loan_amount', 'sales_channel', 'loans_by_channel_stacked.png')
plot_stacked_by_dimension(loans_df, 'loan_amount', 'product_type', 'loans_by_product_type_stacked.png')
plot_stacked_by_dimension(loans_df, 'loan_amount', 'credit_rating', 'loans_by_credit_rating_stacked.png')
plot_stacked_by_dimension(loans_df, 'loan_amount', 'lgd_rating', 'loans_by_lgd_rating_stacked.png')
plot_stacked_by_dimension(applications_df, 'amount_requested', 'product_type', 'applications_by_product_type_stacked.png')
plot_stacked_by_dimension(applications_df, 'amount_requested', 'status', 'applications_by_status_stacked.png')
plot_stacked_by_dimension(write_offs_df, 'amount_written_off', 'reason', 'write_offs_by_reason_stacked.png')
if 'as_of_date' in interactions_df.columns:
    interactions_df['as_of_date'] = pd.to_datetime(interactions_df['interaction_date']).dt.strftime('%Y-%m-%d')
plot_stacked_by_dimension(interactions_df, 'interaction_id', 'interaction_type', 'interactions_by_type_stacked.png', aggfunc='count')
plot_stacked_by_dimension(securities_df, 'security_value', 'security_type', 'securities_by_type_stacked.png')
plot_stacked_by_dimension(securities_df, 'security_value', 'lien_type', 'securities_by_lien_type_stacked.png')
if 'liquidity_positions_df' in locals():
    plot_stacked_by_dimension(liquidity_positions_df, 'amount', 'asset_type', 'liquidity_by_asset_type_stacked.png')
    plot_stacked_by_dimension(liquidity_positions_df, 'amount', 'geography', 'liquidity_by_geography_stacked.png')
if 'funding_sources_df' in locals():
    plot_stacked_by_dimension(funding_sources_df, 'amount', 'source_type', 'funding_by_source_type_stacked.png')
if 'market_positions_df' in locals():
    plot_stacked_by_dimension(market_positions_df, 'market_value', 'instrument', 'market_by_instrument_stacked.png')
    plot_stacked_by_dimension(market_positions_df, 'market_value', 'desk', 'market_by_desk_stacked.png')

print('Stacked column profiling charts for all tables generated.')
print('Stacked column profiling charts for liquidity and market risk tables generated.')
