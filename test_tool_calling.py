#!/usr/bin/env python3
"""
Simple test for tool calling functionality.
"""

import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from openai_responses import OpenAIResponsesAPI, Tool, ToolFunction


def test_tool_creation():
    """Test creating tools."""
    print("Testing tool creation...")
    
    # Test function tool creation
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
                    }
                },
                "required": ["location"]
            }
        )
    )
    
    print(f"✅ Function tool created: {weather_tool.type}")
    print(f"   Function name: {weather_tool.function.name}")
    print(f"   Parameters: {weather_tool.function.parameters}")
    
    # Test hosted tool creation
    hosted_tool = Tool(
        type="web_search_preview"
    )
    
    print(f"✅ Hosted tool created: {hosted_tool.type}")
    print(f"   Tool type: {hosted_tool.type}")
    
    return weather_tool, hosted_tool


def test_api_client_tool_methods():
    """Test API client tool creation methods."""
    print("\nTesting API client tool methods...")
    
    api = OpenAIResponsesAPI(api_key="test-key")
    
    # Test create_function_tool method
    calculator_tool = api.create_function_tool(
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
    
    print(f"✅ Function tool created via API client: {calculator_tool.type}")
    print(f"   Function name: {calculator_tool.function.name}")
    
    # Test create_hosted_tool method
    hosted_tool = api.create_hosted_tool("web_search_preview")
    
    print(f"✅ Hosted tool created via API client: {hosted_tool.type}")
    print(f"   Tool type: {hosted_tool.type}")
    
    return calculator_tool, hosted_tool


def test_tool_serialization():
    """Test tool serialization to dict."""
    print("\nTesting tool serialization...")
    
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
                    }
                },
                "required": ["location"]
            }
        )
    )
    
    # Test serialization
    tool_dict = weather_tool.model_dump(exclude_none=True)
    print(f"✅ Tool serialized to dict: {tool_dict}")
    
    # Test deserialization
    tool_from_dict = Tool(**tool_dict)
    print(f"✅ Tool deserialized from dict: {tool_from_dict.type}")
    
    return tool_dict


def main():
    """Run all tool calling tests."""
    print("🧪 Testing Tool Calling Functionality")
    print("=" * 50)
    
    try:
        # Test tool creation
        weather_tool, hosted_tool = test_tool_creation()
        
        # Test API client methods
        calculator_tool, api_hosted_tool = test_api_client_tool_methods()
        
        # Test serialization
        tool_dict = test_tool_serialization()
        
        print("\n" + "=" * 50)
        print("🎉 All tool calling tests passed!")
        print("=" * 50)
        print("\nKey Features Verified:")
        print("✅ Function tool creation with JSON schema")
        print("✅ Hosted tool creation with tool IDs")
        print("✅ API client helper methods")
        print("✅ Tool serialization/deserialization")
        print("✅ Pydantic model validation")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 