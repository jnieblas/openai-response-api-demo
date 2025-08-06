# Web Interface Demo Guide

## 🚀 Getting Started

### 1. Launch the Web Interface

```bash
# Method 1: Using the launcher script (recommended)
python run_app.py

# Method 2: Direct Streamlit command
streamlit run app.py
```

### 2. Open Your Browser

The app will automatically open at: `http://localhost:8501`

## 🎯 Using the Interface

### Quick Start with Templates

1. **Choose a Template**: Click one of the quick template buttons:
   - 📧 Professional Email
   - 📝 Formal Letter
   - 💬 Casual Message
   - 🙏 Thank You Note
   - 📋 Meeting Confirmation
   - 🎉 Creative Story

2. **Enter API Key**: In the sidebar, enter your OpenAI API key

3. **Generate**: Click "🚀 Generate Response"

### Custom Prompts

1. **Enter Your Prompt**: Write a detailed description of what you want to generate

2. **Configure Format**:
   - **Type**: email, letter, message, response, reply, note
   - **Style**: professional, casual, formal, friendly, business
   - **Tone**: friendly, polite, assertive, neutral, enthusiastic, sympathetic, professional
   - **Length**: short, medium, long
   - **Language**: en (English), or other language codes

3. **Adjust Parameters** (in sidebar):
   - **Model**: Choose from gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-3.5-turbo
   - **Temperature**: 0.0-2.0 (creativity control)
   - **Top-p**: 0.0-1.0 (diversity control)

4. **Generate**: Click the generate button

## 📊 Understanding the Results

### Response Display
- **Content**: The generated text in a scrollable area
- **Token Usage**: 
  - Total Tokens: Complete token count
  - Prompt Tokens: Input tokens used
  - Completion Tokens: Output tokens generated

### Response Details
Click "📊 Response Details" to see:
- Response ID
- Model used
- Status
- Finish reason
- Creation timestamp

## 🔧 Configuration Options

### API Key
- Enter in the sidebar (secure password field)
- Or set as environment variable: `export OPENAI_API_KEY="your-key"`

### Model Settings
- **Temperature**: Lower = more deterministic, Higher = more creative
- **Top-p**: Lower = more focused, Higher = more diverse

### Response Format
- **Type**: Determines the structure (email, letter, etc.)
- **Style**: Writing style and formality
- **Tone**: Emotional tone of the response
- **Length**: Controls response length
- **Language**: Language code for the response

## 🎨 Example Use Cases

### Professional Email
```
Prompt: "Write an email declining a meeting request due to scheduling conflict"
Type: email
Style: professional
Tone: polite
Length: short
```

### Creative Story
```
Prompt: "Write a story about a magical forest"
Type: message
Style: casual
Tone: enthusiastic
Length: long
Temperature: 0.9 (more creative)
```

### Formal Letter
```
Prompt: "Write a letter of recommendation for a former employee"
Type: letter
Style: formal
Tone: professional
Length: long
```

## 🛠️ Troubleshooting

### Common Issues

1. **"No API key provided"**
   - Enter your API key in the sidebar
   - Or set environment variable: `export OPENAI_API_KEY="your-key"`

2. **"Authentication error"**
   - Check that your API key is valid
   - Ensure you have access to the Responses API

3. **"API error"**
   - Check your internet connection
   - Verify API key permissions
   - Check OpenAI service status

4. **App won't start**
   - Install dependencies: `pip install -r requirements.txt`
   - Check Python version: `python --version` (should be 3.13+)

### Getting Help

- Check the console output for detailed error messages
- Verify your OpenAI API key has the necessary permissions
- Ensure you have sufficient API credits

## 🎉 Tips for Best Results

1. **Be Specific**: Detailed prompts generate better responses
2. **Use Templates**: Start with templates and customize
3. **Experiment**: Try different temperatures and formats
4. **Save Good Prompts**: Copy successful prompts for reuse
5. **Check Token Usage**: Monitor costs with the token counters 