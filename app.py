#!/usr/bin/env python3
"""
Streamlit Web Interface for OpenAI Responses API

A user-friendly web interface for generating structured responses using OpenAI's Responses API.
"""

import os
import sys
import streamlit as st
from typing import Dict, Any, Optional

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from openai_responses import OpenAIResponsesAPI, ResponseFormat
from openai_responses.exceptions import APIError, AuthenticationError


def setup_page():
    """Configure the Streamlit page."""
    st.set_page_config(
        page_title="OpenAI Responses API",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🚀 OpenAI Responses API")
    st.markdown("Generate structured responses with customizable parameters")


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
        ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
        index=0,
        help="Select the OpenAI model to use for generation."
    )
    
    # Temperature slider
    temperature = st.sidebar.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Controls randomness. Lower values are more deterministic, higher values more creative."
    )
    
    # Top-p slider
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


def create_response_format_section():
    """Create the response format configuration section."""
    st.header("📝 Response Format")
    
    col1, col2 = st.columns(2)
    
    with col1:
        response_type = st.selectbox(
            "Response Type",
            ["email", "letter", "message", "response", "reply", "note"],
            index=0,
            help="Type of response to generate."
        )
        
        style = st.selectbox(
            "Style",
            ["professional", "casual", "formal", "friendly", "business"],
            index=0,
            help="Writing style for the response."
        )
        
        length = st.selectbox(
            "Length",
            ["short", "medium", "long"],
            index=1,
            help="Desired length of the response."
        )
    
    with col2:
        tone = st.selectbox(
            "Tone",
            ["friendly", "polite", "assertive", "neutral", "enthusiastic", "sympathetic", "professional"],
            index=1,
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
    
    prompt = st.text_area(
        "Enter your prompt",
        height=150,
        placeholder="Describe what kind of response you want to generate. For example: 'Write an email declining a meeting request due to a scheduling conflict'",
        help="Describe the response you want to generate. Be specific about the context and requirements."
    )
    
    return prompt


def create_quick_templates():
    """Create quick template buttons."""
    st.header("🎯 Quick Templates")
    
    col1, col2, col3 = st.columns(3)
    
    templates = {
        "📧 Professional Email": {
            "prompt": "Write a professional email declining a meeting request from a colleague due to a scheduling conflict",
            "format": {"type": "email", "style": "professional", "tone": "polite", "length": "short"}
        },
        "📝 Formal Letter": {
            "prompt": "Write a formal letter of recommendation for a former employee",
            "format": {"type": "letter", "style": "formal", "tone": "professional", "length": "long"}
        },
        "💬 Casual Message": {
            "prompt": "Write a friendly message to congratulate someone on their promotion",
            "format": {"type": "message", "style": "casual", "tone": "friendly", "length": "short"}
        },
        "🙏 Thank You Note": {
            "prompt": "Write a thank you message for a birthday gift from a friend",
            "format": {"type": "message", "style": "casual", "tone": "enthusiastic", "length": "medium"}
        },
        "📋 Meeting Confirmation": {
            "prompt": "Write a brief email confirming receipt of an important document",
            "format": {"type": "email", "style": "professional", "tone": "neutral", "length": "short"}
        },
        "🎉 Celebration": {
            "prompt": "Write a creative story about a magical forest",
            "format": {"type": "message", "style": "casual", "tone": "enthusiastic", "length": "long"}
        }
    }
    
    for i, (template_name, template_data) in enumerate(templates.items()):
        col = [col1, col2, col3][i % 3]
        with col:
            if st.button(template_name, key=f"template_{i}"):
                st.session_state.prompt = template_data["prompt"]
                st.session_state.response_format = template_data["format"]
                st.rerun()


def generate_response(api_key: str, prompt: str, response_format: Dict[str, Any], config: Dict[str, Any]):
    """Generate a response using the API."""
    try:
        # Initialize API client
        api = OpenAIResponsesAPI(
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            timeout=30
        )
        
        # Create response format object
        format_obj = ResponseFormat(**response_format)
        
        # Generate response
        response = api.generate_response(
            prompt=prompt,
            response_format=format_obj,
            model=config["model"],
            temperature=config["temperature"],
            top_p=config["top_p"]
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
    st.header("📤 Generated Response")
    
    if error:
        st.error(error)
        return
    
    if response:
        # Display the response content
        st.subheader("Content")
        st.text_area(
            "Generated Response",
            value=response.content,
            height=300,
            disabled=True,
            key="response_content"
        )
        
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
    
    # Create sidebar
    config = create_sidebar()
    
    # Create main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Quick templates
        create_quick_templates()
        
        # Prompt input
        prompt = create_prompt_section()
        
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
                    response, error = generate_response(
                        api_key=config["api_key"],
                        prompt=prompt,
                        response_format=response_format,
                        config=config
                    )
                    display_response(response, error)
    
    with col2:
        # Display current configuration
        st.header("⚙️ Current Settings")
        
        st.subheader("Model Configuration")
        st.write(f"**Model:** {config['model']}")
        st.write(f"**Temperature:** {config['temperature']}")
        st.write(f"**Top-p:** {config['top_p']}")
        
        st.subheader("Response Format")
        st.write(f"**Type:** {response_format['type']}")
        st.write(f"**Style:** {response_format['style']}")
        st.write(f"**Tone:** {response_format['tone']}")
        st.write(f"**Length:** {response_format['length']}")
        st.write(f"**Language:** {response_format['language']}")
        
        # API status
        st.subheader("🔑 API Status")
        if config["api_key"] or os.getenv("OPENAI_API_KEY"):
            st.success("API key configured")
        else:
            st.warning("No API key provided")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "Built with ❤️ using [Streamlit](https://streamlit.io) and [OpenAI Responses API](https://platform.openai.com/docs/api-reference/responses)"
    )


if __name__ == "__main__":
    main() 