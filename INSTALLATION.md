# Installation Guide

This guide will help you install and set up the OpenAI Responses API Python Interface on any machine.

## Prerequisites

- Python 3.13 or higher
- OpenAI API key (get one from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys))

## Quick Installation

### Option 1: Automated Installation Script

#### macOS/Linux:
```bash
chmod +x install.sh
./install.sh
```

#### Windows:
```cmd
install.bat
```

### Option 2: Manual Installation

#### Step 1: Install Python 3.13

**macOS:**
```bash
# Using Homebrew
brew install python@3.13

# Using pyenv (recommended)
pyenv install 3.13.0
pyenv local 3.13.0
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.13 python3.13-venv
```

**Windows:**
Download from [https://python.org](https://python.org) and install Python 3.13

#### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3.13 -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

#### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 4: Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# OpenAI API Configuration
OPENAI_API_KEY=your-api-key-here

# Optional: Custom base URL (for Azure OpenAI or other providers)
# OPENAI_BASE_URL=https://your-custom-endpoint.com/v1
```

#### Step 5: Test Installation

```bash
python test_import.py
python main.py
```

## Verification

After installation, you should see:

1. ✅ All imports successful in `test_import.py`
2. ✅ Demo runs successfully in `main.py` (with API key)
3. ✅ Generated responses displayed correctly

## Troubleshooting

### Common Issues

**Python version not found:**
```bash
# Check Python version
python --version

# If not 3.13+, install it first
```

**Import errors:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**API key errors:**
- Make sure your `.env` file contains a valid OpenAI API key
- Check that the API key has access to the Responses API
- Verify the key is not expired

**Permission errors (macOS/Linux):**
```bash
chmod +x install.sh
```

## Next Steps

1. **Run the demo:** `python main.py`
2. **Check the README:** For usage examples and API documentation
3. **Explore the code:** Look at `src/openai_responses/` for the implementation
4. **Build your own:** Use the API interface in your projects

## Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Verify your Python version is 3.13+
3. Ensure your OpenAI API key is valid
4. Check the project's README.md for more information

## Development Setup

For development work:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/

# Lint code
flake8 src/
``` 