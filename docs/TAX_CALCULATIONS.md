# Tax Calculations and Assumptions

## Overview

This document details the tax calculations implemented in the AV vs CTO simulator, based on French tax law as of 2024. Understanding these calculations is crucial for interpreting results and validating assumptions.

## Table of Contents

1. [Assurance-Vie (AV) Taxation](#assurance-vie-av-taxation)
2. [Compte-Titre Ordinaire (CTO) Taxation](#compte-titre-ordinaire-cto-taxation)
3. [Key Differences](#key-differences)
4. [Implementation Details](#implementation-details)
5. [Assumptions and Limitations](#assumptions-and-limitations)
6. [Validation Examples](#validation-examples)

## Assurance-Vie (AV) Taxation

### Prerequisites

- **Contract Age**: Must be >8 years old (assumed throughout)
- **Withdrawal Type**: Partial withdrawal (rachat partiel)
- **Tax Method**: Proportional method for determining taxable gains

### Tax Calculation Process

#### Step 1: Determine Gains Portion

For each withdrawal, only the **gains portion** is taxable:

```
Gains Portion = Withdrawal × (Unrealized Gains / Account Balance)

Where:
- Unrealized Gains = Current Balance - Premium Basis
- Premium Basis = Sum of all premiums paid (reduced by previous withdrawals)
```

#### Step 2: Premium Bucket Classification

Gains are taxed differently based on when premiums were paid:

- **≤€150,000 bucket**: Premiums up to €150,000 threshold
- **>€150,000 bucket**: Premiums above €150,000 threshold

**Tax Rates:**
- ≤€150k gains: **7.5% IR** + 17.2% social contributions = **24.7% total**
- >€150k gains: **12.8% IR** + 17.2% social contributions = **29.8% total**

#### Step 3: Annual Allowance Application

Each year, taxpayers receive an allowance that reduces **income tax only** (not social contributions):

- **Single person**: €4,600 per year
- **Married couple**: €9,200 per year (€4,600 each)

**Application order**:
1. Allowance applied first to 7.5% gains (better rate)
2. Remaining allowance applied to 12.8% gains
3. Social contributions unaffected by allowance

#### Example Calculation

**Scenario**: €200k initial premium, €250k current balance, €10k withdrawal

```
1. Gains portion: €10k × (€50k / €250k) = €2,000
2. Premium buckets: 
   - ≤€150k: €150k / €200k = 75% → €1,500 gains
   - >€150k: €50k / €200k = 25% → €500 gains
3. Before allowance:
   - 7.5% bucket: €1,500 × 7.5% = €112.50
   - 12.8% bucket: €500 × 12.8% = €64.00
   - Social contributions: €2,000 × 17.2% = €344.00
4. With €4,600 allowance (single):
   - 7.5% bucket: max(0, €112.50 - €4,600) = €0
   - 12.8% bucket: €64.00 (allowance already used)
   - Social contributions: €344.00 (unchanged)
   - Total tax: €0 + €64.00 + €344.00 = €408.00
```

### Implementation Notes

- **Monthly simulation**: Gains tracked throughout year, taxes calculated annually
- **Basis reduction**: Premium basis reduced by (withdrawal - gains) each month
- **Proportional method**: Always used (not FIFO or other methods)

## Compte-Titre Ordinaire (CTO) Taxation

### Tax Regime: PFU (Prélèvement Forfaitaire Unique)

CTO accounts are subject to the flat tax (PFU) regime:

**Flat Tax Rate**: **30% total**
- Income tax (IR): 12.8%
- Social contributions (PS): 17.2%

### Tax Calculation Process

#### Step 1: Determine Gains Portion

Similar to AV, only gains are taxable:

```
Gains Portion = Withdrawal × (Unrealized Gains / Account Balance)

Where:
- Unrealized Gains = Current Balance - Purchase Basis
- Purchase Basis = Original investment (reduced by previous withdrawals)
```

#### Step 2: Account for Transaction Fees

**Important**: Transaction fees reduce taxable gains:

```
Taxable Gains = max(0, Gains Portion - Transaction Fee)
```

This reflects the fact that fees are deductible expenses.

#### Step 3: Apply Flat Tax

```
Tax Due = Taxable Gains × 30%
```

**No allowances** or reductions available under PFU.

#### Example Calculation

**Scenario**: €100k initial investment, €120k current balance, €5k withdrawal, 0.1% + €5 transaction fee

```
1. Transaction fee: max(€5k × 0.1%, €5) = €5.00
2. Gains portion: €5k × (€20k / €120k) = €833.33
3. Taxable gains: max(0, €833.33 - €5.00) = €828.33
4. Tax due: €828.33 × 30% = €248.50
5. Net received: €5,000 - €5.00 - €248.50 = €4,746.50
```

### Implementation Notes

- **Annual taxation**: Gains accumulated throughout year, tax calculated annually
- **Fee deduction**: All transaction fees reduce taxable gains
- **No optimization**: Cannot elect for progressive tax scale in this simulation

## Key Differences

| Aspect | Assurance-Vie (AV) | CTO |
|--------|-------------------|-----|
| **Taxable amount** | Gains only (proportional) | Gains only (proportional) |
| **Tax rates** | 7.5%/12.8% + 17.2% | 12.8% + 17.2% (flat) |
| **Annual allowance** | €4,600/€9,200 on IR | None |
| **Premium thresholds** | €150k creates rate tiers | N/A |
| **Fee treatment** | Not deductible | Reduces taxable gains |
| **Minimum tax** | None | None |
| **Complexity** | High (multiple rates, allowances) | Low (single flat rate) |

## Implementation Details

### Net Withdrawal Solver

The simulator's key innovation is solving for the **gross withdrawal needed** to achieve a target **net amount**:

#### For AV:
```python
def solve_gross_withdrawal_av(target_net, balance_info, tax_info):
    # Binary search to find gross amount that yields target_net after:
    # 1. Proportional gains calculation
    # 2. Premium bucket allocation  
    # 3. Tax calculation with allowances
    # 4. Social contribution calculation
```

#### For CTO:
```python  
def solve_gross_withdrawal_cto(target_net, balance_info, tax_info):
    # Binary search to find gross amount that yields target_net after:
    # 1. Transaction fee calculation
    # 2. Proportional gains calculation
    # 3. Fee deduction from gains
    # 4. Flat tax application
```

This approach ensures both vehicles provide exactly the same net income for fair comparison.

### Monthly vs Annual Calculations

**Monthly simulation**:
- Investment growth applied monthly
- Management fees deducted monthly (AV only)
- Withdrawals processed monthly
- Transaction fees charged monthly (CTO only)

**Annual tax calculation**:
- Gains accumulated throughout year
- Taxes calculated once per year
- Net withdrawals credited based on gross withdrawals minus annual taxes

This reflects real-world timing where taxes are typically paid annually.

## Assumptions and Limitations

### Simplifying Assumptions

1. **Contract age >8 years**: All AV tax advantages apply
2. **Proportional method**: Used for all gain calculations
3. **No FIFO**: Contracts don't use first-in-first-out for tax purposes
4. **Annual allowance timing**: Applied optimally each year
5. **No tax payment timing**: Taxes paid exactly when calculated
6. **No inheritance**: Estate planning benefits not considered
7. **Current law**: 2024 tax rates assumed constant
8. **No alternative regimes**: PFU always used for CTO

### Known Limitations

1. **Real contracts may differ**: Specific terms may create variations
2. **Professional management**: Additional fees not modeled  
3. **Tax optimization**: Real-world strategies not implemented
4. **Regulatory changes**: Future law changes not predicted
5. **Currency effects**: International investments not considered
6. **Liquidity constraints**: Assumes unlimited liquidity in both vehicles

### Validation Against Real Scenarios

Users should validate results against:
- Actual contract terms and fee schedules
- Current tax declarations and calculations
- Professional tax advice for complex situations
- Regulatory updates and changes

## Validation Examples

### Example 1: Simple AV Calculation

**Given**:
- €100k premium (single bucket, ≤€150k)
- €150k current balance (€50k gains)
- €6k withdrawal
- Single person (€4,600 allowance)

**Manual calculation**:
```
1. Gains in withdrawal: €6k × (€50k/€150k) = €2k
2. IR before allowance: €2k × 7.5% = €150
3. IR after allowance: max(0, €150 - €4,600) = €0  
4. Social contributions: €2k × 17.2% = €344
5. Total tax: €0 + €344 = €344
6. Net received: €6k - €344 = €5,656
```

**Simulator verification**: Run with these parameters and confirm tax = €344

### Example 2: CTO with Minimum Fee

**Given**:
- €50k investment
- €60k current balance (€10k gains) 
- €1k withdrawal
- 0.1% fee with €5 minimum

**Manual calculation**:
```
1. Transaction fee: max(€1k × 0.1%, €5) = €5
2. Gains in withdrawal: €1k × (€10k/€60k) = €167
3. Taxable gains: max(0, €167 - €5) = €162
4. Tax: €162 × 30% = €49
5. Net received: €1k - €5 - €49 = €946
```

**Simulator verification**: Run with these parameters and confirm net ≈ €946

### Example 3: Mixed Premium Buckets

**Given**:
- €200k total premiums (€150k + €50k buckets)
- €300k current balance (€100k gains)
- €15k withdrawal  
- Married couple (€9,200 allowance)

**Manual calculation**:
```
1. Gains in withdrawal: €15k × (€100k/€300k) = €5k
2. Bucket allocation:
   - ≤€150k: €5k × (€150k/€200k) = €3,750
   - >€150k: €5k × (€50k/€200k) = €1,250
3. IR before allowance:
   - 7.5% bucket: €3,750 × 7.5% = €281
   - 12.8% bucket: €1,250 × 12.8% = €160
   - Total IR: €441
4. IR after allowance: max(0, €441 - €9,200) = €0
5. Social contributions: €5k × 17.2% = €860
6. Total tax: €0 + €860 = €860
7. Net received: €15k - €860 = €14,140
```

**Simulator verification**: Run with --abatement 9200 and confirm results

## Professional Use

### For Tax Advisors

This simulator can help:
- Illustrate tax differences to clients
- Model different withdrawal strategies  
- Demonstrate impact of fees on net returns
- Support product selection discussions

**Important**: Always verify against current tax law and specific client circumstances.

### For Financial Advisors

Use cases include:
- Retirement income planning
- Product comparison analysis
- Fee impact demonstration
- Client education on tax efficiency

**Disclaimer**: This tool provides estimates based on assumptions. Professional advice should always consider individual circumstances and current regulations.

### Regulatory Compliance

This simulator is:
- ✅ Educational tool for analysis
- ✅ Based on publicly available tax rules
- ❌ Not official tax advice
- ❌ Not guaranteed to be current or complete
- ❌ Not a substitute for professional consultation

Always consult qualified tax professionals for official advice.