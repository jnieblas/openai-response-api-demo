#!/usr/bin/env python3
"""
Streamlit Web Interface for OpenAI Responses API

A user-friendly web interface for generating structured responses using OpenAI's Responses API.
"""

import os
import sys
import streamlit as st
import json
from typing import Dict, Any, Optional, List

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from openai_responses import OpenAIResponsesAPI, ResponseFormat, Tool, ToolFunction
from openai_responses.exceptions import APIError, AuthenticationError


def setup_page():
    """Setup the Streamlit page configuration."""
    st.set_page_config(
        page_title="OpenAI Responses API Interface",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Add custom CSS for better markdown rendering
    st.markdown("""
    <style>
    /* Style only the response content markdown */
    .response-markdown {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #007bff;
        margin: 1rem 0;
    }
    
    /* Style headings in response content */
    .response-markdown h1, 
    .response-markdown h2, 
    .response-markdown h3 {
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Style lists in response content */
    .response-markdown ul, 
    .response-markdown ol {
        margin-left: 1.5rem;
    }
    
    .response-markdown li {
        margin-bottom: 0.25rem;
    }
    
    /* Style blockquotes in response content */
    .response-markdown blockquote {
        border-left: 4px solid #6c757d;
        padding-left: 1rem;
        margin: 1rem 0;
        color: #6c757d;
    }
    
    /* Style code in response content */
    .response-markdown code {
        background-color: #e9ecef;
        padding: 0.2rem 0.4rem;
        border-radius: 0.25rem;
        font-family: 'Courier New', monospace;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🤖 OpenAI Responses API Interface")
    st.markdown("Generate structured responses using OpenAI's Responses API with support for tools and custom formatting.")


def create_sidebar():
    """Create the sidebar with configuration options."""
    st.sidebar.header("⚙️ Configuration")
    
    # API Key input
    api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Enter your OpenAI API key. You can also set it as OPENAI_API_KEY environment variable."
    )
    
    # Model selection
    model = st.sidebar.selectbox(
        "Model",
        ["gpt-5","gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
        index=0,
        help="Select the OpenAI model to use for generation."
    )
    
    # Conditional parameters based on model
    if model == "gpt-5":
        # GPT-5 specific parameters
        st.sidebar.subheader("GPT-5 Parameters")
        
        effort = st.sidebar.selectbox(
            "Effort",
            ["low", "medium", "high"],
            index=1,
            help="Controls how much effort the model puts into generating the response."
        )
        
        verbosity = st.sidebar.selectbox(
            "Verbosity",
            ["low", "medium", "high"],
            index=1,
            help="Controls the level of detail in the response."
        )
        
        return {
            "api_key": api_key,
            "model": model,
            "effort": effort,
            "verbosity": verbosity
        }
    else:
        # Traditional parameters for other models
        st.sidebar.subheader("Generation Parameters")
        
        temperature = st.sidebar.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            help="Controls randomness. Lower values are more deterministic, higher values more creative."
        )
        
        top_p = st.sidebar.slider(
            "Top-p",
            min_value=0.0,
            max_value=1.0,
            value=1.0,
            step=0.1,
            help="Controls diversity via nucleus sampling. Lower values focus on most likely tokens."
        )
        
        return {
            "api_key": api_key,
            "model": model,
            "temperature": temperature,
            "top_p": top_p
        }


def create_tools_section():
    """Create the tools configuration section."""
    st.header("🔧 Tools Configuration")
    
    # Enable tools (default to True)
    enable_tools = st.checkbox(
        "Enable Tool Calling",
        value=True,
        help="Enable function tools (your custom functions) or hosted tools (OpenAI's pre-built tools)."
    )
    
    if not enable_tools:
        return None, None
    
    # Tool type selection (default to hosted_tool)
    tool_type = st.selectbox(
        "Tool Type",
        ["hosted_tool", "function"],
        index=0,
        help="Choose between hosted tools (OpenAI's pre-built tools) or function tools (your custom functions)."
    )
    
    tools = []
    tool_choice = "auto"
    
    if tool_type == "hosted_tool":
        # Hosted tool configuration (OpenAI's pre-built tools)
        st.subheader("OpenAI Hosted Tools")
        
        hosted_tool_options = {
            "file_search": "Search through files in your workspace",
            "web_search_preview": "Search the web for current information",
            "computer_use_preview": "Interact with your computer (file operations, etc.)",
            "code_interpreter": "Execute and analyze code",
            "image_generation": "Generate images using DALL-E"
        }
        
        selected_hosted_tools = st.multiselect(
            "Select Hosted Tools",
            options=list(hosted_tool_options.keys()),
            default=["web_search_preview"],
            help="Choose which OpenAI hosted tools to make available to the model."
        )
        
        # Create hosted tool objects
        for tool_id in selected_hosted_tools:
            tool = Tool(type=tool_id)
            tools.append(tool)
        
        # Show selected tools info
        if selected_hosted_tools:
            st.subheader("Selected Hosted Tools")
            for tool_id in selected_hosted_tools:
                with st.expander(f"📋 {tool_id}"):
                    st.write(f"**Description:** {hosted_tool_options[tool_id]}")
                    st.write(f"**Tool ID:** `{tool_id}`")
    
    elif tool_type == "function":
        # Function tool configuration (your custom functions)
        st.subheader("Custom Function Tools")
        st.info("These are custom functions that you define with your own JSON schema.")
        
        # Function tool configuration
        function_name = st.text_input(
            "Function Name",
            value="get_weather",
            help="Name of your custom function."
        )
        
        function_description = st.text_area(
            "Function Description",
            value="Get the current weather in a given location",
            help="Description of what your function does."
        )
        
        # Parameters configuration
        st.subheader("Function Parameters")
        st.write("Define the JSON schema for your function parameters:")
        
        # Simple parameter builder
        num_params = st.number_input(
            "Number of Parameters",
            min_value=1,
            max_value=10,
            value=1,
            help="How many parameters does your function need?"
        )
        
        parameters = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        for i in range(num_params):
            st.write(f"**Parameter {i+1}:**")
            col1, col2 = st.columns(2)
            
            with col1:
                param_name = st.text_input(
                    f"Parameter Name {i+1}",
                    value=f"param_{i+1}",
                    key=f"param_name_{i}"
                )
                
                param_type = st.selectbox(
                    f"Parameter Type {i+1}",
                    ["string", "number", "integer", "boolean", "array", "object"],
                    key=f"param_type_{i}"
                )
                
                is_required = st.checkbox(
                    f"Required {i+1}",
                    value=True,
                    key=f"required_{i}"
                )
            
            with col2:
                param_desc = st.text_input(
                    f"Parameter Description {i+1}",
                    value=f"Description for parameter {i+1}",
                    key=f"param_desc_{i}"
                )
                
                # Add enum support for strings
                if param_type == "string":
                    use_enum = st.checkbox(
                        f"Use Enum Values {i+1}",
                        key=f"use_enum_{i}"
                    )
                    if use_enum:
                        enum_values = st.text_input(
                            f"Enum Values (comma-separated) {i+1}",
                            value="option1,option2,option3",
                            key=f"enum_values_{i}"
                        )
                        enum_list = [v.strip() for v in enum_values.split(",")]
                        parameters["properties"][param_name] = {
                            "type": param_type,
                            "description": param_desc,
                            "enum": enum_list
                        }
                    else:
                        parameters["properties"][param_name] = {
                            "type": param_type,
                            "description": param_desc
                        }
                else:
                    parameters["properties"][param_name] = {
                        "type": param_type,
                        "description": param_desc
                    }
                
                if is_required:
                    parameters["required"].append(param_name)
            
            st.divider()
        
        # Create tool
        if function_name and function_description:
            tool = Tool(
                type="function",
                function=ToolFunction(
                    name=function_name,
                    description=function_description,
                    parameters=parameters
                )
            )
            tools.append(tool)
            
            # Show the generated JSON schema
            st.subheader("Generated JSON Schema")
            with st.expander("View Function Schema"):
                st.json(parameters)
    
    # Tool choice configuration
    st.subheader("Tool Choice")
    tool_choice = st.selectbox(
        "Tool Choice",
        ["auto", "none"],
        help="'auto' lets the model decide when to use tools, 'none' prevents tool usage."
    )
    
    # Show tool configuration summary
    if tools:
        st.subheader("📋 Tool Configuration Summary")
        for i, tool in enumerate(tools):
            with st.expander(f"Tool {i+1}: {tool.type}"):
                if tool.type in ["code_interpreter", "file_search", "web_search_preview", "web_search_preview_2025_03_11", "image_generation", "mcp", "computer_use_preview"]:
                    st.write(f"**Type:** OpenAI Hosted Tool")
                    st.write(f"**Tool ID:** `{tool.type}`")
                    if tool.type in hosted_tool_options:
                        st.write(f"**Description:** {hosted_tool_options[tool.type]}")
                else:
                    st.write(f"**Type:** Function Tool")
                    st.write(f"**Function Name:** `{tool.function.name}`")
                    st.write(f"**Description:** {tool.function.description}")
                    st.write("**Parameters:**")
                    st.json(tool.function.parameters)
    
    return tools, tool_choice


def create_response_format_section():
    """Create the response format configuration section."""
    st.header("📝 Response Format")
    
    col1, col2 = st.columns(2)
    
    with col1:
        response_type = st.selectbox(
            "Response Type",
            ["email", "letter", "message", "response", "reply", "note"],
            index=3,  # "response" is at index 3
            help="Type of response to generate."
        )
        
        style = st.selectbox(
            "Style",
            ["professional", "casual", "formal", "friendly", "business"],
            index=1,  # "casual" is at index 1
            help="Writing style for the response."
        )
        
        length = st.selectbox(
            "Length",
            ["short", "medium", "long"],
            index=0,  # "short" is at index 0
            help="Desired length of the response."
        )
    
    with col2:
        tone = st.selectbox(
            "Tone",
            ["friendly", "polite", "assertive", "neutral", "enthusiastic", "sympathetic", "professional"],
            index=3,  # "neutral" is at index 3
            help="Tone of the response."
        )
        
        language = st.text_input(
            "Language",
            value="en",
            help="Language code for the response (e.g., 'en' for English)."
        )
    
    return {
        "type": response_type,
        "style": style,
        "tone": tone,
        "length": length,
        "language": language
    }


def create_prompt_section():
    """Create the prompt input section."""
    st.header("💭 Prompt")
    
    # Add custom CSS for black X button
    st.markdown("""
    <style>
    /* Style the clear conversation button to be black */
    div[data-testid="stButton"] button[kind="secondary"] {
        background-color: #000000 !important;
        color: white !important;
        border-color: #000000 !important;
        font-weight: bold !important;
    }
    
    div[data-testid="stButton"] button[kind="secondary"]:hover {
        background-color: #333333 !important;
        border-color: #333333 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create a row with prompt input and clear button
    col1, col2 = st.columns([20, 1])
    
    with col1:
        prompt = st.text_area(
            "Enter your prompt",
            height=150,
            placeholder="Describe what kind of response you want to generate. For example: 'Write an email declining a meeting request due to a scheduling conflict'",
            help="Describe the response you want to generate. Be specific about the context and requirements."
        )
    
    with col2:
        # Add spacing to align with the text area
        st.write("")  # Empty space for alignment
        st.write("")  # More spacing
        
        # Clear conversation button with black X and styling
        if st.button(
            "✕", 
            help="Clear conversation context", 
            key="clear_conversation",
            use_container_width=True,
            type="secondary"
        ):
            st.session_state.conversation_history = []
            st.session_state.last_response = None
            st.session_state.last_error = None
            st.rerun()
    
    return prompt


def generate_response(api_key: str, prompt: str, response_format: Dict[str, Any], config: Dict[str, Any], tools: Optional[List[Tool]] = None, tool_choice: Optional[str] = None, previous_response_id: Optional[str] = None):
    """Generate a response using the API."""
    try:
        # Initialize API client
        api = OpenAIResponsesAPI(
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            timeout=30
        )
        
        # Create response format object
        format_obj = ResponseFormat(**response_format)
        
        # Prepare parameters based on model
        if config["model"] == "gpt-5":
            # GPT-5 uses effort and verbosity
            response = api.generate_response(
                prompt=prompt,
                response_format=format_obj,
                model=config["model"],
                tools=tools,
                tool_choice=tool_choice,
                previous_response_id=previous_response_id
            )
        else:
            # Traditional models use temperature and top_p
            response = api.generate_response(
                prompt=prompt,
                response_format=format_obj,
                model=config["model"],
                temperature=config.get("temperature"),
                top_p=config.get("top_p"),
                tools=tools,
                tool_choice=tool_choice,
                previous_response_id=previous_response_id
            )
        
        return response, None
        
    except AuthenticationError as e:
        return None, f"Authentication error: {e}. Please check your API key."
    except APIError as e:
        return None, f"API error: {e}"
    except Exception as e:
        return None, f"Unexpected error: {e}"


def display_response(response, error: Optional[str] = None):
    """Display the generated response or error."""
    st.header("�� Generated Response")
    
    if error:
        st.error(error)
        return
    
    if response:
        # Display the response content
        st.subheader("Content")
        
        # Add toggle for raw text view with proper key
        col1, col2 = st.columns([1, 4])
        with col1:
            show_raw = st.checkbox(
                "Show Raw Text", 
                key="show_raw_text_checkbox",
                help="Toggle to see the raw markdown text instead of rendered content"
            )
        with col2:
            if show_raw:
                st.info("📄 Showing raw markdown text")
            else:
                st.info("🎨 Showing rendered markdown")
        
        # Use markdown to render the content properly
        if response.content:
            if show_raw:
                st.text_area(
                    "Raw Response Text",
                    value=response.content,
                    height=300,
                    disabled=True,
                    key="response_content_raw"
                )
            else:
                # Render markdown with custom styling
                st.markdown(f"""
                <div class="response-markdown">
                {response.content}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No content generated.")
        
        # Display tool calls if any
        if response.tool_calls:
            st.subheader("🔧 Tool Calls")
            for i, tool_call in enumerate(response.tool_calls):
                with st.expander(f"Tool Call {i+1}: {tool_call.id}"):
                    st.json({
                        "id": tool_call.id,
                        "type": tool_call.type,
                        "function": tool_call.function,
                        "hosted_tool": tool_call.hosted_tool
                    })
        
        # Display metadata
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Tokens", response.total_tokens)
        
        with col2:
            st.metric("Prompt Tokens", response.prompt_tokens)
        
        with col3:
            st.metric("Completion Tokens", response.completion_tokens)
        
        # Display additional info
        with st.expander("📊 Response Details"):
            st.json({
                "id": response.id,
                "model": response.model,
                "status": response.status,
                "finish_reason": response.finish_reason,
                "created_at": response.created_at
            })


def main():
    """Main Streamlit application."""
    setup_page()
    
    # Initialize session state
    if "prompt" not in st.session_state:
        st.session_state.prompt = ""
    if "response_format" not in st.session_state:
        st.session_state.response_format = {}
    if "last_response" not in st.session_state:
        st.session_state.last_response = None
    if "last_error" not in st.session_state:
        st.session_state.last_error = None
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    
    # Create sidebar
    config = create_sidebar()
    
    # Create main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Display conversation history
        if st.session_state.conversation_history:
            st.subheader("📜 Conversation History")
            
            # Show warning if conversation is getting long
            if len(st.session_state.conversation_history) >= 8:
                st.warning("⚠️ Conversation history is getting long. Consider starting a new conversation for better performance.")
            
            for i, (user_msg, assistant_msg) in enumerate(st.session_state.conversation_history):
                with st.expander(f"Exchange {i+1}", expanded=False):
                    st.write("**👤 You:**")
                    st.write(user_msg)
                    st.write("**🤖 Assistant:**")
                    st.markdown(f"""
                    <div class="response-markdown">
                    {assistant_msg}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Prompt input
        prompt = create_prompt_section()
        
        # Tools configuration
        tools, tool_choice = create_tools_section()
        
        # Response format configuration
        response_format = create_response_format_section()
        
        # Generate button
        if st.button("🚀 Generate Response", type="primary", use_container_width=True):
            if not prompt.strip():
                st.error("Please enter a prompt.")
            elif not (config["api_key"] or os.getenv("OPENAI_API_KEY")):
                st.error("Please provide an OpenAI API key.")
            else:
                with st.spinner("Generating response..."):
                    # Get previous response ID for conversation continuity
                    previous_response_id = None
                    if st.session_state.last_response:
                        previous_response_id = st.session_state.last_response.id
                    
                    response, error = generate_response(
                        api_key=config["api_key"],
                        prompt=prompt,
                        response_format=response_format,
                        config=config,
                        tools=tools,
                        tool_choice=tool_choice,
                        previous_response_id=previous_response_id
                    )
                    
                    if response and not error:
                        # Add to conversation history for display purposes
                        st.session_state.conversation_history.append((prompt, response.content))
                        # Limit history to last 10 exchanges for display
                        if len(st.session_state.conversation_history) > 10:
                            st.session_state.conversation_history = st.session_state.conversation_history[-10:]
                    
                    st.session_state.last_response = response
                    st.session_state.last_error = error
                    st.rerun()
    
    # Always display the last response if it exists
    if st.session_state.last_response or st.session_state.last_error:
        display_response(st.session_state.last_response, st.session_state.last_error)
    
    with col2:
        # Display current configuration
        st.header("⚙️ Current Settings")
        
        st.subheader("Model Configuration")
        st.write(f"**Model:** {config['model']}")
        
        # Display model-specific parameters
        if config['model'] == "gpt-5":
            st.write(f"**Effort:** {config['effort']}")
            st.write(f"**Verbosity:** {config['verbosity']}")
        else:
            st.write(f"**Temperature:** {config['temperature']}")
            st.write(f"**Top-p:** {config['top_p']}")
        
        st.subheader("Response Format")
        st.write(f"**Type:** {response_format['type']}")
        st.write(f"**Style:** {response_format['style']}")
        st.write(f"**Tone:** {response_format['tone']}")
        st.write(f"**Length:** {response_format['length']}")
        st.write(f"**Language:** {response_format['language']}")
        
        # Tool configuration
        if tools:
            st.subheader("🔧 Tools")
            st.write(f"**Tools Enabled:** ✅")
            st.write(f"**Tool Choice:** {tool_choice}")
            st.write(f"**Number of Tools:** {len(tools)}")
        else:
            st.subheader("🔧 Tools")
            st.write("**Tools Enabled:** ❌")
        
        # API status
        st.subheader("🔑 API Status")
        if config["api_key"] or os.getenv("OPENAI_API_KEY"):
            st.success("API key configured")
        else:
            st.warning("No API key provided")
        
        # Conversation statistics
        st.subheader("💬 Conversation")
        exchange_count = len(st.session_state.conversation_history)
        if exchange_count > 0:
            st.metric("Exchanges", exchange_count)
            st.info(f"Current conversation has {exchange_count} exchange(s)")
        else:
            st.info("No conversation history yet")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "Built with ❤️ using [Streamlit](https://streamlit.io) and [OpenAI Responses API](https://platform.openai.com/docs/api-reference/responses)"
    )


if __name__ == "__main__":
    main() 