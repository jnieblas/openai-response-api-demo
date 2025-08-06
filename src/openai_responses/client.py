"""
Main client for OpenAI Responses API.
"""

import os
import time
from typing import Dict, Any, Optional, Union, List
import requests
from dotenv import load_dotenv
import json

from .models import ResponseFormat, ResponseResponse, Tool, ToolCall
from .exceptions import (
    OpenAIResponsesError,
    APIError,
    ValidationError,
    AuthenticationError,
    RateLimitError,
    QuotaExceededError,
)


class OpenAIResponsesAPI:
    """
    Client for OpenAI Responses API.
    
    Provides a clean interface for generating structured responses using OpenAI's Responses API.
    """
    
    BASE_URL = "https://api.openai.com/v1"
    RESPONSES_ENDPOINT = f"{BASE_URL}/responses"
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
    ):
        """
        Initialize the OpenAI Responses API client.
        
        Args:
            api_key: OpenAI API key. If not provided, will try to load from environment.
            base_url: Base URL for the API. Defaults to OpenAI's production URL.
            timeout: Request timeout in seconds.
            max_retries: Maximum number of retries for failed requests.
        """
        # Load environment variables
        load_dotenv()
        
        # Set API key
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise AuthenticationError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        # Set base URL
        self.base_url = base_url or self.BASE_URL
        self.responses_endpoint = f"{self.base_url}/responses"
        
        # Set request parameters
        self.timeout = timeout
        self.max_retries = max_retries
        
        # Set up session
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "openai-responses-api/0.1.0",
        })
    
    def generate_response(
        self,
        prompt: str,
        response_format: Union[ResponseFormat, Dict[str, Any]],
        model: str = "gpt-4o",
        temperature: Optional[float] = 0.7,
        top_p: Optional[float] = 1.0,
        tools: Optional[List[Union[Tool, Dict[str, Any]]]] = None,
        tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
    ) -> ResponseResponse:
        """
        Generate a response using the OpenAI Responses API.
        
        Args:
            prompt: The prompt to generate a response for.
            response_format: Format configuration for the response.
            model: OpenAI model to use.
            temperature: Sampling temperature (0.0 to 2.0).
            top_p: Nucleus sampling parameter (0.0 to 1.0).
            tools: List of tools available to the model (function tools or hosted tools).
            tool_choice: Tool choice configuration ('auto', 'none', or specific tool).
            
        Returns:
            ResponseResponse object containing the generated response.
            
        Raises:
            ValidationError: If request parameters are invalid.
            APIError: If the API request fails.
            RateLimitError: If rate limit is exceeded.
            QuotaExceededError: If quota is exceeded.
        """
        try:
            # Convert dict to ResponseFormat if needed
            if isinstance(response_format, dict):
                response_format = ResponseFormat(**response_format)
            
            # Convert dict tools to Tool objects if needed
            if tools:
                tools = [
                    Tool(**tool) if isinstance(tool, dict) else tool
                    for tool in tools
                ]
            
            # Create request data with correct API structure
            request_data = {
                "model": model,
                "input": prompt,
                "text": {
                    "format": {
                        "type": "text"
                    }
                },
                "temperature": temperature,
                "top_p": top_p,
            }
            
            # Add tools if provided
            if tools:
                request_data["tools"] = [tool.model_dump(exclude_none=True) for tool in tools]
            
            # Add tool_choice if provided
            if tool_choice:
                request_data["tool_choice"] = tool_choice
            
            # Remove None values
            request_data = {k: v for k, v in request_data.items() if v is not None}
            
            # Make API request
            response = self._make_request(request_data)
            
            # Parse and return response
            return ResponseResponse(**response)
            
        except ValidationError:
            raise
        except Exception as e:
            if isinstance(e, OpenAIResponsesError):
                raise
            raise APIError(f"Unexpected error: {str(e)}")
    
    def create_function_tool(
        self,
        name: str,
        description: str,
        parameters: Dict[str, Any]
    ) -> Tool:
        """
        Create a function tool for use with the API.
        
        Args:
            name: Name of the function.
            description: Description of what the function does.
            parameters: JSON schema for the function parameters.
            
        Returns:
            Tool object representing the function tool.
        """
        from .models import ToolFunction
        
        function = ToolFunction(
            name=name,
            description=description,
            parameters=parameters
        )
        
        return Tool(type="function", function=function)
    
    def create_hosted_tool(self, hosted_tool_id: str) -> Tool:
        """
        Create a hosted tool reference for use with the API.
        
        Args:
            hosted_tool_id: ID of the hosted tool (e.g., 'web_search_preview', 'file_search').
            
        Returns:
            Tool object representing the hosted tool.
        """
        return Tool(type=hosted_tool_id)
    
    def _make_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a request to the OpenAI Responses API with retry logic.
        
        Args:
            data: Request data to send.
            
        Returns:
            API response data.
            
        Raises:
            APIError: If the request fails after all retries.
        """
        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.post(
                    self.responses_endpoint,
                    json=data,
                    timeout=self.timeout,
                )
                
                # Handle different response status codes
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    raise AuthenticationError("Invalid API key or authentication failed.")
                elif response.status_code == 429:
                    if attempt < self.max_retries:
                        retry_after = int(response.headers.get("Retry-After", 60))
                        time.sleep(retry_after)
                        continue
                    raise RateLimitError("Rate limit exceeded.")
                elif response.status_code == 402:
                    raise QuotaExceededError("Quota exceeded.")
                else:
                    error_data = response.json() if response.content else {}
                    error_message = error_data.get("error", {}).get("message", f"HTTP {response.status_code}")
                    raise APIError(error_message, response.status_code, error_data)
                    
            except requests.exceptions.Timeout:
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise APIError("Request timeout")
            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)
                    continue
                raise APIError(f"Request failed: {str(e)}")
        
        raise APIError("Request failed after all retries")
    
    def create_email_response(
        self,
        prompt: str,
        style: str = "professional",
        tone: str = "polite",
        length: Optional[str] = None,
        tools: Optional[List[Union[Tool, Dict[str, Any]]]] = None,
        tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
        **kwargs
    ) -> ResponseResponse:
        """
        Generate an email response.
        
        Args:
            prompt: The prompt describing what email to generate.
            style: Email style (professional, casual, formal, friendly, business).
            tone: Email tone (friendly, polite, assertive, neutral, enthusiastic, sympathetic).
            length: Desired length (short, medium, long).
            tools: List of tools available to the model.
            tool_choice: Tool choice configuration.
            **kwargs: Additional parameters for generate_response.
            
        Returns:
            ResponseResponse object containing the generated email.
        """
        response_format = ResponseFormat(
            type="email",
            style=style,
            tone=tone,
            length=length,
        )
        
        return self.generate_response(
            prompt, 
            response_format, 
            tools=tools,
            tool_choice=tool_choice,
            **kwargs
        )
    
    def create_letter_response(
        self,
        prompt: str,
        style: str = "formal",
        tone: str = "polite",
        length: Optional[str] = None,
        tools: Optional[List[Union[Tool, Dict[str, Any]]]] = None,
        tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
        **kwargs
    ) -> ResponseResponse:
        """
        Generate a letter response.
        
        Args:
            prompt: The prompt describing what letter to generate.
            style: Letter style (professional, casual, formal, friendly, business).
            tone: Letter tone (friendly, polite, assertive, neutral, enthusiastic, sympathetic).
            length: Desired length (short, medium, long).
            tools: List of tools available to the model.
            tool_choice: Tool choice configuration.
            **kwargs: Additional parameters for generate_response.
            
        Returns:
            ResponseResponse object containing the generated letter.
        """
        response_format = ResponseFormat(
            type="letter",
            style=style,
            tone=tone,
            length=length,
        )
        
        return self.generate_response(
            prompt, 
            response_format, 
            tools=tools,
            tool_choice=tool_choice,
            **kwargs
        )
    
    def create_message_response(
        self,
        prompt: str,
        style: str = "casual",
        tone: str = "friendly",
        length: Optional[str] = None,
        tools: Optional[List[Union[Tool, Dict[str, Any]]]] = None,
        tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
        **kwargs
    ) -> ResponseResponse:
        """
        Generate a message response.
        
        Args:
            prompt: The prompt describing what message to generate.
            style: Message style (professional, casual, formal, friendly, business).
            tone: Message tone (friendly, polite, assertive, neutral, enthusiastic, sympathetic).
            length: Desired length (short, medium, long).
            tools: List of tools available to the model.
            tool_choice: Tool choice configuration.
            **kwargs: Additional parameters for generate_response.
            
        Returns:
            ResponseResponse object containing the generated message.
        """
        response_format = ResponseFormat(
            type="message",
            style=style,
            tone=tone,
            length=length,
        )
        
        return self.generate_response(
            prompt, 
            response_format, 
            tools=tools,
            tool_choice=tool_choice,
            **kwargs
        )
    
    def close(self):
        """Close the session and clean up resources."""
        if hasattr(self, 'session'):
            self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close() 