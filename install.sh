#!/bin/bash

# OpenAI Responses API Demo - Installation Script
# This script sets up the Python environment and installs dependencies

set -e  # Exit on any error

echo "🚀 OpenAI Responses API Demo - Installation Script"
echo "=================================================="

# Check if Python 3.13 is available
if ! command -v python3.13 &> /dev/null; then
    echo "❌ Python 3.13 is not installed or not in PATH"
    echo "   Please install Python 3.13 using pyenv or your preferred method"
    echo "   Example: pyenv install 3.13.0"
    exit 1
fi

echo "✅ Python 3.13 found: $(python3.13 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3.13 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Dependencies installed successfully"

# Test the installation
echo "🧪 Testing installation..."
python test_import.py

echo ""
echo "🎉 Installation completed successfully!"
echo "=================================================="
echo ""
echo "📋 Next steps:"
echo "1. Set your OpenAI API key:"
echo "   export OPENAI_API_KEY='your-api-key-here'"
echo ""
echo "2. Run the command line demo:"
echo "   python main.py"
echo ""
echo "3. Run comprehensive tool calling examples:"
echo "   python tool_calling_example.py"
echo ""
echo "4. Launch the web interface:"
echo "   python run_app.py"
echo ""
echo "🔧 Key Features Available:"
echo "✅ Structured response generation (emails, letters, messages)"
echo "✅ Function tools with JSON schema parameters"
echo "✅ Hosted tools with tool IDs"
echo "✅ Interactive web interface with Streamlit"
echo "✅ Tool choice options (auto, none, specific)"
echo "✅ Comprehensive error handling and validation"
echo ""
echo "📖 For more information, see README.md" 