"""
Custom exceptions for the OpenAI Responses API interface.
"""

from typing import Optional, Dict, Any


class OpenAIResponsesError(Exception):
    """Base exception for all OpenAI Responses API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}


class APIError(OpenAIResponsesError):
    """Exception raised for API-related errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code, response_data)


class ValidationError(OpenAIResponsesError):
    """Exception raised for validation errors."""
    
    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(message, None, None)
        self.field = field


class AuthenticationError(APIError):
    """Exception raised for authentication errors."""
    
    def __init__(self, message: str = "Authentication failed. Please check your API key."):
        super().__init__(message, 401)


class RateLimitError(APIError):
    """Exception raised for rate limit errors."""
    
    def __init__(self, message: str = "Rate limit exceeded. Please try again later."):
        super().__init__(message, 429)


class QuotaExceededError(APIError):
    """Exception raised for quota exceeded errors."""
    
    def __init__(self, message: str = "Quota exceeded. Please check your OpenAI account."):
        super().__init__(message, 402) 