#!/usr/bin/env python3
"""
OpenAI Responses API Demo

This script demonstrates how to use the OpenAI Responses API interface
to generate various types of structured responses.
"""

import os
import sys
from typing import Dict, Any

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from openai_responses import OpenAIResponsesAPI, ResponseFormat
from openai_responses.exceptions import OpenAIResponsesError, APIError, AuthenticationError


def print_separator(title: str):
    """Print a formatted separator with title."""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)


def print_response(response, title: str = "Generated Response"):
    """Print a formatted response."""
    print(f"\n{title}:")
    print("-" * 40)
    print(response.content)
    print(f"\nTokens used: {response.total_tokens} (prompt: {response.prompt_tokens}, completion: {response.completion_tokens})")
    print(f"Finish reason: {response.finish_reason}")


def demo_basic_usage():
    """Demonstrate basic usage of the API."""
    print_separator("Basic Usage Example")
    
    try:
        # Initialize the API client
        api = OpenAIResponsesAPI()
        
        # Example 1: Generate a professional email
        print("Generating a professional email response...")
        response = api.create_email_response(
            prompt="Write an email declining a meeting request from a colleague due to a scheduling conflict",
            style="professional",
            tone="polite",
            length="short"
        )
        print_response(response, "Professional Email Response")
        
    except AuthenticationError as e:
        print(f"Authentication error: {e}")
        print("Please set your OPENAI_API_KEY environment variable.")
    except APIError as e:
        print(f"API error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def demo_custom_formats():
    """Demonstrate custom response formats."""
    print_separator("Custom Response Formats")
    
    try:
        api = OpenAIResponsesAPI()
        
        # Example 2: Custom response format
        print("Generating a response with custom format...")
        custom_format = ResponseFormat(
            type="message",
            style="casual",
            tone="enthusiastic",
            length="medium",
            language="en"
        )
        
        response = api.generate_response(
            prompt="Write a thank you message for a birthday gift from a friend",
            response_format=custom_format,
            temperature=0.8
        )
        print_response(response, "Custom Format Response")
        
    except Exception as e:
        print(f"Error: {e}")


def demo_different_response_types():
    """Demonstrate different response types."""
    print_separator("Different Response Types")
    
    try:
        api = OpenAIResponsesAPI()
        
        # Example 3: Letter response
        print("Generating a formal letter...")
        letter_response = api.create_letter_response(
            prompt="Write a formal letter of recommendation for a former employee",
            style="formal",
            tone="professional",
            length="long"
        )
        print_response(letter_response, "Formal Letter")
        
        # Example 4: Message response
        print("\nGenerating a casual message...")
        message_response = api.create_message_response(
            prompt="Write a friendly message to congratulate someone on their promotion",
            style="casual",
            tone="friendly",
            length="short"
        )
        print_response(message_response, "Casual Message")
        
    except Exception as e:
        print(f"Error: {e}")


def demo_advanced_parameters():
    """Demonstrate advanced parameters."""
    print_separator("Advanced Parameters")
    
    try:
        api = OpenAIResponsesAPI()
        
        # Example 5: Using advanced parameters
        print("Generating response with advanced parameters...")
        response = api.generate_response(
            prompt="Write a creative story about a magical forest",
            response_format={
                "type": "message",
                "style": "casual",
                "tone": "enthusiastic",
                "length": "long"
            },
            model="gpt-4o",
            temperature=0.9,  # More creative
            top_p=0.9
        )
        print_response(response, "Advanced Parameters Response")
        
    except Exception as e:
        print(f"Error: {e}")


def demo_error_handling():
    """Demonstrate error handling."""
    print_separator("Error Handling")
    
    try:
        # Example 6: Invalid API key
        print("Testing error handling with invalid API key...")
        api = OpenAIResponsesAPI(api_key="invalid-key")
        response = api.create_email_response("Test prompt")
        
    except AuthenticationError as e:
        print(f"✅ Correctly caught authentication error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    try:
        # Example 7: Invalid response format
        print("\nTesting error handling with invalid response format...")
        api = OpenAIResponsesAPI()
        response = api.generate_response(
            prompt="Test prompt",
            response_format={
                "type": "invalid_type",  # Invalid type
                "style": "invalid_style"  # Invalid style
            }
        )
        
    except Exception as e:
        print(f"✅ Correctly caught validation error: {e}")


def demo_context_manager():
    """Demonstrate context manager usage."""
    print_separator("Context Manager Usage")
    
    try:
        # Example 8: Using context manager
        print("Using context manager for automatic resource cleanup...")
        with OpenAIResponsesAPI() as api:
            response = api.create_email_response(
                prompt="Write a brief email confirming receipt of an important document",
                style="professional",
                tone="neutral",
                length="short"
            )
            print_response(response, "Context Manager Response")
        
        print("✅ Context manager automatically closed the session")
        
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Main function to run all demos."""
    print("🚀 OpenAI Responses API Demo")
    print("This demo showcases the Python interface for OpenAI's Responses API")
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  Warning: OPENAI_API_KEY environment variable is not set.")
        print("   Some examples may fail. Set it with:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        print("\n   Continuing with demo (some examples will show error handling)...")
    
    # Run all demos
    demo_basic_usage()
    demo_custom_formats()
    demo_different_response_types()
    demo_advanced_parameters()
    demo_error_handling()
    demo_context_manager()
    
    print_separator("Demo Complete")
    print("✅ All demos completed!")
    print("\nFor more information, check the README.md file.")
    print("To use this in your own projects, import the OpenAIResponsesAPI class.")


if __name__ == "__main__":
    main() 