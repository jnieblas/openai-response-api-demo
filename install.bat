@echo off
REM OpenAI Responses API Python Interface - Windows Installation Script

echo 🚀 Installing OpenAI Responses API Python Interface
echo ==================================================

REM Check if Python 3.13 is available
python --version 2>nul
if errorlevel 1 (
    echo ❌ Python not found
    echo    Please install Python 3.13 first from https://python.org
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python version: %PYTHON_VERSION%

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo 📦 Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install dependencies
echo 📥 Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

REM Set up environment variables
echo 🔧 Setting up environment...
if not exist .env (
    echo # OpenAI API Configuration > .env
    echo # Get your API key from: https://platform.openai.com/api-keys >> .env
    echo OPENAI_API_KEY=your-api-key-here >> .env
    echo. >> .env
    echo # Optional: Custom base URL (for Azure OpenAI or other providers) >> .env
    echo # OPENAI_BASE_URL=https://your-custom-endpoint.com/v1 >> .env
    echo ✅ Created .env file template
    echo    Please edit .env and add your OpenAI API key
) else (
    echo ✅ .env file already exists
)

REM Test installation
echo 🧪 Testing installation...
python test_import.py
if errorlevel 1 (
    echo ❌ Installation test failed
    pause
    exit /b 1
)

echo.
echo 🎉 Installation complete!
echo.
echo Next steps:
echo 1. Edit .env file and add your OpenAI API key
echo 2. Activate the virtual environment: venv\Scripts\activate.bat
echo 3. Run the demo: python main.py
echo 4. Check README.md for more information
echo.
echo Happy coding! 🚀
pause 