# Installation Guide

## System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: Minimal (< 100MB)
- **Storage**: < 50MB for all files

## Quick Installation

### Option 1: Clone from GitHub (Recommended)

```bash
git clone https://github.com/octupole/assurancevie.git
cd assurancevie
```

### Option 2: Download ZIP

1. Download ZIP from GitHub releases
2. Extract to desired directory
3. Navigate to extracted folder

## Dependencies

The simulator has **no required dependencies** beyond Python standard library. However, optional dependencies enable additional features:

### Core Functionality (No additional packages needed)

```bash
python av_vs_cto_simulator.py -i 100000 -w 2.5%
```

Works immediately with any Python 3.8+ installation.

### Enhanced Functionality

Install optional packages for full features:

```bash
pip install pandas matplotlib
```

**What this enables**:
- CSV export (`--csv` option)
- Grid analysis (`--grid` option)  
- Charts and plots (`--plot` option)

### Development Setup

For contributors or advanced users:

```bash
pip install -r requirements.txt
```

This installs all dependencies including development tools.

## Installation Verification

### Test Basic Functionality

```bash
python av_vs_cto_simulator.py --help
```

Should display help information without errors.

### Test Core Simulation

```bash
python av_vs_cto_simulator.py -i 100000 -w 2.5% --years 5
```

Should output comparison results.

### Test Enhanced Features

```bash
python av_vs_cto_simulator.py -i 100000 -w 2.5% --csv test.csv
```

Should create `test.csv` file (requires pandas).

### Test Plotting

```bash
python av_vs_cto_simulator.py -i 100000 -w 2.5% --grid 50000:200000:50000 --plot
```

Should display a chart (requires pandas + matplotlib).

## Platform-Specific Instructions

### Windows

#### Using Python from Microsoft Store
```cmd
python av_vs_cto_simulator.py -i 100000 -w 2.5%
```

#### Using Anaconda
```cmd
conda install pandas matplotlib
python av_vs_cto_simulator.py -i 100000 -w 2.5% --csv results.csv
```

#### Using Command Prompt
```cmd
# If 'python' doesn't work, try 'py'
py av_vs_cto_simulator.py --help
```

### macOS

#### Using Homebrew Python
```bash
brew install python
pip3 install pandas matplotlib
python3 av_vs_cto_simulator.py -i 100000 -w 2.5%
```

#### Using System Python
```bash
python3 av_vs_cto_simulator.py -i 100000 -w 2.5%
```

### Linux (Ubuntu/Debian)

#### Install Python and pip
```bash
sudo apt update
sudo apt install python3 python3-pip
pip3 install pandas matplotlib
```

#### Run simulator
```bash
python3 av_vs_cto_simulator.py -i 100000 -w 2.5%
```

### Linux (CentOS/RHEL/Fedora)

#### Install Python and pip
```bash
# CentOS/RHEL
sudo yum install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip

pip3 install pandas matplotlib
```

## Docker Installation (Optional)

For isolated environment or consistent deployment:

### Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY av_vs_cto_simulator.py .
COPY docs/ ./docs/

ENTRYPOINT ["python", "av_vs_cto_simulator.py"]
```

### Build and run

```bash
docker build -t av-cto-simulator .
docker run av-cto-simulator -i 100000 -w 2.5%
```

## Virtual Environment Setup (Recommended)

Isolate dependencies from system Python:

### Create virtual environment

```bash
python3 -m venv av-cto-env
```

### Activate environment

**Linux/macOS**:
```bash
source av-cto-env/bin/activate
```

**Windows**:
```cmd
av-cto-env\Scripts\activate
```

### Install dependencies

```bash
pip install pandas matplotlib
```

### Run simulator

```bash
python av_vs_cto_simulator.py -i 100000 -w 2.5%
```

### Deactivate when done

```bash
deactivate
```

## Troubleshooting

### Common Issues

#### "python: command not found"

**Solution**: Try `python3` or `py` instead of `python`

#### "No module named 'pandas'"

**Solution**: 
```bash
pip install pandas
# or
pip3 install pandas
```

#### "Permission denied"

**Solution**: Use `--user` flag or virtual environment:
```bash
pip install --user pandas matplotlib
```

#### Charts don't display

**Possible causes**:
1. matplotlib not installed: `pip install matplotlib`
2. No GUI available (SSH session): Save to file instead
3. Backend issues: Try different matplotlib backend

#### CSV files not created

**Cause**: pandas not installed
**Solution**: `pip install pandas`

### Getting Help

1. **Check Python version**: `python --version` (need 3.8+)
2. **Check pip version**: `pip --version`
3. **List installed packages**: `pip list`
4. **Test imports**: 
   ```python
   python -c "import pandas; import matplotlib; print('OK')"
   ```

### Performance Issues

The simulator is lightweight and should run quickly. If experiencing slowness:

1. **Large grid analysis**: Reduce grid size or step
2. **Memory issues**: Close other applications
3. **Old Python**: Upgrade to Python 3.9+

## Updating

### From GitHub

```bash
cd assurancevie
git pull origin main
```

### From ZIP download

1. Download latest release
2. Replace old files with new ones
3. Keep any CSV files you want to preserve

## Uninstallation

### Remove files

```bash
rm -rf av-cto-simulator/  # Linux/macOS
# or manually delete folder on Windows
```

### Remove Python packages (optional)

```bash
pip uninstall pandas matplotlib
```

### Remove virtual environment

```bash
rm -rf av-cto-env/  # Linux/macOS
# or delete folder on Windows
```

## Next Steps

After successful installation:

1. **Read the documentation**: Check `docs/USAGE.md`
2. **Try examples**: Follow `docs/EXAMPLES.md`
3. **Understand taxes**: Review `docs/TAX_CALCULATIONS.md`
4. **Run your analysis**: Use your own parameters

## Support

If you encounter installation issues:

1. Check this guide first
2. Search existing GitHub issues
3. Create new issue with:
   - Operating system and version
   - Python version (`python --version`)
   - Full error message
   - What you tried to do