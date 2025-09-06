# Changelog

All notable changes to the AV vs CTO Simulator will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Features
- PEA (Plan d'Épargne en Actions) support
- PER (Plan d'Épargne Retraite) comparison
- Inheritance tax calculations
- Monte Carlo simulation support
- Web interface option

## [1.0.0] - 2024-01-XX

### Added
- Initial release of AV vs CTO comparison simulator
- Net withdrawal calculation system
- French tax compliance (AV >8 years, CTO PFU)
- Two withdrawal strategies: percentage-based and fixed amount
- Grid analysis for break-even point identification
- CSV export functionality
- Matplotlib visualization support
- Comprehensive command-line interface
- Minimum transaction fee support for CTO accounts
- Premium threshold handling (€150k) for AV taxation
- Annual allowance calculation (€4,600/€9,200)
- Complete English documentation while maintaining French terminology

### Features
- **Core Simulation**:
  - Monthly compounding with annual tax calculation
  - Proportional gains method for both AV and CTO
  - Accurate implementation of French tax rules
  - Support for different withdrawal bases (initial vs current balance)

- **Tax Calculations**:
  - AV: 7.5%/12.8% IR + 17.2% PS with allowances and thresholds
  - CTO: 30% PFU flat tax (12.8% + 17.2%)
  - Transaction fee deduction for CTO taxable gains

- **Analysis Tools**:
  - Single scenario comparison
  - Grid analysis across capital ranges
  - CSV export with full simulation data
  - Optional matplotlib charts

- **Command Line Interface**:
  - Comprehensive parameter control
  - Input validation and error handling
  - Help system with examples
  - Flexible output options

### Documentation
- Complete README with quick start guide
- Detailed usage documentation (USAGE.md)
- Comprehensive examples (EXAMPLES.md)  
- Tax calculation documentation (TAX_CALCULATIONS.md)
- Installation guide (INSTALL.md)
- Requirements specification

### Technical
- Python 3.8+ compatibility
- No required dependencies (pandas/matplotlib optional)
- Type hints throughout codebase
- Comprehensive parameter validation
- Binary search for net withdrawal solving

## Development Notes

### Architecture Decisions
- **Net-first approach**: All withdrawals specified as net amounts
- **Monthly simulation**: Realistic timing of fees and performance
- **Annual taxation**: Matches real-world tax calculation timing
- **Proportional gains**: Consistent with French tax law implementation
- **Binary search solver**: Ensures exact net withdrawal amounts

### Code Quality
- Full type annotations
- Comprehensive docstrings
- Clear separation of concerns
- Extensive input validation
- Error handling and user feedback

### Future Compatibility
- Designed for easy extension to additional investment vehicles
- Parameterized tax rates for easy law change adaptation
- Modular structure for feature additions
- Clear interfaces between simulation components