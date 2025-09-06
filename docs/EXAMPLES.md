# Examples and Use Cases

## Quick Reference Examples

### Basic Comparisons

#### Example 1: Standard Retirement Scenario
```bash
python av_vs_cto_simulator.py -i 250000 -w 2.5% --years 20
```

**Scenario**: €250k investment, 2.5% annual withdrawals for 20 years
**Expected**: Likely AV advantage due to tax allowances and reasonable time horizon

#### Example 2: Early Retirement with High Withdrawals
```bash
python av_vs_cto_simulator.py -i 400000 -w 4% --years 15 --abatement 9200
```

**Scenario**: Married couple, €400k, 4% withdrawals, 15-year bridge to pension
**Expected**: AV advantage amplified by higher allowance and frequent withdrawals

#### Example 3: Conservative Wealth Preservation
```bash
python av_vs_cto_simulator.py -i 500000 -w 1.5% --years 30 --withdraw-on balance
```

**Scenario**: Large portfolio, minimal withdrawals, balance-based (never exhausts)
**Expected**: AV advantage grows over long time horizon

### Fixed Monthly Income Examples

#### Example 4: Predictable Retirement Income
```bash
python av_vs_cto_simulator.py -i 300000 --withdraw-fixed 1200 --years 25
```

**Scenario**: Need exactly €1,200/month net for 25 years
**Expected**: Shows how long each account lasts with fixed withdrawals

#### Example 5: Supplemental Income
```bash
python av_vs_cto_simulator.py -i 150000 --withdraw-fixed 500 --years 20
```

**Scenario**: Supplement pension with €500/month from savings
**Expected**: AV likely better due to allowances offsetting smaller capital

### Fee Sensitivity Analysis

#### Example 6: Low-Cost AV vs CTO
```bash
python av_vs_cto_simulator.py -i 200000 -w 3% --av-fee 0.5% --years 15
```

**Scenario**: Excellent AV contract with 0.5% fees
**Expected**: Strong AV advantage

#### Example 7: High-Cost AV vs CTO
```bash
python av_vs_cto_simulator.py -i 200000 -w 3% --av-fee 1.5% --years 15
```

**Scenario**: Expensive AV contract with 1.5% fees
**Expected**: CTO may be competitive or better

#### Example 8: Expensive CTO Transactions
```bash
python av_vs_cto_simulator.py -i 100000 -w 3% --cto-fee 0.05% --cto-min-fee 15 --years 20
```

**Scenario**: High transaction costs (0.05% + €15 minimum)
**Expected**: AV advantage increases significantly

## Comprehensive Analysis Examples

### Example 9: Complete Break-even Analysis
```bash
python av_vs_cto_simulator.py -w 2.5% --years 20 --grid 50000:500000:25000 --csv breakeven.csv --plot
```

**Purpose**: Find the capital threshold where AV becomes advantageous
**Output**: CSV with differences across capital range, visual chart
**Analysis**: Look for where difference (AV-CTO) turns positive

### Example 10: Time Horizon Sensitivity
```bash
# Short term (5 years)
python av_vs_cto_simulator.py -i 200000 -w 3% --years 5 --csv short_term.csv

# Medium term (15 years)  
python av_vs_cto_simulator.py -i 200000 -w 3% --years 15 --csv medium_term.csv

# Long term (30 years)
python av_vs_cto_simulator.py -i 200000 -w 3% --years 30 --csv long_term.csv
```

**Purpose**: See how time horizon affects the comparison
**Expected**: AV advantage increases with longer horizons

### Example 11: Market Conditions Analysis
```bash
# Bull market scenario
python av_vs_cto_simulator.py -i 300000 -w 2.5% -r 7% --years 20 --csv bull_market.csv

# Normal market scenario
python av_vs_cto_simulator.py -i 300000 -w 2.5% -r 5% --years 20 --csv normal_market.csv

# Bear market scenario
python av_vs_cto_simulator.py -i 300000 -w 2.5% -r 3% --years 20 --csv bear_market.csv
```

**Purpose**: Test robustness across different return environments
**Analysis**: Compare relative advantages across scenarios

## Real-World Scenarios

### Scenario A: The Cautious Retiree

**Profile**: 
- Age 65, conservative investor
- €180k in savings
- Wants €600/month supplemental income
- Married couple
- Risk-averse, prefers predictability

```bash
python av_vs_cto_simulator.py -i 180000 --withdraw-fixed 600 --years 25 -r 4% --abatement 9200 --csv cautious_retiree.csv
```

**Analysis Points**:
- Fixed income provides certainty
- 25-year horizon allows AV advantages to compound  
- Conservative 4% return assumption
- Married couple gets higher allowance

### Scenario B: The Early Retiree

**Profile**:
- Age 50, wants to retire early
- €450k accumulated
- Needs €2,000/month until age 67
- Single person
- Willing to take some market risk

```bash
python av_vs_cto_simulator.py -i 450000 --withdraw-fixed 2000 --years 17 -r 5.5% --abatement 4600 --csv early_retiree.csv
```

**Analysis Points**:
- High withdrawal rate tests sustainability
- Medium-term horizon (17 years)
- Higher return assumption for growth investments
- Single person allowance

### Scenario C: The High Net Worth Individual

**Profile**:
- Age 55, wealthy professional
- €800k to invest
- Conservative 2% withdrawal rate
- Married couple
- Focused on wealth preservation

```bash
python av_vs_cto_simulator.py -i 800000 -w 2% --years 30 -r 6% --abatement 9200 --withdraw-on balance --csv high_net_worth.csv
```

**Analysis Points**:
- Low withdrawal rate for sustainability
- Long horizon maximizes tax advantages
- Balance-based withdrawals never exhaust capital
- Large capital makes fee differences significant

### Scenario D: The Fee-Sensitive Investor

**Profile**:
- Comparing two specific products
- €200k to invest
- Standard retirement needs
- Concerned about costs

```bash
# Option 1: Premium AV with low fees
python av_vs_cto_simulator.py -i 200000 -w 2.5% --years 20 --av-fee 0.6% --csv premium_av.csv

# Option 2: Standard AV with typical fees  
python av_vs_cto_simulator.py -i 200000 -w 2.5% --years 20 --av-fee 0.9% --csv standard_av.csv

# Option 3: Low-cost CTO
python av_vs_cto_simulator.py -i 200000 -w 2.5% --years 20 --cto-fee 0.005% --cto-min-fee 2 --csv low_cost_cto.csv
```

**Analysis Points**:
- Direct comparison of actual products
- Same parameters except fees
- Quantifies cost impact over time

## Advanced Analysis Examples

### Example 12: Monte Carlo-Style Analysis

Simulate different market conditions:

```bash
# Create multiple scenarios with different return assumptions
for return in 3 4 5 6 7; do
    python av_vs_cto_simulator.py -i 300000 -w 3% --years 20 -r ${return}% --csv returns_${return}pct.csv
done
```

**Purpose**: Understand sensitivity to market returns
**Analysis**: Compare results across return scenarios

### Example 13: Lifecycle Strategy Analysis

```bash
# Phase 1: Accumulation (age 50-65)
python av_vs_cto_simulator.py -i 400000 -w 1% --years 15 -r 6% --csv accumulation.csv

# Phase 2: Early retirement (age 65-75)  
python av_vs_cto_simulator.py -i 500000 -w 3% --years 10 -r 5% --csv early_retirement.csv

# Phase 3: Late retirement (age 75+)
python av_vs_cto_simulator.py -i 400000 -w 4% --years 15 -r 4% --csv late_retirement.csv
```

**Purpose**: Model different life phases with different needs
**Analysis**: Optimal strategy may change over time

### Example 14: Tax Law Change Sensitivity

```bash
# Current tax rates
python av_vs_cto_simulator.py -i 250000 -w 2.5% --years 20 --csv current_tax.csv

# Pessimistic scenario (higher taxes)
python av_vs_cto_simulator.py -i 250000 -w 2.5% --years 20 --av-ir-low 10% --av-ir-high 15% --pfu-ir 15% --csv higher_tax.csv

# Optimistic scenario (lower taxes)
python av_vs_cto_simulator.py -i 250000 -w 2.5% --years 20 --av-ir-low 5% --av-ir-high 10% --pfu-ir 10% --csv lower_tax.csv
```

**Purpose**: Test robustness to potential tax law changes
**Analysis**: How sensitive are results to tax policy?

## Batch Analysis Scripts

### Creating Comparison Reports

```bash
#!/bin/bash
# compare_scenarios.sh

CAPITAL=200000
YEARS=20
WITHDRAWAL=2.5%

echo "Generating comparison reports..."

# Base case
python av_vs_cto_simulator.py -i $CAPITAL -w $WITHDRAWAL --years $YEARS --csv base_case.csv

# Sensitivity tests
python av_vs_cto_simulator.py -i $CAPITAL -w $WITHDRAWAL --years $YEARS --av-fee 0.5% --csv low_fees.csv
python av_vs_cto_simulator.py -i $CAPITAL -w $WITHDRAWAL --years $YEARS --av-fee 1.5% --csv high_fees.csv
python av_vs_cto_simulator.py -i $CAPITAL -w $WITHDRAWAL --years $YEARS -r 3% --csv low_returns.csv
python av_vs_cto_simulator.py -i $CAPITAL -w $WITHDRAWAL --years $YEARS -r 7% --csv high_returns.csv

echo "Analysis complete. Check CSV files for results."
```

### Grid Analysis for Multiple Parameters

```bash
#!/bin/bash
# comprehensive_analysis.sh

echo "Running comprehensive break-even analysis..."

# Different withdrawal rates
for rate in 2.0 2.5 3.0 3.5; do
    python av_vs_cto_simulator.py -w ${rate}% --years 20 --grid 100000:400000:20000 --csv grid_${rate}pct.csv
done

# Different time horizons
for years in 10 15 20 25; do
    python av_vs_cto_simulator.py -w 2.5% --years $years --grid 100000:400000:20000 --csv grid_${years}years.csv  
done

echo "Grid analysis complete. Check CSV files for break-even points."
```

## Interpreting Results

### Key Questions to Ask

1. **Which vehicle provides better total wealth?** Look at the final difference
2. **How sensitive is the result to fees?** Compare different fee scenarios
3. **What's the break-even capital amount?** Use grid analysis
4. **How does time horizon affect the choice?** Test different periods
5. **What if market returns are lower?** Stress test with conservative assumptions

### Red Flags in Results

- **Extreme differences**: Very large differences may indicate input errors
- **Counter-intuitive results**: CTO winning with high AV fees is expected, but other surprises warrant investigation  
- **Unrealistic assumptions**: Check if withdrawal rates are sustainable
- **Tax inconsistencies**: Verify tax parameters match your situation

### Next Steps

After running analyses:
1. **Identify clear winners**: Scenarios where one vehicle is clearly better
2. **Find break-even points**: Capital amounts where choice matters less
3. **Consider real-world factors**: Liquidity, estate planning, complexity
4. **Seek professional advice**: Use results to inform discussions with advisors
5. **Monitor assumptions**: Review periodically as laws and fees change