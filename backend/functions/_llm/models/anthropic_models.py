from typing import List, Literal, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime
import json
import textwrap
from .base_models import AIResponse

class AnthropicTextContent(BaseModel):
    """Represents text content in Anthropic responses."""
    type: Literal["text"]
    text: str

    def __str__(self):
        return f"Text: {self.text}"

class AnthropicToolUseContent(BaseModel):
    """Represents tool use content in Anthropic responses."""
    type: Literal["tool_use"]
    id: str
    name: str
    input: Dict[str, Any]

    def __str__(self):
        return f"""Tool Use:
  ID: {self.id}
  Name: {self.name}
  Input:
{textwrap.indent(json.dumps(self.input, indent=2), '    ')}"""

AnthropicContent = Union[AnthropicTextContent, AnthropicToolUseContent]

class AnthropicUsage(BaseModel):
    """Represents token usage in Anthropic responses."""
    input_tokens: int
    output_tokens: int

class AnthropicResponse(AIResponse):
    """Represents a completion response from the Anthropic API."""
    content: List[AnthropicContent] = Field(..., description="List of content items in the response")
    role: Literal["assistant"] = Field(..., description="Role of the message sender")
    stop_reason: Optional[str] = Field(None, description="Reason for stopping the generation")
    stop_sequence: Optional[str] = Field(None, description="Sequence that caused the generation to stop")
    type: Optional[Literal["message"]] = Field(None, description="Type of the response")

    @classmethod
    def from_completion(cls, completion: Any, provider: str, model: str) -> 'AnthropicResponse':
        completion_data = completion.model_dump(exclude={'usage'})
        
        for field in ['provider', 'model', 'created_at', 'total_tokens', 'prompt_tokens', 'completion_tokens']:
            completion_data.pop(field, None)
        
        return cls(
            provider=provider,
            model=model,
            created_at=datetime.utcnow(),
            total_tokens=completion.usage.input_tokens + completion.usage.output_tokens,
            prompt_tokens=completion.usage.input_tokens,
            completion_tokens=completion.usage.output_tokens,
            **completion_data
        )

    def get_message_content(self) -> str:
        content_parts = []
        for item in self.content:
            if isinstance(item, AnthropicTextContent):
                content_parts.append(item.text)
            elif isinstance(item, AnthropicToolUseContent):
                tool_use = f"[Tool Use: {item.name}]\nInput: {json.dumps(item.input, indent=2)}"
                content_parts.append(tool_use)
        return "\n\n".join(content_parts)

    def __str__(self):
        content_str = "\n".join(f"  {i+1}. {textwrap.indent(str(content), '     ').strip()}" 
                                for i, content in enumerate(self.content))
        return f"""{super().__str__()}
  Role: {self.role}
  Stop reason: {self.stop_reason or 'N/A'}
  Stop sequence: {self.stop_sequence or 'N/A'}
  Type: {self.type or 'N/A'}
  Content items:
{content_str}"""