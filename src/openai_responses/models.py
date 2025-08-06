"""
Pydantic models for OpenAI Responses API requests and responses.
"""

from typing import Dict, Any, Optional, Union, List
from pydantic import BaseModel, Field, validator


class ToolFunction(BaseModel):
    """Model for function tool definition."""
    
    name: str = Field(..., description="Name of the function")
    description: Optional[str] = Field(None, description="Description of the function")
    parameters: Dict[str, Any] = Field(..., description="Function parameters schema")


class Tool(BaseModel):
    """Model for tool definition."""
    
    type: str = Field(..., description="Type of tool (function, code_interpreter, file_search, web_search_preview, etc.)")
    function: Optional[ToolFunction] = Field(None, description="Function definition for function tools")
    
    @validator('type')
    def validate_type(cls, v):
        """Validate tool type."""
        valid_types = [
            'function',  # Custom function tools
            'code_interpreter',  # OpenAI hosted tools
            'file_search',
            'web_search_preview',
            'web_search_preview_2025_03_11',
            'image_generation',
            'mcp',
            'computer_use_preview'
        ]
        if v not in valid_types:
            raise ValueError(f"Invalid tool type. Must be one of: {valid_types}")
        return v


class ResponseFormat(BaseModel):
    """Model for response format configuration."""
    
    type: str = Field(..., description="Type of response format (e.g., 'email', 'letter', 'message')")
    style: Optional[str] = Field(None, description="Style of the response (e.g., 'professional', 'casual', 'formal')")
    tone: Optional[str] = Field(None, description="Tone of the response (e.g., 'friendly', 'polite', 'assertive')")
    length: Optional[str] = Field(None, description="Desired length of response (e.g., 'short', 'medium', 'long')")
    language: Optional[str] = Field("en", description="Language code for the response")
    
    # Additional custom fields
    custom_fields: Optional[Dict[str, Any]] = Field(None, description="Additional custom format fields")
    
    @validator('type')
    def validate_type(cls, v):
        """Validate response type."""
        valid_types = ['email', 'letter', 'message', 'response', 'reply', 'note']
        if v.lower() not in valid_types:
            raise ValueError(f"Invalid response type. Must be one of: {valid_types}")
        return v.lower()
    
    @validator('style')
    def validate_style(cls, v):
        """Validate response style."""
        if v is not None:
            valid_styles = ['professional', 'casual', 'formal', 'friendly', 'business']
            if v.lower() not in valid_styles:
                raise ValueError(f"Invalid style. Must be one of: {valid_styles}")
            return v.lower()
        return v
    
    @validator('tone')
    def validate_tone(cls, v):
        """Validate response tone."""
        if v is not None:
            valid_tones = ['friendly', 'polite', 'assertive', 'neutral', 'enthusiastic', 'sympathetic', 'professional']
            if v.lower() not in valid_tones:
                raise ValueError(f"Invalid tone. Must be one of: {valid_tones}")
            return v.lower()
        return v


class ResponseRequest(BaseModel):
    """Model for OpenAI Responses API request."""
    
    model: str = Field(default="gpt-4o", description="OpenAI model to use")
    prompt: str = Field(..., description="The prompt to generate a response for")
    response_format: ResponseFormat = Field(..., description="Format configuration for the response")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0, description="Sampling temperature")
    max_tokens: Optional[int] = Field(None, gt=0, description="Maximum number of tokens to generate")
    top_p: Optional[float] = Field(1.0, ge=0.0, le=1.0, description="Nucleus sampling parameter")
    frequency_penalty: Optional[float] = Field(0.0, ge=-2.0, le=2.0, description="Frequency penalty")
    presence_penalty: Optional[float] = Field(0.0, ge=-2.0, le=2.0, description="Presence penalty")
    seed: Optional[int] = Field(None, description="Random seed for reproducible results")
    tools: Optional[List[Tool]] = Field(None, description="List of tools available to the model")
    tool_choice: Optional[Union[str, Dict[str, Any]]] = Field(None, description="Tool choice configuration")
    
    @validator('model')
    def validate_model(cls, v):
        """Validate OpenAI model."""
        valid_models = ['gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo', 'gpt-3.5-turbo']
        if v not in valid_models:
            raise ValueError(f"Invalid model. Must be one of: {valid_models}")
        return v


class ToolCall(BaseModel):
    """Model for tool call in response."""
    
    id: str = Field(..., description="Tool call ID")
    type: str = Field(..., description="Type of tool call")
    function: Optional[Dict[str, Any]] = Field(None, description="Function call details")
    hosted_tool: Optional[Dict[str, Any]] = Field(None, description="Hosted tool call details")


class ResponseResponse(BaseModel):
    """Model for OpenAI Responses API response."""
    
    id: str = Field(..., description="Unique identifier for the response")
    object: Optional[str] = Field(None, description="Object type")
    created_at: Optional[int] = Field(None, description="Unix timestamp of creation")
    status: Optional[str] = Field(None, description="Response status")
    model: Optional[str] = Field(None, description="Model used for generation")
    output: Optional[list] = Field(None, description="Generated output")
    usage: Optional[Dict[str, Any]] = Field(None, description="Token usage information")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Response metadata")
    text: Optional[Union[str, Dict[str, Any]]] = Field(None, description="Generated text content")
    
    @property
    def content(self) -> str:
        """Get the content of the response."""
        # For Responses API with tools, the content is in output[1]['content'][0]['text']
        # (first output is tool call, second is message)
        if self.output and len(self.output) > 1:
            # Look for message type output
            for output_item in self.output:
                if output_item.get('type') == 'message' and 'content' in output_item:
                    content_list = output_item['content']
                    if content_list and len(content_list) > 0:
                        content_item = content_list[0]
                        if 'text' in content_item:
                            return content_item['text']
        
        # For Responses API without tools, the content is in output[0]['content'][0]['text']
        if self.output and len(self.output) > 0:
            output_item = self.output[0]
            if 'content' in output_item and len(output_item['content']) > 0:
                content_item = output_item['content'][0]
                if 'text' in content_item:
                    return content_item['text']
        
        # Fallback to text field if available
        if hasattr(self, 'text') and self.text:
            if isinstance(self.text, str):
                return self.text
            elif isinstance(self.text, dict) and 'content' in self.text:
                return self.text['content']
        
        # Fallback to choices if available
        if hasattr(self, 'choices') and self.choices and len(self.choices) > 0:
            return self.choices[0].get('message', {}).get('content', '')
        
        return ''
    
    @property
    def finish_reason(self) -> Optional[str]:
        """Get the finish reason of the response."""
        if self.output and len(self.output) > 0:
            return self.output[0].get('finish_reason')
        if hasattr(self, 'choices') and self.choices and len(self.choices) > 0:
            return self.choices[0].get('finish_reason')
        return None
    
    @property
    def prompt_tokens(self) -> int:
        """Get the number of prompt tokens used."""
        if self.usage:
            return self.usage.get('input_tokens', 0)
        return 0
    
    @property
    def completion_tokens(self) -> int:
        """Get the number of completion tokens used."""
        if self.usage:
            return self.usage.get('output_tokens', 0)
        return 0
    
    @property
    def total_tokens(self) -> int:
        """Get the total number of tokens used."""
        if self.usage:
            return self.usage.get('total_tokens', 0)
        return 0 

    @property
    def tool_calls(self) -> Optional[List[ToolCall]]:
        """Get tool calls from the response."""
        if not self.output:
            return None
        
        tool_calls = []
        for output_item in self.output:
            if output_item.get('type') in ['web_search_call', 'function_call']:
                # Create a ToolCall object from the output item
                tool_call = ToolCall(
                    id=output_item.get('id', ''),
                    type=output_item.get('type', ''),
                    function=output_item.get('action', {}),
                    hosted_tool=output_item.get('action', {})
                )
                tool_calls.append(tool_call)
        
        return tool_calls if tool_calls else None 