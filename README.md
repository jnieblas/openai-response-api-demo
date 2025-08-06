# OpenAI Responses API Python Interface

A Python interface for the OpenAI Responses API, providing a clean and type-safe way to interact with OpenAI's structured response generation service.

## Features

- 🚀 Clean, type-safe Python interface for OpenAI Responses API
- 📦 Easy installation and dependency management
- 🔧 Configurable response formats and parameters
- 🛡️ Error handling and validation
- 📝 Comprehensive examples and documentation
- 🌐 **NEW: Interactive web interface with Streamlit**

## Requirements

- Python 3.13 or higher
- OpenAI API key

## Installation

### Using pip

```bash
pip install -r requirements.txt
```

### Using pyenv (recommended)

```bash
# Install Python 3.13
pyenv install 3.13.0
pyenv local 3.13.0

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Option 1: Web Interface (Recommended)

1. Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

2. Launch the web interface:
```bash
python run_app.py
```

3. Open your browser and go to `http://localhost:8501`

### Option 2: Command Line Demo

1. Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

2. Run the example:
```bash
python main.py
```

## Web Interface Features

The Streamlit web interface provides:

- 🎯 **Quick Templates** - Pre-configured templates for common use cases
- ⚙️ **Interactive Configuration** - Adjust model, temperature, and other parameters
- 📝 **Custom Prompts** - Enter your own prompts with real-time formatting
- 📊 **Response Analytics** - View token usage and response metadata
- 🔑 **Secure API Key Input** - Enter your API key securely in the interface

### Quick Templates Available:

- 📧 Professional Email
- 📝 Formal Letter  
- 💬 Casual Message
- 🙏 Thank You Note
- 📋 Meeting Confirmation
- 🎉 Creative Story

## Usage

### Web Interface

1. Launch the app: `python run_app.py`
2. Enter your API key (or set it as environment variable)
3. Choose a quick template or create a custom prompt
4. Adjust response format settings
5. Click "Generate Response"

### Python API

```python
from openai_responses import OpenAIResponsesAPI

# Initialize the API client
api = OpenAIResponsesAPI()

# Generate a response
response = api.generate_response(
    prompt="Write a professional email declining a meeting request",
    response_format={
        "type": "email",
        "style": "professional",
        "tone": "polite"
    }
)

print(response.content)
```

## Project Structure

```
openai-responses-demo/
├── src/
│   └── openai_responses/
│       ├── __init__.py
│       ├── client.py
│       ├── models.py
│       └── exceptions.py
├── app.py                 # Streamlit web interface
├── run_app.py            # Web interface launcher
├── main.py               # Command line demo
├── requirements.txt
├── pyproject.toml
├── .python-version
└── README.md
```

## License

MIT License 