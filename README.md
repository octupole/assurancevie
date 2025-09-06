# AV vs CTO Retirement Simulator 🇫🇷

A Python simulator for comparing **Assurance-Vie (AV)** and **Compte-Titre Ordinaire (CTO)** investment strategies under French taxation, specifically designed for retirement planning with regular withdrawals.

## 🎯 Overview

This simulator helps French investors compare two popular retirement investment vehicles:

- **Assurance-Vie (AV)**: Life insurance contracts with tax advantages after 8+ years
- **Compte-Titre Ordinaire (CTO)**: Regular investment accounts under PFU (flat tax) regime

The tool simulates monthly withdrawals over a specified time horizon, accounting for French tax rules, fees, and different withdrawal strategies.

## ✨ Key Features

- **Net Withdrawal Focus**: Specify your desired net income after taxes
- **Flexible Withdrawal Options**: Percentage-based or fixed monthly amounts
- **French Tax Compliance**: Accurate implementation of AV and CTO tax rules
- **Break-even Analysis**: Grid analysis to find optimal investment thresholds
- **Visual Analytics**: Optional matplotlib charts and CSV export
- **Comprehensive Reporting**: Detailed breakdown of taxes, fees, and final wealth

## 🚀 Quick Start

### Basic Usage

```bash
# Compare €100k investment with 2.5% annual net withdrawals over 10 years
python av_vs_cto_simulator.py -i 100000 -w 2.5% --years 10

# Fixed monthly withdrawals of €1000
python av_vs_cto_simulator.py -i 150000 --withdraw-fixed 1000 --years 15

# Generate CSV report and chart
python av_vs_cto_simulator.py -i 200000 -w 3% --years 20 --csv results.csv --plot
```

### Grid Analysis

Find break-even points across different capital amounts:

```bash
# Analyze €50k to €500k range in €25k steps
python av_vs_cto_simulator.py -w 2.5% --years 20 \
    --grid 50000:500000:25000 --csv grid_analysis.csv --plot
```

## 📊 Sample Output

```
--- Parameters ---
Initial capital: 100,000.00 €
Horizon: 10 years | Return: 5.000 %/year
NET withdrawals: 2.500 %/year on initial
AV: fees 0.750 %/year | IR 7.5% / 12.8% | premium threshold 150,000 € | allowance 4,600 €
CTO: commission 0.00800 %/withdrawal (min 3.00€) | PFU = IR 12.8% + PS 17.2% = 30.0%

--- Results over horizon ---
AV : final capital = 89,234.56 € | cumulative net withdrawals = 25,000.00 € | taxes = 1,234.56 €
CTO: final capital = 87,456.78 € | cumulative net withdrawals = 25,000.00 € | taxes = 2,345.67 € | commissions = 234.56 €

Difference (AV − CTO) in total net wealth = 1,777.78 €
```

## 🛠 Installation

### Requirements

- Python 3.8+
- Core dependencies: `argparse`, `dataclasses` (built-in)
- Optional: `pandas` (for CSV/grid analysis), `matplotlib` (for charts)

### Install Optional Dependencies

```bash
pip install pandas matplotlib
```

### Download

```bash
git clone https://github.com/octupole/myretirement.git
cd av-cto-simulator
```

## 📚 Documentation

### Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `-i, --initial` | Starting capital (€) | 100,000 |
| `-r, --annual-return` | Annual gross return rate | 5% |
| `-y, --years` | Time horizon in years | 10 |
| `-w, --withdraw-rate` | Annual NET withdrawal rate | 2.5% |
| `--withdraw-fixed` | Fixed monthly NET amount (€) | - |
| `--withdraw-on` | Withdrawal base: `initial` or `balance` | initial |

#### Fee Parameters

| Argument | Description | Default |
|----------|-------------|---------|
| `--av-fee` | AV management fees per year | 0.75% |
| `--cto-fee` | CTO commission per withdrawal | 0.008% |
| `--cto-min-fee` | Minimum CTO commission (€) | 3 |

#### Tax Parameters

| Argument | Description | Default |
|----------|-------------|---------|
| `--ps-rate` | Social contributions rate | 17.2% |
| `--pfu-ir` | PFU income tax portion | 12.8% |
| `--av-ir-low` | AV IR for ≤€150k premiums | 7.5% |
| `--av-ir-high` | AV IR for >€150k premiums | 12.8% |
| `--av-threshold` | Premium threshold | €150,000 |
| `--abatement` | Annual AV IR allowance | €4,600 |

#### Analysis Options

| Argument | Description |
|----------|-------------|
| `--grid min:max:step` | Grid analysis range |
| `--csv filename` | Export results to CSV |
| `--plot` | Generate matplotlib chart |

## 🧮 Tax Calculation Details

### Assurance-Vie (AV) - After 8 Years

- **Management Fees**: Applied annually to account balance
- **Withdrawal Taxation**: Only gains portion is taxed (proportional method)
- **Tax Rates**: 
  - ≤€150k premiums: 7.5% IR + 17.2% social contributions
  - >€150k premiums: 12.8% IR + 17.2% social contributions
- **Annual Allowance**: €4,600 (single) / €9,200 (couple) on IR only
- **No Transaction Fees**: On withdrawals

### Compte-Titre Ordinaire (CTO)

- **Transaction Fees**: Commission per withdrawal (percentage + minimum)
- **Taxation**: PFU flat tax on gains only
- **Tax Rate**: 30% total (12.8% IR + 17.2% social contributions)
- **No Allowances**: All gains taxed at flat rate
- **Fee Impact**: Transaction fees reduce taxable gains

## 💡 Use Cases

### 1. Retirement Planning

Compare which vehicle provides better net income for your retirement:

```bash
# Retired couple with €300k, needing €1,200/month
python av_vs_cto_simulator.py -i 300000 --withdraw-fixed 1200 --years 25 --abatement 9200
```

### 2. Wealth Preservation

Analyze long-term wealth preservation with minimal withdrawals:

```bash
# Conservative 1.5% withdrawal rate over 30 years
python av_vs_cto_simulator.py -i 500000 -w 1.5% --years 30 --withdraw-on balance
```

### 3. Break-even Analysis

Find the capital threshold where AV becomes advantageous:

```bash
# High-fee AV scenario
python av_vs_cto_simulator.py --av-fee 1.5% -w 3% --years 15 \
    --grid 100000:1000000:50000 --csv breakeven.csv
```

## 📈 Advanced Features

### Grid Analysis

The `--grid` option performs analysis across multiple capital amounts to identify break-even points and optimal thresholds.

Output includes:
- All simulation parameters and results for each capital amount
- Difference calculation (AV - CTO)
- CSV export with complete data
- Optional visualization of the difference curve

### Net Withdrawal System

The simulator automatically calculates the gross withdrawal needed to achieve your target net amount, accounting for:
- Tax on gains portion
- Transaction fees (CTO only)
- Annual allowances (AV only)
- Different tax rates for different premium buckets (AV)

## ⚠️ Important Notes

1. **Tax Assumptions**: Based on current French tax law (2024)
2. **AV Contract Age**: Assumes contracts are >8 years old
3. **No Inheritance**: Simulation doesn't account for inheritance tax advantages
4. **Simplified Model**: Real contracts may have additional fees or constraints
5. **Professional Advice**: This tool is for educational purposes; consult tax professionals

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional French investment vehicles (PEA, PER)
- Inheritance tax calculations
- More sophisticated fee models
- Additional tax scenarios

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

- Create an issue for bugs or feature requests
- Check existing issues before creating new ones
- Provide sample commands that reproduce any problems

---
