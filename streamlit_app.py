#!/usr/bin/env python3
"""
Streamlit Web Interface for AV vs CTO Retirement Simulator

This file provides a user-friendly web interface for the French retirement planning
simulator that compares Assurance-Vie (AV) vs Compte-Titre Ordinaire (CTO) investment
strategies.

Features:
- Interactive form with all simulation parameters
- Real-time calculation and visualization
- Professional metrics display with comparisons
- Responsive design that works on desktop and mobile
- Advanced parameters in collapsible sections
- Preset scenario buttons for quick analysis

Requirements:
    pip install streamlit plotly pandas

Usage:
    streamlit run streamlit_app.py
    
    Then open your browser to http://localhost:8501

The interface provides:
1. Sidebar with all input parameters organized in sections
2. Main area with simulation results and visualizations
3. Parameter summary panel with quick scenario buttons
4. Professional charts showing wealth breakdown

All calculations use the same core logic as the command-line simulator,
ensuring consistency between interfaces.
"""

# Core web framework for building the GUI
import streamlit as st
# Data manipulation for results table
import pandas as pd
# Plotting libraries for interactive charts (px currently unused but available)
import plotly.express as px
import plotly.graph_objects as go
# Import the core simulation logic and data structures
from av_vs_cto_simulator import Inputs, run_single
import sys
import os

# Ensure we can import the simulator from the same directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure the Streamlit page settings
# Wide layout provides more space for the two-column design
st.set_page_config(
    page_title="AV vs CTO Simulator", 
    page_icon="💰", 
    layout="wide"
)

st.title("🇫🇷 AV vs CTO Retirement Simulator")
st.markdown("Compare **Assurance-Vie** and **CTO** investment strategies for French retirement planning")

# =============================================================================
# SIDEBAR: INPUT PARAMETERS
# =============================================================================
# The sidebar contains all input parameters organized in logical sections:
# 1. Basic Settings (capital, return, time horizon)
# 2. Withdrawal Strategy (percentage vs fixed amount)
# 3. Advanced Parameters (fees and tax rates) - collapsible

st.sidebar.header("📊 Simulation Parameters")

# BASIC SETTINGS SECTION
# These are the core parameters most users will adjust
st.sidebar.subheader("Basic Settings")
# Initial capital input with reasonable bounds and step size
# Default of €100,000 is a common starting point for retirement planning
initial = st.sidebar.number_input(
    "Initial Capital (€)", 
    min_value=1000, 
    max_value=2000000, 
    value=100000, 
    step=5000,
    help="Starting investment amount"
)

# Annual return slider - converts percentage to decimal for calculations
# Range 1-10% covers realistic market expectations
annual_return = st.sidebar.slider(
    "Annual Return (%)", 
    min_value=1.0, 
    max_value=10.0, 
    value=5.0, 
    step=0.1,
    help="Expected annual gross return"
) / 100  # Convert percentage to decimal

# Investment time horizon - 5-40 years covers most retirement scenarios
# Default of 20 years is typical for mid-career retirement planning
years = st.sidebar.slider(
    "Time Horizon (years)", 
    min_value=5, 
    max_value=40, 
    value=20, 
    step=1,
    help="Investment period"
)

# WITHDRAWAL STRATEGY SECTION
# Users can choose between:
# 1. Percentage-based: withdraw X% annually (on initial capital or current balance)
# 2. Fixed amount: withdraw €X per month
# The interface dynamically shows/hides relevant options based on selection
st.sidebar.subheader("💸 Withdrawal Strategy")
# Radio button to select withdrawal strategy
# This controls which additional inputs are shown below
withdrawal_type = st.sidebar.radio(
    "Withdrawal Type",
    ["Percentage", "Fixed Amount"],
    help="Choose between percentage-based or fixed monthly withdrawals"
)

# PERCENTAGE-BASED WITHDRAWAL OPTIONS
# Only shown when user selects "Percentage" option
if withdrawal_type == "Percentage":
    # Annual withdrawal rate as percentage (NET of taxes)
    # Range 0.5-8% covers conservative to aggressive withdrawal strategies
    withdraw_rate = st.sidebar.slider(
        "Annual NET Withdrawal Rate (%)", 
        min_value=0.5, 
        max_value=8.0, 
        value=2.5, 
        step=0.1,
        help="Percentage of capital withdrawn annually (net of taxes)"
    ) / 100  # Convert to decimal
    withdraw_fixed = None  # Not used in percentage mode
    
    # Whether to calculate percentage on initial capital or current balance
    # "initial" = fixed euro amount each year
    # "balance" = percentage of current portfolio value
    withdraw_on = st.sidebar.selectbox(
        "Withdrawal Base",
        ["initial", "balance"],
        help="Calculate percentage on initial capital or current balance"
    )
# FIXED AMOUNT WITHDRAWAL OPTIONS
# Only shown when user selects "Fixed Amount" option
else:
    # Fixed monthly withdrawal amount (NET of taxes)
    # €100-€20,000 range covers most retirement income needs
    withdraw_fixed = st.sidebar.number_input(
        "Fixed Monthly NET Amount (€)", 
        min_value=100, 
        max_value=20000, 
        value=1000, 
        step=50,
        help="Fixed monthly amount (net of taxes)"
    )
    # These parameters are not used in fixed amount mode but needed for the Inputs object
    withdraw_rate = 0.025  # Default value, will be ignored
    withdraw_on = "initial"  # Default value, will be ignored

# ADVANCED PARAMETERS SECTION (COLLAPSIBLE)
# These parameters have reasonable defaults but can be adjusted for specific scenarios
# Organized in an expander to avoid cluttering the main interface
# Contains: Fee parameters and Tax parameters
with st.sidebar.expander("🔧 Advanced Parameters"):
    # FEE PARAMETERS SUBSECTION
    st.subheader("Fees")
    # AV management fees - typically 0.5-1.5% annually in France
    # Applied to the entire AV balance each year
    av_fee = st.slider(
        "AV Management Fees (%/year)", 
        min_value=0.1, 
        max_value=3.0, 
        value=0.75, 
        step=0.05,
        help="Annual management fees for Assurance-Vie"
    ) / 100  # Convert to decimal
    
    # CTO transaction fees - charged on each withdrawal
    # Typically 0.1-1% per transaction at French brokers
    cto_fee = st.slider(
        "CTO Transaction Fee (%)", 
        min_value=0.001, 
        max_value=0.5, 
        value=0.008, 
        step=0.001,
        help="Commission per CTO withdrawal"
    ) / 100  # Convert to decimal
    
    # CTO minimum transaction fee - most brokers have a minimum fee per transaction
    # Even small withdrawals incur this minimum cost
    cto_min_fee = st.number_input(
        "CTO Minimum Fee (€)", 
        min_value=0.0, 
        max_value=50.0, 
        value=3.0, 
        step=0.5,
        help="Minimum commission per CTO transaction"
    )
    
    # TAX PARAMETERS SUBSECTION
    # These implement current French tax law (as of 2024)
    # Users can adjust for potential law changes or personal situations
    st.subheader("Tax Parameters")
    # Prélèvements sociaux (social contributions) - applies to both AV and CTO
    # Current rate is 17.2% on investment gains
    ps_rate = st.slider(
        "Social Contributions (%)", 
        min_value=15.0, 
        max_value=20.0, 
        value=17.2, 
        step=0.1,
        help="Prélèvements sociaux rate"
    ) / 100  # Convert to decimal
    
    # PFU (Prélèvement Forfaitaire Unique) income tax rate for CTO
    # Current rate is 12.8% (part of the 30% flat tax with 17.2% social contributions)
    pfu_ir = st.slider(
        "PFU Income Tax (%)", 
        min_value=10.0, 
        max_value=15.0, 
        value=12.8, 
        step=0.1,
        help="Income tax portion of PFU"
    ) / 100  # Convert to decimal
    
    # AV income tax rate for premiums up to €150,000
    # Lower rate applies to moderate premium amounts
    av_ir_low = st.slider(
        "AV IR ≤€150k (%)", 
        min_value=5.0, 
        max_value=10.0, 
        value=7.5, 
        step=0.1,
        help="AV income tax rate for premiums ≤€150k"
    ) / 100  # Convert to decimal
    
    # AV income tax rate for premiums above €150,000
    # Higher rate (same as PFU) applies to large premium amounts
    av_ir_high = st.slider(
        "AV IR >€150k (%)", 
        min_value=10.0, 
        max_value=15.0, 
        value=12.8, 
        step=0.1,
        help="AV income tax rate for premiums >€150k"
    ) / 100  # Convert to decimal
    
    # Premium threshold that determines which AV tax rate applies
    # Currently €150,000 in French law
    av_threshold = st.number_input(
        "Premium Threshold (€)", 
        min_value=100000, 
        max_value=200000, 
        value=150000, 
        step=10000,
        help="Premium threshold for AV tax rates"
    )
    
    # Annual tax allowance for AV withdrawals
    # €4,600 for single filers, €9,200 for married couples filing jointly
    abatement = st.selectbox(
        "Annual IR Allowance (€)",
        [4600, 9200],
        index=0,
        help="€4,600 (single) or €9,200 (couple)"
    )

# =============================================================================
# MAIN CONTENT AREA
# =============================================================================
# Two-column layout:
# - Left column (2/3 width): Simulation results and visualizations
# - Right column (1/3 width): Parameter summary and quick scenarios
col1, col2 = st.columns([2, 1])

# LEFT COLUMN: SIMULATION RESULTS
with col1:
    st.header("📈 Simulation Results")
    
    # Primary action button - triggers the simulation
    # Uses "primary" type for visual emphasis
    if st.button("🚀 Run Simulation", type="primary"):
        # Create the inputs object using values from the UI controls
        # This matches the dataclass structure expected by the core simulator
        inp = Inputs(
            initial=initial,
            annual_return=annual_return,
            years=years,
            withdraw_rate_annual=withdraw_rate,
            withdraw_fixed_monthly=withdraw_fixed,
            withdraw_on_initial=(withdraw_on == 'initial'),
            av_fee_annual=av_fee,
            cto_fee_rate=cto_fee,
            cto_min_fee=cto_min_fee,
            ps_rate=ps_rate,
            pfu_ir_rate=pfu_ir,
            av_ir_low=av_ir_low,
            av_ir_high=av_ir_high,
            av_premium_threshold=av_threshold,
            av_abatement_ir=abatement,
        )
        
        # Execute the simulation with error handling
        # The spinner provides user feedback during calculation
        try:
            with st.spinner('Running simulation...'):
                # Call the core simulation function from av_vs_cto_simulator.py
                out = run_single(inp)
            
            # SUCCESS: Display results in organized sections
            st.success("Simulation completed!")
            
            # KEY METRICS SECTION
            # Three columns for side-by-side comparison: AV, CTO, Difference
            col_av, col_cto, col_diff = st.columns(3)
            
            # AV METRICS COLUMN
            with col_av:
                # Total wealth = final capital + all withdrawals received
                st.metric(
                    "🏛️ AV Total Wealth",
                    f"€{out.total_wealth_av:,.0f}",
                    help="Final capital + cumulative withdrawals"
                )
                # Capital remaining at end of simulation
                st.metric(
                    "Final Capital",
                    f"€{out.end_balance_av:,.0f}"
                )
                # Total taxes paid over the simulation period
                st.metric(
                    "Taxes Paid",
                    f"€{out.taxes_paid_av:,.0f}"
                )
            
            # CTO METRICS COLUMN
            with col_cto:
                # Total wealth = final capital + all withdrawals received
                st.metric(
                    "🏦 CTO Total Wealth",
                    f"€{out.total_wealth_cto:,.0f}",
                    help="Final capital + cumulative withdrawals"
                )
                # Capital remaining at end of simulation
                st.metric(
                    "Final Capital",
                    f"€{out.end_balance_cto:,.0f}"
                )
                # Total costs: taxes + transaction fees
                st.metric(
                    "Taxes + Fees",
                    f"€{out.taxes_paid_cto + out.fees_cto:,.0f}"
                )
            
            # COMPARISON COLUMN
            with col_diff:
                diff = out.diff_av_minus_cto
                # Show absolute and percentage difference
                # Green for positive (AV advantage), red for negative (CTO advantage)
                st.metric(
                    "⚖️ AV Advantage",
                    f"€{diff:,.0f}",
                    delta=f"{(diff/out.total_wealth_cto)*100:+.1f}%",
                    delta_color="normal" if diff >= 0 else "inverse",
                    help="Difference in total wealth (AV - CTO)"
                )
                
                # Clear winner indicator
                winner = "AV" if diff >= 0 else "CTO"
                st.metric(
                    "Winner",
                    winner,
                    help="Investment vehicle with higher total wealth"
                )
            
            # DETAILED BREAKDOWN TABLE
            # Comprehensive comparison table showing all key metrics
            st.subheader("📊 Detailed Breakdown")
            
            # Create a structured comparison table
            results_df = pd.DataFrame({
                'Metric': [
                    'Final Capital',
                    'Cumulative Net Withdrawals', 
                    'Total Taxes',
                    'Transaction Fees',
                    'Total Net Wealth'
                ],
                'AV (€)': [
                    f"{out.end_balance_av:,.0f}",
                    f"{out.cum_net_withdraw_av:,.0f}",
                    f"{out.taxes_paid_av:,.0f}",
                    "0",
                    f"{out.total_wealth_av:,.0f}"
                ],
                'CTO (€)': [
                    f"{out.end_balance_cto:,.0f}",
                    f"{out.cum_net_withdraw_cto:,.0f}",
                    f"{out.taxes_paid_cto:,.0f}",
                    f"{out.fees_cto:,.0f}",
                    f"{out.total_wealth_cto:,.0f}"
                ],
                'Difference (€)': [
                    f"{out.end_balance_av - out.end_balance_cto:+,.0f}",
                    f"{out.cum_net_withdraw_av - out.cum_net_withdraw_cto:+,.0f}",
                    f"{out.taxes_paid_av - out.taxes_paid_cto:+,.0f}",
                    f"{-out.fees_cto:+,.0f}",
                    f"{diff:+,.0f}"
                ]
            })
            
            # Display the comparison table
            st.table(results_df)
            
            # INTERACTIVE VISUALIZATION
            # Stacked bar chart showing wealth composition for both vehicles
            st.subheader("📈 Wealth Comparison")
            
            # Prepare data for the chart (currently stored but could be used for additional charts)
            comparison_data = {
                'Vehicle': ['AV', 'CTO'],
                'Final Capital': [out.end_balance_av, out.end_balance_cto],
                'Cumulative Withdrawals': [out.cum_net_withdraw_av, out.cum_net_withdraw_cto],
                'Total Wealth': [out.total_wealth_av, out.total_wealth_cto]
            }
            
            # Create stacked bar chart using Plotly
            # Shows total wealth broken down into final capital and cumulative withdrawals
            fig = go.Figure(data=[
                go.Bar(name='Final Capital', x=['AV', 'CTO'], 
                       y=[out.end_balance_av, out.end_balance_cto]),
                go.Bar(name='Cumulative Withdrawals', x=['AV', 'CTO'], 
                       y=[out.cum_net_withdraw_av, out.cum_net_withdraw_cto])
            ])
            
            # Configure chart appearance and behavior
            fig.update_layout(
                barmode='stack',  # Stack bars to show total wealth composition
                title="Total Wealth Breakdown",
                xaxis_title="Investment Vehicle",
                yaxis_title="Amount (€)",
                yaxis_tickformat=",",  # Format numbers with commas
                height=400
            )
            
            # Display chart with responsive width
            st.plotly_chart(fig, use_container_width=True)
            
        # ERROR HANDLING
        # Catch any simulation errors and provide user-friendly feedback
        except Exception as e:
            st.error(f"Simulation failed: {str(e)}")
            st.info("Please check your input parameters and try again.")

# RIGHT COLUMN: PARAMETER SUMMARY AND QUICK SCENARIOS
with col2:
    st.header("ℹ️ Parameter Summary")
    
    # Display current parameter values for quick reference
    # This helps users verify their inputs before running simulation
    st.info(f"""
    **Investment**: €{initial:,}  
    **Return**: {annual_return*100:.1f}% per year  
    **Horizon**: {years} years  
    **Withdrawals**: {
        f"{withdraw_rate*100:.1f}%/year on {withdraw_on}" if withdrawal_type == "Percentage" 
        else f"€{withdraw_fixed:,}/month fixed"
    }
    """)
    
    # QUICK SCENARIOS SECTION
    # Preset parameter combinations for common retirement scenarios
    # Users can click buttons to quickly load realistic parameter sets
    st.subheader("🎯 Quick Scenarios")
    
    # Define common retirement planning scenarios
    # Each scenario has reasonable defaults for different situations
    scenarios = {
        "Conservative Retiree": {
            "initial": 150000,
            "return": 4.0,
            "years": 25,
            "withdraw": 2.0
        },
        "Early Retirement": {
            "initial": 400000,
            "return": 5.5,
            "years": 17,
            "withdraw": 3.5
        },
        "Wealth Preservation": {
            "initial": 500000,
            "return": 6.0,
            "years": 30,
            "withdraw": 1.5
        }
    }
    
    # Display scenario buttons
    # Note: Current implementation shows buttons but doesn't update parameters
    # A full implementation would use st.session_state to update sidebar values
    for scenario_name, params in scenarios.items():
        if st.button(f"📋 {scenario_name}", key=scenario_name):
            st.rerun()  # TODO: Implement session state parameter updates

# =============================================================================
# FOOTER
# =============================================================================
# Important disclaimers and links
st.markdown("---")
st.markdown(
    """
    **⚠️ Disclaimer**: This tool is for educational purposes only. 
    Consult qualified financial and tax professionals before making investment decisions.
    
    **📚 Documentation**: [GitHub Repository](https://github.com/octupole/assurancevie)
    """
)