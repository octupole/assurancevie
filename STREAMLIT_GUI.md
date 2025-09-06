# Streamlit Web Interface Guide

This document explains how to use and understand the Streamlit web interface for the AV vs CTO Simulator.

## Quick Start

### Installation
```bash
# Install required dependencies
pip install streamlit plotly pandas

# Run the web interface
streamlit run streamlit_app.py
```

The interface will open automatically in your browser at `http://localhost:8501`.

## Interface Overview

The Streamlit interface provides a user-friendly web-based GUI that makes all simulator functionality accessible through interactive forms and visualizations.

### Layout Structure

```
┌─────────────────────────────────────────────────────────────┐
│                    🇫🇷 AV vs CTO Simulator                    │
├─────────────────┬───────────────────────────────────────────┤
│   📊 SIDEBAR    │              MAIN CONTENT                 │
│                 │                                           │
│ • Basic Settings│  📈 Simulation Results                    │
│ • Withdrawal    │  • Key Metrics (3 columns)               │
│ • Advanced Params│  • Detailed Breakdown Table             │
│   (collapsible) │  • Interactive Charts                    │
│                 │                                           │
│                 ├───────────────────────────────────────────┤
│                 │  ℹ️ Parameter Summary                     │
│                 │  🎯 Quick Scenarios                       │
└─────────────────┴───────────────────────────────────────────┘
```

## Parameter Sections

### 1. Basic Settings (Always Visible)

**Initial Capital (€)**
- Range: €1,000 - €2,000,000
- Default: €100,000
- Step: €5,000
- Purpose: Starting investment amount

**Annual Return (%)**
- Range: 1.0% - 10.0%
- Default: 5.0%
- Step: 0.1%
- Purpose: Expected gross annual return

**Time Horizon (years)**
- Range: 5 - 40 years
- Default: 20 years
- Purpose: Investment period length

### 2. Withdrawal Strategy

**Withdrawal Type (Radio Selection)**
- **Percentage**: Withdraw X% annually
- **Fixed Amount**: Withdraw €X monthly

#### If "Percentage" Selected:
**Annual NET Withdrawal Rate (%)**
- Range: 0.5% - 8.0%
- Default: 2.5%
- Purpose: Percentage withdrawn annually (after taxes)

**Withdrawal Base**
- **initial**: Calculate percentage on initial capital (fixed euro amount)
- **balance**: Calculate percentage on current portfolio value

#### If "Fixed Amount" Selected:
**Fixed Monthly NET Amount (€)**
- Range: €100 - €20,000
- Default: €1,000
- Purpose: Fixed monthly income (after taxes)

### 3. Advanced Parameters (Collapsible)

#### Fee Parameters
**AV Management Fees (%/year)**
- Range: 0.1% - 3.0%
- Default: 0.75%
- Purpose: Annual management fees for Assurance-Vie

**CTO Transaction Fee (%)**
- Range: 0.001% - 0.5%
- Default: 0.008%
- Purpose: Commission per CTO withdrawal

**CTO Minimum Fee (€)**
- Range: €0 - €50
- Default: €3
- Purpose: Minimum commission per CTO transaction

#### Tax Parameters (French Tax Law 2024)
**Social Contributions (%)**
- Range: 15.0% - 20.0%
- Default: 17.2%
- Purpose: Prélèvements sociaux rate

**PFU Income Tax (%)**
- Range: 10.0% - 15.0%
- Default: 12.8%
- Purpose: Income tax portion of PFU for CTO

**AV IR ≤€150k (%)**
- Range: 5.0% - 10.0%
- Default: 7.5%
- Purpose: AV income tax rate for moderate premiums

**AV IR >€150k (%)**
- Range: 10.0% - 15.0%
- Default: 12.8%
- Purpose: AV income tax rate for large premiums

**Premium Threshold (€)**
- Range: €100,000 - €200,000
- Default: €150,000
- Purpose: Threshold for AV tax rate determination

**Annual IR Allowance (€)**
- Options: €4,600 (single) or €9,200 (couple)
- Default: €4,600
- Purpose: Annual tax allowance for AV withdrawals

## Results Display

### Key Metrics (3-Column Layout)

#### AV Column 🏛️
- **Total Wealth**: Final capital + cumulative withdrawals
- **Final Capital**: Remaining balance at end
- **Taxes Paid**: Total taxes over simulation period

#### CTO Column 🏦
- **Total Wealth**: Final capital + cumulative withdrawals
- **Final Capital**: Remaining balance at end
- **Taxes + Fees**: Total costs over simulation period

#### Comparison Column ⚖️
- **AV Advantage**: Difference in total wealth (€ and %)
  - Green = AV wins
  - Red = CTO wins
- **Winner**: Clear indication of better strategy

### Detailed Breakdown Table

Comprehensive comparison showing:
- Final Capital (both vehicles)
- Cumulative Net Withdrawals
- Total Taxes
- Transaction Fees
- Total Net Wealth
- Differences for each metric

### Interactive Visualization

**Stacked Bar Chart** showing:
- Final capital remaining
- Cumulative withdrawals received
- Total wealth composition for both AV and CTO

## Quick Scenarios Panel

Pre-configured parameter sets for common situations:

### Conservative Retiree
- **Capital**: €150,000
- **Return**: 4.0%
- **Horizon**: 25 years
- **Withdrawal**: 2.0%
- **Use Case**: Risk-averse retiree with moderate capital

### Early Retirement
- **Capital**: €400,000
- **Return**: 5.5%
- **Horizon**: 17 years
- **Withdrawal**: 3.5%
- **Use Case**: FIRE movement, early retirement strategy

### Wealth Preservation
- **Capital**: €500,000
- **Return**: 6.0%
- **Horizon**: 30 years
- **Withdrawal**: 1.5%
- **Use Case**: Focus on capital preservation with minimal withdrawals

## Technical Implementation

### Architecture
```python
streamlit_app.py
├── Parameter Collection (Sidebar)
│   ├── Basic Settings
│   ├── Withdrawal Strategy (Conditional UI)
│   └── Advanced Parameters (Collapsible)
├── Simulation Execution
│   ├── Input Validation
│   ├── Inputs Object Creation
│   └── Core Simulator Call
├── Results Display
│   ├── Key Metrics (st.metric)
│   ├── Comparison Table (pandas DataFrame)
│   └── Interactive Charts (plotly)
└── User Experience
    ├── Error Handling
    ├── Loading Indicators
    └── Help Text
```

### Key Streamlit Components Used

**Input Widgets**
- `st.number_input()`: Numeric inputs with validation
- `st.slider()`: Range inputs with visual feedback
- `st.radio()`: Exclusive choice selection
- `st.selectbox()`: Dropdown selection
- `st.expander()`: Collapsible sections

**Display Components**
- `st.metric()`: Key performance indicators with deltas
- `st.table()`: Structured data display
- `st.plotly_chart()`: Interactive visualizations
- `st.columns()`: Multi-column layouts

**User Feedback**
- `st.spinner()`: Loading indicators
- `st.success()`: Success messages
- `st.error()`: Error handling
- `st.info()`: Information displays

### Data Flow

1. **User Input**: Streamlit widgets collect parameters
2. **Validation**: Automatic validation through widget constraints
3. **Processing**: Create `Inputs` object and call `run_single()`
4. **Display**: Format and present results through multiple visualization methods
5. **Interactivity**: Real-time updates when parameters change

## Advantages over Command Line

### User Experience
- **Visual Interface**: No command-line knowledge required
- **Immediate Feedback**: See parameter effects instantly
- **Error Prevention**: Input validation prevents invalid combinations
- **Help Integration**: Contextual help for each parameter

### Accessibility
- **Mobile Friendly**: Responsive design works on tablets/phones
- **Cross-Platform**: Works on any device with a web browser
- **No Installation**: Users don't need to install Python locally
- **Easy Sharing**: Share results via URL or screenshots

### Visualization
- **Interactive Charts**: Hover, zoom, pan capabilities
- **Professional Presentation**: Clean, modern interface
- **Multiple Views**: Metrics, tables, and charts simultaneously
- **Comparison Focus**: Side-by-side AV vs CTO presentation

## Deployment Options

### Local Development
```bash
streamlit run streamlit_app.py
# Access at http://localhost:8501
```

### Network Access
```bash
streamlit run streamlit_app.py --server.address 0.0.0.0
# Access from any device on local network
```

### Cloud Deployment
- **Streamlit Cloud**: Free hosting connected to GitHub
- **Heroku**: Easy cloud deployment
- **Other platforms**: AWS, GCP, Azure compatible

## Customization

### Adding New Parameters
1. Add widget in appropriate sidebar section
2. Include in `Inputs` object creation
3. Update parameter summary display

### Modifying Visualizations
- Charts use Plotly - highly customizable
- Can add new chart types (line, scatter, etc.)
- Color schemes and themes adjustable

### Extending Functionality
- Add parameter presets system using `st.session_state`
- Implement parameter export/import
- Add Monte Carlo simulation toggle
- Include sensitivity analysis charts

## Performance Considerations

### Optimization
- Simulation runs only when button clicked (not reactive)
- Results cached automatically by Streamlit
- Minimal memory footprint

### Scalability
- Single-user focused (not multi-tenant)
- Can handle complex simulations quickly
- Resource usage scales with simulation complexity

## Troubleshooting

### Common Issues

**"Import could not be resolved" warnings**
- Install dependencies: `pip install streamlit plotly pandas`
- These are IDE warnings, not runtime errors

**Charts not displaying**
- Ensure plotly is installed: `pip install plotly`
- Check browser compatibility (modern browsers only)

**Simulation button not responding**
- Check console for error messages
- Verify av_vs_cto_simulator.py is in same directory
- Ensure all required parameters are valid

### Browser Compatibility
- **Recommended**: Chrome, Firefox, Safari (latest versions)
- **Supported**: Edge, Opera
- **Not supported**: Internet Explorer

## Future Enhancements

### Planned Features
- Session state for scenario button functionality
- Parameter export/import (JSON format)
- Historical comparison charts
- Sensitivity analysis visualizations
- Multi-scenario comparison tables
- PDF report generation

### Integration Possibilities
- Database storage for user scenarios
- API integration for real-time market data
- Advanced analytics dashboard
- Mobile app companion

This Streamlit interface provides a professional, accessible way to use the AV vs CTO simulator without requiring command-line expertise, making French retirement planning analysis available to a broader audience.