#!/usr/bin/env python3
"""
Tool Calling Example for OpenAI Responses API

This example demonstrates how to use function tools and hosted tools
with the OpenAI Responses API.
"""

import os
import sys
import json
from typing import Dict, Any

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from openai_responses import OpenAIResponsesAPI, Tool, ToolFunction


def create_weather_function_tool() -> Tool:
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


def create_calculator_function_tool() -> Tool:
    """Create a calculator function tool."""
    
    calculator_parameters = {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["add", "subtract", "multiply", "divide"],
                "description": "The mathematical operation to perform"
            },
            "a": {
                "type": "number",
                "description": "First number"
            },
            "b": {
                "type": "number", 
                "description": "Second number"
            }
        },
        "required": ["operation", "a", "b"]
    }
    
    return Tool(
        type="function",
        function=ToolFunction(
            name="calculate",
            description="Perform basic mathematical operations",
            parameters=calculator_parameters
        )
    )


def create_hosted_tool_example() -> Tool:
    """Create a hosted tool reference."""
    
    # This would be a real hosted tool ID from your OpenAI account
    # For demonstration, we'll use a placeholder
    hosted_tool_id = "web_search_preview"  # Use actual OpenAI hosted tool
    
    return Tool(type=hosted_tool_id)


def demo_function_tools():
    """Demonstrate function tools."""
    print("=" * 60)
    print("Function Tools Demo")
    print("=" * 60)
    
    try:
        # Initialize API client
        api = OpenAIResponsesAPI()
        
        # Create function tools
        weather_tool = create_weather_function_tool()
        calculator_tool = create_calculator_function_tool()
        
        # Example 1: Weather tool
        print("\n1. Weather Tool Example")
        print("-" * 30)
        
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
        
        print(f"Response: {response.content}")
        
        # Check for tool calls
        if response.tool_calls:
            print(f"\nTool calls made: {len(response.tool_calls)}")
            for tool_call in response.tool_calls:
                print(f"Tool call ID: {tool_call.id}")
                print(f"Tool call type: {tool_call.type}")
                if tool_call.function:
                    print(f"Function: {tool_call.function}")
        
        # Example 2: Calculator tool
        print("\n2. Calculator Tool Example")
        print("-" * 30)
        
        response = api.generate_response(
            prompt="Calculate 15 * 23 and explain the result in a friendly way.",
            response_format={
                "type": "message",
                "style": "casual",
                "tone": "enthusiastic"
            },
            tools=[calculator_tool],
            tool_choice="auto"
        )
        
        print(f"Response: {response.content}")
        
        # Example 3: Multiple tools
        print("\n3. Multiple Tools Example")
        print("-" * 30)
        
        response = api.generate_response(
            prompt="What's the weather in London and what's 100 divided by 5?",
            response_format={
                "type": "message",
                "style": "professional",
                "tone": "neutral"
            },
            tools=[weather_tool, calculator_tool],
            tool_choice="auto"
        )
        
        print(f"Response: {response.content}")
        
    except Exception as e:
        print(f"Error: {e}")


def demo_hosted_tools():
    """Demonstrate hosted tools."""
    print("\n" + "=" * 60)
    print("Hosted Tools Demo")
    print("=" * 60)
    
    try:
        # Initialize API client
        api = OpenAIResponsesAPI()
        
        # Create hosted tool reference
        web_search_tool = create_hosted_tool_example()
        
        print("\nUsing OpenAI's web_search_preview hosted tool.")
        print("This tool allows the model to search the web for current information.")
        
        # Example with hosted tool
        response = api.generate_response(
            prompt="Search for the latest news about AI developments and summarize the key points.",
            response_format={
                "type": "message",
                "style": "professional",
                "tone": "informative"
            },
            tools=[web_search_tool],
            tool_choice="auto"
        )
        
        print(f"\nResponse: {response.content}")
        
        if response.tool_calls:
            print(f"\nHosted tool calls made: {len(response.tool_calls)}")
            for tool_call in response.tool_calls:
                print(f"Tool call ID: {tool_call.id}")
                print(f"Tool call type: {tool_call.type}")
                if tool_call.hosted_tool:
                    print(f"Hosted tool: {tool_call.hosted_tool}")
        
    except Exception as e:
        print(f"Error: {e}")


def demo_tool_choice_options():
    """Demonstrate different tool choice options."""
    print("\n" + "=" * 60)
    print("Tool Choice Options Demo")
    print("=" * 60)
    
    try:
        # Initialize API client
        api = OpenAIResponsesAPI()
        
        # Create function tool
        weather_tool = create_weather_function_tool()
        
        # Example 1: Auto tool choice (let model decide)
        print("\n1. Auto Tool Choice")
        print("-" * 20)
        
        response = api.generate_response(
            prompt="What's the weather like in Tokyo?",
            response_format={"type": "message", "style": "casual"},
            tools=[weather_tool],
            tool_choice="auto"
        )
        
        print(f"Response: {response.content}")
        
        # Example 2: None tool choice (no tools used)
        print("\n2. None Tool Choice")
        print("-" * 20)
        
        response = api.generate_response(
            prompt="What's the weather like in Tokyo?",
            response_format={"type": "message", "style": "casual"},
            tools=[weather_tool],
            tool_choice="none"
        )
        
        print(f"Response: {response.content}")
        
        # Example 3: Specific tool choice
        print("\n3. Specific Tool Choice")
        print("-" * 20)
        
        response = api.generate_response(
            prompt="What's the weather like in Tokyo?",
            response_format={"type": "message", "style": "casual"},
            tools=[weather_tool],
            tool_choice={"type": "function", "function": {"name": "get_weather"}}
        )
        
        print(f"Response: {response.content}")
        
    except Exception as e:
        print(f"Error: {e}")


def demo_integration_with_response_methods():
    """Demonstrate tool calling with response-specific methods."""
    print("\n" + "=" * 60)
    print("Integration with Response Methods Demo")
    print("=" * 60)
    
    try:
        # Initialize API client
        api = OpenAIResponsesAPI()
        
        # Create function tool
        calculator_tool = create_calculator_function_tool()
        
        # Example 1: Email with tool
        print("\n1. Email Response with Tool")
        print("-" * 30)
        
        response = api.create_email_response(
            prompt="Calculate the total cost for 5 items at $12.50 each and include it in a professional email to the client.",
            style="professional",
            tone="polite",
            tools=[calculator_tool],
            tool_choice="auto"
        )
        
        print(f"Email Response: {response.content}")
        
        # Example 2: Letter with tool
        print("\n2. Letter Response with Tool")
        print("-" * 30)
        
        response = api.create_letter_response(
            prompt="Write a formal letter explaining the weather calculation for our outdoor event planning.",
            style="formal",
            tone="professional",
            tools=[create_weather_function_tool()],
            tool_choice="auto"
        )
        
        print(f"Letter Response: {response.content}")
        
        # Example 3: Message with tool
        print("\n3. Message Response with Tool")
        print("-" * 30)
        
        response = api.create_message_response(
            prompt="Send a friendly message to a friend with a quick calculation.",
            style="casual",
            tone="friendly",
            tools=[calculator_tool],
            tool_choice="auto"
        )
        
        print(f"Message Response: {response.content}")
        
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Run all tool calling demos."""
    print("🚀 OpenAI Responses API - Tool Calling Examples")
    print("This demo showcases function tools and hosted tools")
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  Warning: OPENAI_API_KEY environment variable is not set.")
        print("   Set it with: export OPENAI_API_KEY='your-api-key-here'")
        print("   Some examples may fail without a valid API key.")
    
    # Run demos
    demo_function_tools()
    demo_hosted_tools()
    demo_tool_choice_options()
    demo_integration_with_response_methods()
    
    print("\n" + "=" * 60)
    print("Demo Complete!")
    print("=" * 60)
    print("\nKey Features Demonstrated:")
    print("✅ Function tools with JSON schema parameters")
    print("✅ Hosted tools with tool IDs")
    print("✅ Different tool choice options (auto, none, specific)")
    print("✅ Integration with response-specific methods")
    print("✅ Tool call detection and handling")


if __name__ == "__main__":
    main() 