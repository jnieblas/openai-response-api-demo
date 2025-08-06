#!/usr/bin/env python3
"""
OpenAI Responses API Demo

This script demonstrates the usage of the OpenAI Responses API interface.
"""

import os
import sys
from typing import Dict, Any

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from openai_responses import OpenAIResponsesAPI, ResponseFormat, Tool, ToolFunction
from openai_responses.exceptions import APIError, AuthenticationError


def create_weather_tool() -> Tool:
    """Create a weather function tool."""
    weather_parameters = {
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
    
    return Tool(
        type="function",
        function=ToolFunction(
            name="get_weather",
            description="Get the current weather in a given location",
            parameters=weather_parameters
        )
    )


def demo_basic_usage():
    """Demonstrate basic API usage."""
    print("=" * 60)
    print("Basic Usage Demo")
    print("=" * 60)
    
    try:
        # Initialize API client
        api = OpenAIResponsesAPI()
        
        # Create response format
        response_format = ResponseFormat(
            type="email",
            style="professional",
            tone="polite",
            length="medium"
        )
        
        # Generate response
        response = api.generate_response(
            prompt="Write a professional email declining a meeting request due to a scheduling conflict",
            response_format=response_format,
            temperature=0.7
        )
        
        print(f"Generated Email:\n{response.content}")
        print(f"\nTokens used: {response.total_tokens}")
        print(f"Model: {response.model}")
        
    except Exception as e:
        print(f"Error: {e}")


def demo_advanced_parameters():
    """Demonstrate advanced parameter usage."""
    print("\n" + "=" * 60)
    print("Advanced Parameters Demo")
    print("=" * 60)
    
    try:
        # Initialize API client
        api = OpenAIResponsesAPI()
        
        # Generate response with custom parameters
        response = api.generate_response(
            prompt="Write a creative story about a magical forest",
            response_format={
                "type": "message",
                "style": "casual",
                "tone": "enthusiastic",
                "length": "long"
            },
            model="gpt-4o",
            temperature=0.9,
            top_p=0.8
        )
        
        print(f"Creative Story:\n{response.content}")
        print(f"\nTokens used: {response.total_tokens}")
        
    except Exception as e:
        print(f"Error: {e}")


def demo_tool_calling():
    """Demonstrate tool calling functionality."""
    print("\n" + "=" * 60)
    print("Tool Calling Demo")
    print("=" * 60)
    
    try:
        # Initialize API client
        api = OpenAIResponsesAPI()
        
        # Create a weather tool
        weather_tool = create_weather_tool()
        
        # Generate response with tool
        response = api.generate_response(
            prompt="What's the weather like in New York City? Please provide a detailed response.",
            response_format={
                "type": "message",
                "style": "casual",
                "tone": "friendly"
            },
            tools=[weather_tool],
            tool_choice="auto"
        )
        
        print(f"Response with Tool:\n{response.content}")
        
        # Check for tool calls
        if response.tool_calls:
            print(f"\nTool calls made: {len(response.tool_calls)}")
            for tool_call in response.tool_calls:
                print(f"Tool call ID: {tool_call.id}")
                print(f"Tool call type: {tool_call.type}")
                if tool_call.hosted_tool:
                    print(f"Hosted tool: {tool_call.hosted_tool}")
                elif tool_call.function:
                    print(f"Function: {tool_call.function}")
        
        print(f"\nTokens used: {response.total_tokens}")
        
    except Exception as e:
        print(f"Error: {e}")


def demo_response_methods():
    """Demonstrate response-specific methods."""
    print("\n" + "=" * 60)
    print("Response Methods Demo")
    print("=" * 60)
    
    try:
        # Initialize API client
        api = OpenAIResponsesAPI()
        
        # Create a calculator tool
        calculator_tool = Tool(
            type="function",
            function=ToolFunction(
                name="calculate",
                description="Perform basic mathematical operations",
                parameters={
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "enum": ["add", "subtract", "multiply", "divide"],
                            "description": "The mathematical operation to perform"
                        },
                        "a": {"type": "number", "description": "First number"},
                        "b": {"type": "number", "description": "Second number"}
                    },
                    "required": ["operation", "a", "b"]
                }
            )
        )
        
        # Email with tool
        print("\n1. Email Response with Tool")
        email_response = api.create_email_response(
            prompt="Calculate the total cost for 5 items at $12.50 each and include it in a professional email to the client.",
            style="professional",
            tone="polite",
            tools=[calculator_tool],
            tool_choice="auto"
        )
        print(f"Email: {email_response.content}")
        
        # Letter with tool
        print("\n2. Letter Response with Tool")
        letter_response = api.create_letter_response(
            prompt="Write a formal letter explaining the weather calculation for our outdoor event planning.",
            style="formal",
            tone="professional",
            tools=[create_weather_tool()],
            tool_choice="auto"
        )
        print(f"Letter: {letter_response.content}")
        
        # Message with tool
        print("\n3. Message Response with Tool")
        message_response = api.create_message_response(
            prompt="Send a friendly message to a friend with a quick calculation.",
            style="casual",
            tone="friendly",
            tools=[calculator_tool],
            tool_choice="auto"
        )
        print(f"Message: {message_response.content}")
        
    except Exception as e:
        print(f"Error: {e}")


def demo_hosted_tools():
    """Demonstrate hosted tools usage."""
    print("\n" + "=" * 60)
    print("Hosted Tools Demo")
    print("=" * 60)
    
    try:
        # Initialize API client
        api = OpenAIResponsesAPI()
        
        # Create hosted tool references (OpenAI's pre-built tools)
        web_search_tool = Tool(
            type="web_search_preview"
        )
        
        file_search_tool = Tool(
            type="file_search"
        )
        
        print("Using OpenAI's pre-built hosted tools:")
        print("- web_search_preview: Search the web for current information")
        print("- file_search: Search through files in your workspace")
        
        # Generate response with web search tool
        print("\n1. Web Search Tool Example")
        response = api.generate_response(
            prompt="Search for the latest news about AI developments and summarize them.",
            response_format={
                "type": "message",
                "style": "professional",
                "tone": "informative"
            },
            tools=[web_search_tool],
            tool_choice="auto"
        )
        
        print(f"Response: {response.content}")
        
        if response.tool_calls:
            print(f"\nWeb search tool calls made: {len(response.tool_calls)}")
            for tool_call in response.tool_calls:
                print(f"Tool call ID: {tool_call.id}")
                print(f"Tool call type: {tool_call.type}")
                if tool_call.hosted_tool:
                    print(f"Hosted tool: {tool_call.hosted_tool}")
        
        # Generate response with file search tool
        print("\n2. File Search Tool Example")
        response = api.generate_response(
            prompt="Search through available files to find information about the project structure.",
            response_format={
                "type": "message",
                "style": "casual",
                "tone": "helpful"
            },
            tools=[file_search_tool],
            tool_choice="auto"
        )
        
        print(f"Response: {response.content}")
        
        if response.tool_calls:
            print(f"\nFile search tool calls made: {len(response.tool_calls)}")
            for tool_call in response.tool_calls:
                print(f"Tool call ID: {tool_call.id}")
                print(f"Tool call type: {tool_call.type}")
                if tool_call.hosted_tool:
                    print(f"Hosted tool: {tool_call.hosted_tool}")
        
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Run all demos."""
    print("🚀 OpenAI Responses API Demo")
    print("This demo showcases the Python interface for OpenAI's Responses API")
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  Warning: OPENAI_API_KEY environment variable is not set.")
        print("   Set it with: export OPENAI_API_KEY='your-api-key-here'")
        print("   Some examples may fail without a valid API key.")
    
    # Run demos
    demo_basic_usage()
    demo_advanced_parameters()
    demo_tool_calling()
    demo_response_methods()
    demo_hosted_tools()
    
    print("\n" + "=" * 60)
    print("Demo Complete!")
    print("=" * 60)
    print("\nKey Features Demonstrated:")
    print("✅ Basic response generation")
    print("✅ Advanced parameter configuration")
    print("✅ Function tools with JSON schema")
    print("✅ Hosted tools with tool IDs")
    print("✅ Response-specific methods (email, letter, message)")
    print("✅ Tool call detection and handling")
    print("\nFor more examples, see:")
    print("- tool_calling_example.py (comprehensive tool examples)")
    print("- python run_app.py (web interface)")


if __name__ == "__main__":
    main() 