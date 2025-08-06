# OpenAI Responses API Python Interface

A Python interface for the OpenAI Responses API, providing a clean and type-safe way to interact with OpenAI's structured response generation service.

## Features

- 🚀 Clean, type-safe Python interface for OpenAI Responses API
- 📦 Easy installation and dependency management
- 🔧 Configurable response formats and parameters
- 🛡️ Error handling and validation
- 📝 Comprehensive examples and documentation

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

1. Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

2. Run the example:
```bash
python main.py
```

## Usage

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
├── main.py
├── requirements.txt
├── pyproject.toml
├── .python-version
└── README.md
```

## License

MIT License 