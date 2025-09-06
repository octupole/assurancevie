#!/usr/bin/env python3
"""
Assurance-Vie (>8 years) vs CTO (PFU) Simulator for France

Default assumptions (modifiable via CLI):
- Gross returns compounded monthly
- Equal net monthly withdrawals: either annual rate on capital, or fixed monthly amount
- System automatically calculates gross withdrawal needed to achieve net target amount
- AV: annual management fees, no withdrawal fees
- CTO: transaction commission per withdrawal, PFU 30% (IR 12.8% + PS 17.2%)
- AV > 8 years: taxation on GAINS PORTION of withdrawal (proportional method),
  annual IR allowance (default €4,600 single), PS not reduced by allowance.
- €150k premium threshold: gains attributed first to ≤€150k bucket (IR 7.5%),
  then to >€150k bucket (IR 12.8%). Allowance applied first to 7.5%.

Outputs:
- Single summary (AV vs CTO) for given starting capital
- Optional: grid over capital range to analyze break-even points
- CSV export and (optional) matplotlib chart of AV–CTO difference

Examples:
  # Withdrawal of 2.5% net per year from initial capital
  python av_vs_cto_simulator.py -i 100000 -r 5% -w 2.5% --years 10 \
      --av-fee 0.75% --cto-fee 0.008% --csv out.csv --plot

  # Fixed withdrawal of €1000 net per month
  python av_vs_cto_simulator.py -i 100000 -r 5% --withdraw-fixed 1000 --years 10 \
      --av-fee 0.75% --cto-fee 0.008%

  # Grid 10k→1M to find break-even point (no break-even expected with 0.75%):
  python av_vs_cto_simulator.py -r 5% -w 2.5% --years 20 --grid 10000:1000000:10000 \
      --av-fee 0.75% --cto-fee 0.008% --csv grid.csv --plot

Author: you 😊
"""
from __future__ import annotations
import argparse
import math
from dataclasses import dataclass, asdict
from typing import Tuple, List, Optional

try:
    import pandas as pd  # facultatif, requis si --csv ou --grid
except Exception:
    pd = None

# ---------------------- Utils ----------------------


def parse_rate(s: str) -> float:
    """Converts '5%' -> 0.05, '0.05' -> 0.05, '0,75%' -> 0.0075.
    Also accepts '5' (interpreted as 5%)."""
    s = s.strip().replace(',', '.')
    if s.endswith('%'):
        return float(s[:-1]) / 100.0
    # If user writes '5' we assume 5%
    val = float(s)
    return val/100.0


def parse_grid(s: str) -> Tuple[float, float, float]:
    """Parse 'min:max:step' into three floats.
    
    Allows analysis of AV vs CTO simulation over a grid of initial capitals
    to identify break-even points or analyze how advantage changes
    according to investment size.
    
    Examples:
    - "10000:1000000:10000" → (10000.0, 1000000.0, 10000.0)
    - "50000:500000:25000" → (50000.0, 500000.0, 25000.0)
    """
    parts = s.split(':')
    if len(parts) != 3:
        raise argparse.ArgumentTypeError(
            "--grid expected in format min:max:step")
    a, b, c = map(lambda x: float(x.replace(',', '.')), parts)
    if c <= 0:
        raise argparse.ArgumentTypeError("step must be > 0")
    return a, b, c


def solve_gross_withdrawal_av(target_net: float, bal_low: float, bal_high: float, 
                             basis_low: float, basis_high: float, inp: Inputs, 
                             gains_withdrawn_year_low: float, gains_withdrawn_year_high: float) -> float:
    """Solves for the gross withdrawal needed to achieve a target net withdrawal for AV."""
    if target_net <= 0:
        return 0.0
    
    # Initial estimate: assume average effective tax rate
    estimated_tax_rate = 0.15  # rough estimate
    gross_estimate = target_net / (1 - estimated_tax_rate)
    
    # Binary search to find optimal gross withdrawal
    low_gross = target_net  # minimum possible
    high_gross = target_net * 2  # maximum reasonable
    
    for _ in range(20):  # max 20 iterations
        test_gross = (low_gross + high_gross) / 2
        total_bal = bal_low + bal_high
        if total_bal <= 0:
            return 0.0
            
        w_low = test_gross * (bal_low / total_bal)
        w_high = test_gross * (bal_high / total_bal)
        
        # Calculate gains in this withdrawal
        gain_low = max(0.0, bal_low - basis_low)
        gain_high = max(0.0, bal_high - basis_high)
        g_withdraw_low = w_low * (gain_low / bal_low) if bal_low > 0 else 0.0
        g_withdraw_high = w_high * (gain_high / bal_high) if bal_high > 0 else 0.0
        
        # Calculate taxes on these gains
        total_gains_year = gains_withdrawn_year_low + gains_withdrawn_year_high + g_withdraw_low + g_withdraw_high
        ps = inp.ps_rate * total_gains_year
        
        # IR allowance
        remaining = inp.av_abatement_ir
        base_ir_low = max(0.0, gains_withdrawn_year_low + g_withdraw_low)
        use_low = min(remaining, base_ir_low)
        base_ir_low -= use_low
        remaining -= use_low
        
        base_ir_high = max(0.0, gains_withdrawn_year_high + g_withdraw_high)
        use_high = min(remaining, base_ir_high)
        base_ir_high -= use_high
        
        ir = base_ir_low * inp.av_ir_low + base_ir_high * inp.av_ir_high
        taxes = ps + ir
        
        net_result = test_gross - taxes
        
        if abs(net_result - target_net) < 0.01:  # precision of 1 cent
            return test_gross
        elif net_result < target_net:
            low_gross = test_gross
        else:
            high_gross = test_gross
    
    return (low_gross + high_gross) / 2


def solve_gross_withdrawal_cto(target_net: float, bal: float, basis: float, 
                              inp: Inputs, gains_withdrawn_year: float) -> float:
    """Solves for the gross withdrawal needed to achieve a target net withdrawal for CTO."""
    if target_net <= 0 or bal <= 0:
        return 0.0
    
    # Binary search
    low_gross = target_net
    high_gross = target_net * 2
    
    for _ in range(20):  # max 20 iterations
        test_gross = (low_gross + high_gross) / 2
        
        # Calculate commission
        fee = max(inp.cto_fee_rate * test_gross, inp.cto_min_fee)
        
        # Calculate gains in this withdrawal
        gain = max(0.0, bal - basis)
        g_withdraw = test_gross * (gain / bal) if bal > 0 else 0.0
        
        # Taxable gains after commission
        realized_gain = max(0.0, g_withdraw - fee)
        total_gains_year = gains_withdrawn_year + realized_gain
        
        # Taxes
        taxes = total_gains_year * inp.pfu_total_cto
        
        net_result = test_gross - taxes - fee
        
        if abs(net_result - target_net) < 0.01:  # precision of 1 cent
            return test_gross
        elif net_result < target_net:
            low_gross = test_gross
        else:
            high_gross = test_gross
    
    return (low_gross + high_gross) / 2


# ---------------------- Model ----------------------

@dataclass
class Inputs:
    initial: float
    annual_return: float          # ex: 0.05 for 5%
    years: int                    # time horizon in years
    withdraw_rate_annual: float   # ex: 0.025 for 2.5%/year (ignored if withdraw_fixed_monthly)
    withdraw_fixed_monthly: float # fixed monthly net amount, ex: 1000.0 (None to disable)
    withdraw_on_initial: bool     # True = % of initial, False = % of current balance
    av_fee_annual: float          # ex: 0.0075 for 0.75%
    cto_fee_rate: float           # commission per withdrawal, ex: 0.00008 for 0.008%
    cto_min_fee: float            # minimum commission per withdrawal, ex: 3.0 for €3
    ps_rate: float                # social contributions (ex: 0.172)
    pfu_ir_rate: float            # IR portion of PFU (ex: 0.128)
    av_ir_low: float              # 0.075
    av_ir_high: float             # 0.128
    av_premium_threshold: float   # 150_000
    av_abatement_ir: float        # 4600 (single person)

    @property
    def months(self) -> int:
        return self.years * 12

    @property
    def monthly_return(self) -> float:
        return (1 + self.annual_return) ** (1/12) - 1

    @property
    def av_monthly_fee(self) -> float:
        return self.av_fee_annual / 12.0

    @property
    def pfu_total_cto(self) -> float:
        return self.ps_rate + self.pfu_ir_rate


@dataclass
class Outputs:
    end_balance_av: float
    end_balance_cto: float
    cum_net_withdraw_av: float
    cum_net_withdraw_cto: float
    taxes_paid_av: float
    taxes_paid_cto: float
    fees_cto: float

    @property
    def total_wealth_av(self) -> float:
        return self.end_balance_av + self.cum_net_withdraw_av

    @property
    def total_wealth_cto(self) -> float:
        return self.end_balance_cto + self.cum_net_withdraw_cto

    @property
    def diff_av_minus_cto(self) -> float:
        return self.total_wealth_av - self.total_wealth_cto


# ---------------------- Core Simulation ----------------------

def simulate_av(inp: Inputs) -> Tuple[float, float, float]:
    """Returns (end_balance, cum_net_withdraw, taxes_paid)."""
    # Two premium buckets to handle 7.5% / 12.8% rates
    prem_low = min(inp.initial, inp.av_premium_threshold)
    prem_high = max(0.0, inp.initial - inp.av_premium_threshold)

    bal_low, bal_high = prem_low, prem_high
    basis_low, basis_high = prem_low, prem_high

    cum_net_withdraw = 0.0
    taxes_paid = 0.0

    gains_withdrawn_year_low = 0.0
    gains_withdrawn_year_high = 0.0

    if inp.withdraw_fixed_monthly is not None:
        monthly_withdraw_net_target = inp.withdraw_fixed_monthly
    else:
        monthly_withdraw_net_target = inp.initial * inp.withdraw_rate_annual / 12.0

    for m in range(1, inp.months + 1):
        # Performance then management fees
        bal_low *= (1 + inp.monthly_return)
        bal_high *= (1 + inp.monthly_return)
        bal_low *= (1 - inp.av_monthly_fee)
        bal_high *= (1 - inp.av_monthly_fee)

        total_bal = bal_low + bal_high
        if total_bal <= 0:
            break

        # Amount to withdraw this month (net target)
        if inp.withdraw_fixed_monthly is not None:
            target_net = inp.withdraw_fixed_monthly
        elif inp.withdraw_on_initial:
            target_net = monthly_withdraw_net_target
        else:
            target_net = total_bal * (inp.withdraw_rate_annual/12.0)
        
        # Solve for gross withdrawal needed to achieve net target
        w = solve_gross_withdrawal_av(target_net, bal_low, bal_high, basis_low, basis_high, 
                                     inp, gains_withdrawn_year_low, gains_withdrawn_year_high)
        w_low = w * (bal_low / total_bal) if total_bal > 0 else 0.0
        w_high = w * (bal_high / total_bal) if total_bal > 0 else 0.0

        # Gains portion of withdrawal (proportional method)
        gain_low = max(0.0, bal_low - basis_low)
        gain_high = max(0.0, bal_high - basis_high)
        g_withdraw_low = w_low * (gain_low / bal_low) if bal_low > 0 else 0.0
        g_withdraw_high = w_high * \
            (gain_high / bal_high) if bal_high > 0 else 0.0

        # Apply withdrawal
        bal_low -= w_low
        bal_high -= w_high

        # Reduce capital basis
        basis_low = max(0.0, basis_low - (w_low - g_withdraw_low))
        basis_high = max(0.0, basis_high - (w_high - g_withdraw_high))

        # Track gains withdrawn for the year
        gains_withdrawn_year_low += g_withdraw_low
        gains_withdrawn_year_high += g_withdraw_high

        # Annual tax closing
        if m % 12 == 0:
            # PS 17.2% on all withdrawn gains
            ps = inp.ps_rate * (gains_withdrawn_year_low +
                                gains_withdrawn_year_high)

            # IR allowance first at 7.5%, then 12.8% (convention)
            remaining = inp.av_abatement_ir
            base_ir_low = max(0.0, gains_withdrawn_year_low)
            use_low = min(remaining, base_ir_low)
            base_ir_low -= use_low
            remaining -= use_low

            base_ir_high = max(0.0, gains_withdrawn_year_high)
            use_high = min(remaining, base_ir_high)
            base_ir_high -= use_high
            remaining -= use_high

            ir = base_ir_low * inp.av_ir_low + base_ir_high * inp.av_ir_high
            taxes = ps + ir
            taxes_paid += taxes

            # Annual net income received = net target (directly)
            # Gross withdrawal was calculated to achieve this net target
            if inp.withdraw_fixed_monthly is not None:
                net_year = inp.withdraw_fixed_monthly * 12.0
            elif inp.withdraw_on_initial:
                net_year = monthly_withdraw_net_target * 12.0
            else:
                # if withdrawals % of balance, approx: take variable monthly sum
                net_year = target_net * 12.0
            cum_net_withdraw += net_year

            # reset annual totals
            gains_withdrawn_year_low = 0.0
            gains_withdrawn_year_high = 0.0

    return bal_low + bal_high, cum_net_withdraw, taxes_paid


def simulate_cto(inp: Inputs) -> Tuple[float, float, float, float]:
    """Returns (end_balance, cum_net_withdraw, taxes_paid, fees_cto)."""
    bal = inp.initial
    basis = inp.initial

    cum_net_withdraw = 0.0
    taxes_paid = 0.0
    fees_paid = 0.0

    if inp.withdraw_fixed_monthly is not None:
        monthly_withdraw_net_target = inp.withdraw_fixed_monthly
    else:
        monthly_withdraw_net_target = inp.initial * inp.withdraw_rate_annual / 12.0
    gains_withdrawn_year = 0.0
    fees_paid_year = 0.0

    for m in range(1, inp.months + 1):
        # Monthly performance
        bal *= (1 + inp.monthly_return)
        if bal <= 0:
            break

        # Net target amount this month
        if inp.withdraw_fixed_monthly is not None:
            target_net = inp.withdraw_fixed_monthly
        elif inp.withdraw_on_initial:
            target_net = monthly_withdraw_net_target
        else:
            target_net = bal * (inp.withdraw_rate_annual/12.0)

        # Solve for gross withdrawal needed to achieve net target
        w = solve_gross_withdrawal_cto(target_net, bal, basis, inp, gains_withdrawn_year)

        # Commission (charged in addition to withdrawal)
        fee = max(inp.cto_fee_rate * w, inp.cto_min_fee)
        fees_paid += fee
        fees_paid_year += fee

        # Proportional gains portion in w
        gain = max(0.0, bal - basis)
        g_withdraw = w * (gain / bal) if bal > 0 else 0.0

        # Cash outflow + commission
        bal -= (w + fee)

        # Adjust basis
        basis = max(0.0, basis - (w - g_withdraw))

        # Commission reduces the realized taxable gain
        realized_gain = max(0.0, g_withdraw - fee)
        gains_withdrawn_year += realized_gain

        # Annual tax closing
        if m % 12 == 0:
            taxes = gains_withdrawn_year * inp.pfu_total_cto
            taxes_paid += taxes

            # Net received = net target (directly)
            # Gross withdrawal was calculated to achieve this net target
            if inp.withdraw_fixed_monthly is not None:
                net_year = inp.withdraw_fixed_monthly * 12.0
            elif inp.withdraw_on_initial:
                net_year = monthly_withdraw_net_target * 12.0
            else:
                net_year = target_net * 12.0
            cum_net_withdraw += net_year
            gains_withdrawn_year = 0.0
            fees_paid_year = 0.0

    return bal, cum_net_withdraw, taxes_paid, fees_paid


def run_single(inp: Inputs) -> Outputs:
    end_av, net_av, tax_av = simulate_av(inp)
    end_cto, net_cto, tax_cto, fees_cto = simulate_cto(inp)
    return Outputs(
        end_balance_av=end_av,
        end_balance_cto=end_cto,
        cum_net_withdraw_av=net_av,
        cum_net_withdraw_cto=net_cto,
        taxes_paid_av=tax_av,
        taxes_paid_cto=tax_cto,
        fees_cto=fees_cto,
    )


# ---------------------- CLI ----------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Assurance-Vie (>8 years) vs CTO (PFU) simulation with monthly withdrawals")
    p.add_argument('-i', '--initial', type=float, default=100_000,
                   help='Starting capital (€), default 100,000')
    p.add_argument('-r', '--annual-return', type=parse_rate,
                   default='5%', help='Annual gross return rate (ex: 5%%)')
    p.add_argument('-y', '--years', type=int, default=10,
                   help='Time horizon in years, default 10')
    # Mutually exclusive group for withdrawal options
    withdraw_group = p.add_mutually_exclusive_group()
    withdraw_group.add_argument('-w', '--withdraw-rate', type=parse_rate,
                               default='2.5%', help='Annual NET withdrawal rate (ex: 2.5%%)')
    withdraw_group.add_argument('--withdraw-fixed', type=float,
                               help='Fixed monthly NET amount (€, ex: 1000)')
    
    p.add_argument('--withdraw-on', choices=['initial', 'balance'], default='initial',
                   help="Withdrawal base: 'initial' (default) or 'balance' (ignored if --withdraw-fixed)")

    # Fees
    p.add_argument('--av-fee', type=parse_rate, default='0.75%',
                   help="AV management fees / year (ex: 0.75%%)")
    p.add_argument('--cto-fee', type=parse_rate, default='0.008%',
                   help="CTO transaction commission per withdrawal (ex: 0.008%%)")
    p.add_argument('--cto-min-fee', type=float, default=3.0,
                   help="Minimum CTO commission per withdrawal (€, default €3)")

    # Taxation (modifiable if needed)
    p.add_argument('--ps-rate', type=parse_rate, default='17.2%',
                   help='Social contributions (default 17.2%%)')
    p.add_argument('--pfu-ir', type=parse_rate, default='12.8%',
                   help="IR portion of PFU (default 12.8%%, total PFU = IR + PS)")
    p.add_argument('--av-ir-low', type=parse_rate, default='7.5%',
                   help='AV IR <= premium threshold (default 7.5%%)')
    p.add_argument('--av-ir-high', type=parse_rate, default='12.8%',
                   help='AV IR > premium threshold (default 12.8%%)')
    p.add_argument('--av-threshold', type=float, default=150_000.0,
                   help='Premium threshold €150,000 (default)')
    p.add_argument('--abatement', type=float, default=4600.0,
                   help="Annual AV IR allowance (€4,600 single, €9,200 couple)")

    # Optional grid
    p.add_argument('--grid', type=parse_grid,
                   help='Grid analysis min:max:step of initial capitals')
    p.add_argument('--csv', type=str,
                   help='CSV output path (if grid or if you want to save the run)')
    p.add_argument('--plot', action='store_true',
                   help='Plot AV-CTO difference (requires matplotlib)')
    return p


def main():
    args = build_parser().parse_args()

    inp = Inputs(
        initial=args.initial,
        annual_return=args.annual_return,
        years=args.years,
        withdraw_rate_annual=args.withdraw_rate if args.withdraw_rate is not None else 0.025,
        withdraw_fixed_monthly=args.withdraw_fixed,
        withdraw_on_initial=(args.withdraw_on == 'initial'),
        av_fee_annual=args.av_fee,
        cto_fee_rate=args.cto_fee,
        cto_min_fee=args.cto_min_fee,
        ps_rate=args.ps_rate,
        pfu_ir_rate=args.pfu_ir,
        av_ir_low=args.av_ir_low,
        av_ir_high=args.av_ir_high,
        av_premium_threshold=args.av_threshold,
        av_abatement_ir=args.abatement,
    )
    if args.grid:
        if pd is None:
            raise SystemExit(
                "Pandas is required for --grid / --csv. Install it: pip install pandas")
        amin, amax, step = args.grid
        rows: List[dict] = []
        x = amin
        while x <= amax + 1e-9:
            inp_grid = Inputs(**{**inp.__dict__, 'initial': x})
            out = run_single(inp_grid)
            row_data = {**asdict(inp_grid), **asdict(out)}
            row_data['total_wealth_av'] = out.total_wealth_av
            row_data['total_wealth_cto'] = out.total_wealth_cto
            rows.append(row_data)
            x += step
        df = pd.DataFrame(rows)
        df['diff'] = df['total_wealth_av'] - df['total_wealth_cto']
        if args.csv:
            df.to_csv(args.csv, index=False)
            print(f"CSV written: {args.csv}")
        # Plot
        if args.plot:
            try:
                import matplotlib.pyplot as plt
                plt.figure()
                plt.plot(df['initial'], df['diff'])
                plt.axhline(0, linestyle='--')
                plt.xlabel('Initial capital (€)')
                plt.ylabel('AV - CTO: total net wealth')
                plt.title('AV - CTO difference vs initial capital')
                plt.show()
            except Exception as e:
                print(f"Plot failed: {e}")
        # Quick summary
        idx = df['diff'].abs().idxmin()
        print("\n≈ Closest point to equilibrium:")
        print(df.loc[idx, ['initial', 'diff']])
        return

    # Simple run
    out = run_single(inp)
    print("\n--- Parameters ---")
    print(f"Initial capital: {inp.initial:,.2f} €")
    print(
        f"Horizon: {inp.years} years | Return: {inp.annual_return*100:.3f} %/year")
    if inp.withdraw_fixed_monthly is not None:
        print(f"NET withdrawals: {inp.withdraw_fixed_monthly:,.2f} €/month fixed")
    else:
        print(
            f"NET withdrawals: {inp.withdraw_rate_annual*100:.3f} %/year on {'initial' if inp.withdraw_on_initial else 'balance'}")
    print(f"AV: fees {inp.av_fee_annual*100:.3f} %/year | IR {inp.av_ir_low*100:.1f}% / {inp.av_ir_high*100:.1f}% | premium threshold {inp.av_premium_threshold:,.0f} € | allowance {inp.av_abatement_ir:,.0f} €")
    print(f"CTO: commission {inp.cto_fee_rate*100:.5f} %/withdrawal (min {inp.cto_min_fee:.2f}€) | PFU = IR {inp.pfu_ir_rate*100:.1f}% + PS {inp.ps_rate*100:.1f}% = {(inp.pfu_ir_rate+inp.ps_rate)*100:.1f}%")

    print("\n--- Results over horizon ---")
    print(
        f"AV : final capital = {out.end_balance_av:,.2f} € | cumulative net withdrawals = {out.cum_net_withdraw_av:,.2f} € | taxes = {out.taxes_paid_av:,.2f} €")
    print(f"CTO: final capital = {out.end_balance_cto:,.2f} € | cumulative net withdrawals = {out.cum_net_withdraw_cto:,.2f} € | taxes = {out.taxes_paid_cto:,.2f} € | commissions = {out.fees_cto:,.2f} €")
    print(
        f"\nDifference (AV − CTO) in total net wealth = {out.diff_av_minus_cto:,.2f} €")

    if args.csv and pd is not None:
        df = pd.DataFrame([{**asdict(inp), **asdict(out)}])
        df['total_wealth_av'] = out.total_wealth_av
        df['total_wealth_cto'] = out.total_wealth_cto
        df['diff'] = out.diff_av_minus_cto
        df.to_csv(args.csv, index=False)
        print(f"\nCSV written: {args.csv}")


if __name__ == '__main__':
    main()
