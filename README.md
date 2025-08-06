# OpenAI Responses API Python Interface

A clean, type-safe Python interface for OpenAI's Responses API, featuring comprehensive tool calling support for both function tools and hosted tools.

## 🚀 Features

- **Structured Response Generation**: Generate emails, letters, messages, and custom responses
- **Tool Calling Support**: Full support for function tools and hosted tools
- **Type Safety**: Built with Pydantic for robust data validation
- **Error Handling**: Comprehensive exception handling with retry logic
- **Web Interface**: Streamlit-based web UI for interactive usage
- **Multiple Response Types**: Email, letter, message, and custom formats
- **Customizable Parameters**: Temperature, top-p, model selection, and more
- **Hosted Tools**: Support for OpenAI's hosted tools
- **Function Tools**: Custom function definitions with JSON schema

## 📦 Installation

### Prerequisites

- Python 3.13 or higher
- OpenAI API key

### Quick Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd openai-responses-demo
   ```

2. **Set up Python environment**:
   ```bash
   pyenv shell 3.13
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your API key**:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

### Automated Installation

**Unix/macOS**:
```bash
chmod +x install.sh
./install.sh
```

**Windows**:
```cmd
install.bat
```

## 🎯 Quick Start

### Basic Usage

```python
from openai_responses import OpenAIResponsesAPI, ResponseFormat

# Initialize the API client
api = OpenAIResponsesAPI()

# Create a response format
response_format = ResponseFormat(
    type="email",
    style="professional",
    tone="polite",
    length="medium"
)

# Generate a response
response = api.generate_response(
    prompt="Write a professional email declining a meeting request",
    response_format=response_format
)

print(response.content)
```

### Tool Calling with Function Tools

```python
from openai_responses import OpenAIResponsesAPI, Tool, ToolFunction

# Initialize the API client
api = OpenAIResponsesAPI()

# Create a custom function tool (your own function)
weather_tool = Tool(
    type="function",
    function=ToolFunction(
        name="get_weather",
        description="Get the current weather in a given location",
        parameters={
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "The temperature unit to use"
                }
            },
            "required": ["location"]
        }
    )
)

# Generate response with your custom function tool
response = api.generate_response(
    prompt="What's the weather like in New York City?",
    response_format={"type": "message", "style": "casual"},
    tools=[weather_tool],
    tool_choice="auto"
)

print(response.content)

# Check for tool calls
if response.tool_calls:
    for tool_call in response.tool_calls:
        print(f"Tool call: {tool_call.function}")
```

### Tool Calling with Hosted Tools

```python
from openai_responses import OpenAIResponsesAPI, Tool

# Initialize the API client
api = OpenAIResponsesAPI()

# Create a hosted tool reference (OpenAI's pre-built tools)
web_search_tool = Tool(
    type="web_search_preview"
)

# Generate response with OpenAI's hosted tool
response = api.generate_response(
    prompt="Search for the latest news about AI developments",
    response_format={"type": "message", "style": "professional"},
    tools=[web_search_tool],
    tool_choice="auto"
)

print(response.content)
```

### Available OpenAI Hosted Tools

OpenAI provides 5 pre-built hosted tools that you can use:

1. **`file_search`** - Search through files in your workspace
2. **`web_search_preview`** - Search the web for current information
3. **`computer_use_preview`** - Interact with your computer (file operations, etc.)
4. **`code_interpreter`** - Execute and analyze code
5. **`image_generation`** - Generate images using DALL-E

### Response-Specific Methods

```python
# Email response with hosted tool
email_response = api.create_email_response(
    prompt="Search for the latest market trends and include them in a professional email.",
    style="professional",
    tone="polite",
    tools=[web_search_tool],
    tool_choice="auto"
)

# Letter response with custom function tool
letter_response = api.create_letter_response(
    prompt="Write a formal letter explaining the weather calculation for our outdoor event planning.",
    style="formal",
    tone="professional",
    tools=[weather_tool],
    tool_choice="auto"
)

# Message response with multiple tools
message_response = api.create_message_response(
    prompt="Search for current events and calculate some statistics for a friendly message.",
    style="casual",
    tone="friendly",
    tools=[web_search_tool, calculator_tool],
    tool_choice="auto"
)
```

## 🌐 Web Interface

Launch the interactive web interface:

```bash
python run_app.py
```

Or directly with Streamlit:

```bash
streamlit run app.py
```

### Web Interface Features

- **Interactive Parameter Configuration**: Adjust model, temperature, top-p, and more
- **Tool Calling Support**: Configure function tools and hosted tools
- **Response Format Customization**: Choose type, style, tone, and length
- **Quick Templates**: Pre-built templates for common use cases
- **Real-time Response Generation**: See results immediately
- **Tool Call Visualization**: View and inspect tool calls made by the model
- **Markdown Rendering**: Beautiful, formatted responses with proper styling
- **Raw Text Toggle**: Switch between rendered and raw text views

## 📚 Examples

### Command Line Examples

Run the main demo:
```bash
python main.py
```

Run comprehensive tool calling examples:
```bash
python tool_calling_example.py
```

### Tool Choice Options

```python
# Auto: Let the model decide when to use tools
response = api.generate_response(
    prompt="What's the weather like?",
    tools=[weather_tool],
    tool_choice="auto"
)

# None: Prevent tool usage
response = api.generate_response(
    prompt="What's the weather like?",
    tools=[weather_tool],
    tool_choice="none"
)

# Specific: Force use of a particular tool
response = api.generate_response(
    prompt="What's the weather like?",
    tools=[weather_tool],
    tool_choice={"type": "function", "function": {"name": "get_weather"}}
)
```

## 🔧 Configuration

### Response Format Options

- **Type**: `email`, `letter`, `message`, `response`, `reply`, `note`
- **Style**: `professional`, `casual`, `formal`, `friendly`, `business`
- **Tone**: `friendly`, `polite`, `assertive`, `neutral`, `enthusiastic`, `sympathetic`, `professional`
- **Length**: `short`, `medium`, `long`
- **Language**: Language code (e.g., `en`, `es`, `fr`)

### Tool Types

1. **Function Tools**: Custom functions with JSON schema parameters
2. **Hosted Tools**: Pre-built tools from your OpenAI account

### Tool Choice Options

- **`auto`**: Model decides when to use tools
- **`none`**: Prevent tool usage
- **Specific tool**: Force use of a particular tool

## 🛠️ Development

### Project Structure

```
openai-responses-demo/
├── src/
│   └── openai_responses/
│       ├── __init__.py
│       ├── client.py          # Main API client
│       ├── models.py          # Pydantic models
│       └── exceptions.py      # Custom exceptions
├── app.py                     # Streamlit web interface
├── main.py                    # Command line demo
├── tool_calling_example.py    # Comprehensive tool examples
├── run_app.py                 # Web interface launcher
├── requirements.txt           # Python dependencies
├── pyproject.toml            # Project configuration
└── README.md                 # This file
```

### Running Tests

```bash
python test_import.py
```

### Building the Package

```bash
pip install build
python -m build
```

## 📖 API Reference

### OpenAIResponsesAPI

Main client class for interacting with the OpenAI Responses API.

#### Methods

- `generate_response()`: Generate a response with optional tools
- `create_email_response()`: Generate an email response
- `create_letter_response()`: Generate a letter response
- `create_message_response()`: Generate a message response
- `create_function_tool()`: Create a function tool
- `create_hosted_tool()`: Create a hosted tool reference

### Models

- `ResponseFormat`: Configuration for response generation
- `Tool`: Tool definition (function or hosted)
- `ToolFunction`: Function tool with parameters
- `ToolCall`: Tool call in response
- `ResponseResponse`: API response with content and metadata

### Exceptions

- `OpenAIResponsesError`: Base exception class
- `APIError`: API-related errors
- `AuthenticationError`: Authentication failures
- `ValidationError`: Input validation errors
- `RateLimitError`: Rate limit exceeded
- `QuotaExceededError`: Quota exceeded

## 🔒 Error Handling

The library provides comprehensive error handling:

```python
try:
    response = api.generate_response(prompt, response_format)
except AuthenticationError:
    # Handle authentication issues
except APIError as e:
    # Handle API errors
except ValidationError:
    # Handle validation errors
except RateLimitError:
    # Handle rate limiting
except QuotaExceededError:
    # Handle quota issues
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:

1. Check the [OpenAI Responses API documentation](https://platform.openai.com/docs/api-reference/responses)
2. Review the examples in this repository
3. Open an issue on GitHub

## 🔄 Updates

Stay updated with the latest features:

- **Tool Calling**: Full support for function and hosted tools
- **Web Interface**: Interactive Streamlit-based UI
- **Enhanced Error Handling**: Comprehensive exception management
- **Type Safety**: Pydantic models for robust validation 