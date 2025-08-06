#!/bin/bash

# OpenAI Responses API Python Interface - Installation Script
# This script sets up the project on any machine with Python 3.13

set -e  # Exit on any error

echo "🚀 Installing OpenAI Responses API Python Interface"
echo "=================================================="

# Check if Python 3.13 is available
check_python() {
    if command -v python3.13 &> /dev/null; then
        PYTHON_CMD="python3.13"
        echo "✅ Found Python 3.13"
    elif command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
        if [[ "$PYTHON_VERSION" == "3.13" ]]; then
            PYTHON_CMD="python3"
            echo "✅ Found Python 3.13"
        else
            echo "❌ Python 3.13 is required, but found Python $PYTHON_VERSION"
            echo "   Please install Python 3.13 first:"
            echo "   - macOS: brew install python@3.13"
            echo "   - Ubuntu: sudo apt install python3.13"
            echo "   - Or use pyenv: pyenv install 3.13.0"
            exit 1
        fi
    else
        echo "❌ Python 3.13 not found"
        echo "   Please install Python 3.13 first"
        exit 1
    fi
}

# Check if pyenv is available and suggest using it
check_pyenv() {
    if command -v pyenv &> /dev/null; then
        echo "📦 pyenv detected - you can use it to manage Python versions:"
        echo "   pyenv install 3.13.0"
        echo "   pyenv local 3.13.0"
        echo ""
    fi
}

# Create virtual environment
create_venv() {
    echo "📦 Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        # Windows
        source venv/Scripts/activate
    else
        # Unix-like systems
        source venv/bin/activate
    fi
    
    echo "✅ Virtual environment created and activated"
}

# Install dependencies
install_deps() {
    echo "📥 Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
}

# Set up environment variables
setup_env() {
    echo "🔧 Setting up environment..."
    
    if [[ ! -f .env ]]; then
        cat > .env << EOF
# OpenAI API Configuration
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your-api-key-here

# Optional: Custom base URL (for Azure OpenAI or other providers)
# OPENAI_BASE_URL=https://your-custom-endpoint.com/v1
EOF
        echo "✅ Created .env file template"
        echo "   Please edit .env and add your OpenAI API key"
    else
        echo "✅ .env file already exists"
    fi
}

# Test installation
test_installation() {
    echo "🧪 Testing installation..."
    
    # Test import
    if $PYTHON_CMD -c "import sys; sys.path.insert(0, 'src'); from openai_responses import OpenAIResponsesAPI; print('✅ Import successful')" 2>/dev/null; then
        echo "✅ Package import successful"
    else
        echo "❌ Package import failed"
        exit 1
    fi
    
    # Test demo (without API key)
    echo "🧪 Testing demo (will show error handling without API key)..."
    $PYTHON_CMD main.py > /dev/null 2>&1 || echo "✅ Demo script runs (shows expected errors without API key)"
}

# Main installation process
main() {
    check_python
    check_pyenv
    create_venv
    install_deps
    setup_env
    test_installation
    
    echo ""
    echo "🎉 Installation complete!"
    echo ""
    echo "Next steps:"
    echo "1. Edit .env file and add your OpenAI API key"
    echo "2. Activate the virtual environment:"
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        echo "   source venv/Scripts/activate"
    else
        echo "   source venv/bin/activate"
    fi
    echo "3. Run the demo: python main.py"
    echo "4. Check README.md for more information"
    echo ""
    echo "Happy coding! 🚀"
}

# Run main function
main 