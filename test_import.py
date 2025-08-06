#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple test script to verify the OpenAI Responses API package can be imported.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported successfully."""
    try:
        # Test main package import
        from openai_responses import OpenAIResponsesAPI, ResponseFormat
        print("✅ Main package imports successful")
        
        # Test individual module imports
        from openai_responses.client import OpenAIResponsesAPI as Client
        print("✅ Client module import successful")
        
        from openai_responses.models import ResponseFormat as ModelFormat, ResponseResponse
        print("✅ Models module import successful")
        
        from openai_responses.exceptions import OpenAIResponsesError, APIError, ValidationError
        print("✅ Exceptions module import successful")
        
        # Test creating instances using main package imports
        api = OpenAIResponsesAPI(api_key="test-key")
        print("✅ API client instantiation successful")
        
        format_obj = ResponseFormat(type="email", style="professional")
        print("✅ ResponseFormat instantiation successful")
        
        print("\n🎉 All imports and instantiations successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing OpenAI Responses API package imports...")
    success = test_imports()
    sys.exit(0 if success else 1) 