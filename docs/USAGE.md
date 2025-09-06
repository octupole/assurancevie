# Detailed Usage Guide

## Table of Contents

1. [Basic Concepts](#basic-concepts)
2. [Withdrawal Strategies](#withdrawal-strategies)
3. [Tax Optimization](#tax-optimization)
4. [Grid Analysis](#grid-analysis)
5. [Output Interpretation](#output-interpretation)
6. [Common Scenarios](#common-scenarios)

## Basic Concepts

### Net vs Gross Withdrawals

The simulator focuses on **net withdrawals** - the amount you actually receive after taxes and fees. This is more relevant for retirement planning than gross amounts.

**Example:**
- You want €1,000/month net income
- The simulator calculates the gross withdrawal needed (e.g., €1,300)
- After taxes and fees, you receive exactly €1,000

### Investment Vehicles Compared

| Feature | Assurance-Vie (AV) | Compte-Titre Ordinaire (CTO) |
|---------|-------------------|------------------------------|
| **Tax on withdrawals** | Gains only (proportional) | Gains only (proportional) |
| **Tax rates** | 7.5% or 12.8% + 17.2% PS | 30% flat (12.8% + 17.2%) |
| **Annual allowance** | €4,600 single / €9,200 couple | None |
| **Management fees** | Annual % of assets | None typically |
| **Transaction fees** | None on withdrawals | Per transaction |
| **Minimum fees** | None | €3 per transaction (default) |

## Withdrawal Strategies

### 1. Percentage of Initial Capital

```bash
# 2.5% of initial €100k = €2,500/year = €208.33/month net
python av_vs_cto_simulator.py -i 100000 -w 2.5% --withdraw-on initial
```

**Pros:**
- Predictable annual income
- Preserves capital if returns > withdrawal rate
- Simple to understand

**Cons:**
- No inflation adjustment
- May exhaust capital if returns are poor

### 2. Percentage of Current Balance

```bash
# 2.5% of current balance each year (dynamic)
python av_vs_cto_simulator.py -i 100000 -w 2.5% --withdraw-on balance
```

**Pros:**
- Never fully exhausts capital
- Adjusts to market performance
- Sustainable indefinitely

**Cons:**
- Variable income year to year
- Lower income during market downturns

### 3. Fixed Monthly Amount

```bash
# Exactly €800/month net, regardless of balance
python av_vs_cto_simulator.py -i 200000 --withdraw-fixed 800
```

**Pros:**
- Completely predictable income
- Easy budgeting
- Independent of market volatility

**Cons:**
- May exhaust capital quickly
- No adjustment for inflation or market conditions

## Tax Optimization

### AV Premium Threshold Strategy

The €150,000 premium threshold creates different tax rates:

```bash
# Just under threshold - all gains taxed at 7.5%
python av_vs_cto_simulator.py -i 149000 -w 2.5%

# Above threshold - gains split between 7.5% and 12.8%
python av_vs_cto_simulator.py -i 200000 -w 2.5%
```

### Couple vs Single Taxation

```bash
# Single person (€4,600 allowance)
python av_vs_cto_simulator.py -i 150000 -w 3% --abatement 4600

# Married couple (€9,200 allowance)
python av_vs_cto_simulator.py -i 150000 -w 3% --abatement 9200
```

### Fee Impact Analysis

Compare different fee structures:

```bash
# Low-cost AV
python av_vs_cto_simulator.py -i 200000 -w 2.5% --av-fee 0.5%

# High-cost AV
python av_vs_cto_simulator.py -i 200000 -w 2.5% --av-fee 1.2%

# Expensive CTO transactions
python av_vs_cto_simulator.py -i 200000 -w 2.5% --cto-fee 0.1% --cto-min-fee 10
```

## Grid Analysis

Grid analysis helps find break-even points and optimal capital thresholds.

### Finding Break-even Points

```bash
# Where does AV become better than CTO?
python av_vs_cto_simulator.py -w 2.5% --years 15 \
    --grid 50000:300000:10000 --csv breakeven.csv --plot
```

The output CSV will show the difference (AV - CTO) for each capital level. Look for where the difference changes from negative to positive.

### Sensitivity Analysis

Test how different parameters affect the break-even:

```bash
# Higher fees scenario
python av_vs_cto_simulator.py -w 3% --years 20 --av-fee 1.0% \
    --grid 100000:500000:20000 --csv high_fees.csv

# Lower returns scenario  
python av_vs_cto_simulator.py -r 3% -w 2.5% --years 25 \
    --grid 100000:500000:20000 --csv low_returns.csv
```

## Output Interpretation

### Understanding the Results

```
AV : final capital = 89,234.56 € | cumulative net withdrawals = 25,000.00 € | taxes = 1,234.56 €
CTO: final capital = 87,456.78 € | cumulative net withdrawals = 25,000.00 € | taxes = 2,345.67 € | commissions = 234.56 €

Difference (AV − CTO) in total net wealth = 1,777.78 €
```

**Key Metrics:**
- **Final capital**: Remaining invested amount
- **Cumulative net withdrawals**: Total income received after taxes
- **Taxes**: Total tax burden over the period
- **Commissions**: Transaction fees (CTO only)
- **Total net wealth**: Final capital + cumulative withdrawals

### When AV is Better

AV typically outperforms when:
- Lower management fees (<1%)
- Longer time horizons (>15 years)
- Higher capital amounts (>€200k)
- Frequent withdrawals (CTO minimum fees matter)
- Married couple (higher allowance)

### When CTO is Better

CTO typically outperforms when:
- High AV management fees (>1.5%)
- Shorter time horizons (<10 years)
- Lower capital amounts (<€100k)
- Infrequent withdrawals
- Very low transaction costs

## Common Scenarios

### Early Retirement (Age 50-62)

```bash
# Bridge strategy until pension kicks in
python av_vs_cto_simulator.py -i 400000 --withdraw-fixed 2000 --years 12
```

### Traditional Retirement (Age 65+)

```bash
# Supplement pension income
python av_vs_cto_simulator.py -i 300000 -w 2% --years 25 --withdraw-on balance
```

### Wealth Preservation

```bash
# Minimal withdrawals for emergency fund
python av_vs_cto_simulator.py -i 500000 -w 1% --years 30 --withdraw-on balance
```

### High Net Worth

```bash
# Large portfolio with significant tax implications
python av_vs_cto_simulator.py -i 1000000 -w 3% --years 20 --abatement 9200
```

### Market Stress Testing

```bash
# Conservative returns assumption
python av_vs_cto_simulator.py -i 200000 -w 3% --years 20 -r 3%

# Poor market scenario
python av_vs_cto_simulator.py -i 200000 -w 3% --years 20 -r 2%
```

## Tips for Analysis

1. **Start with defaults**: Run basic comparison before adjusting parameters
2. **Use grid analysis**: Find break-even points for your situation
3. **Test fee sensitivity**: Small fee differences compound significantly
4. **Consider time horizon**: Tax advantages need time to compound
5. **Account for inflation**: Consider real returns and withdrawal needs
6. **Professional advice**: Use results to inform discussions with advisors

## Common Mistakes to Avoid

1. **Ignoring fees**: High management fees can eliminate AV tax advantages
2. **Wrong time horizon**: Short-term analysis favors CTO unfairly
3. **Gross vs net confusion**: Focus on net income for retirement planning
4. **Static analysis**: Consider how needs change over time
5. **Tax law changes**: Current rules may not persist indefinitely