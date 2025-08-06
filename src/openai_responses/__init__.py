"""
OpenAI Responses API Python Interface

A clean, type-safe interface for OpenAI's Responses API.
"""

from .client import OpenAIResponsesAPI
from .models import ResponseFormat, ResponseResponse, Tool, ToolFunction, ToolCall
from .exceptions import OpenAIResponsesError, APIError, ValidationError

__version__ = "0.1.0"
__all__ = [
    "OpenAIResponsesAPI",
    "ResponseFormat",
    "ResponseResponse",
    "Tool",
    "ToolFunction", 
    "ToolCall",
    "OpenAIResponsesError",
    "APIError",
    "ValidationError",
] 