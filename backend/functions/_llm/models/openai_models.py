from typing import List, Literal, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import textwrap
from .base_models import AIResponse

class OpenAIFunctionCall(BaseModel):
    """Represents a function call in OpenAI responses."""
    name: str
    arguments: str

    def __str__(self):
        return f"""Function:
  Name: {self.name}
  Arguments:
{textwrap.indent(self.arguments, '    ')}"""

class OpenAIToolCall(BaseModel):
    """Represents a tool call in OpenAI responses."""
    id: str
    type: Literal["function"]
    function: OpenAIFunctionCall

    def __str__(self):
        return f"""Tool Call:
  ID: {self.id}
  Type: {self.type}
{textwrap.indent(str(self.function), '  ')}"""

class OpenAIMessage(BaseModel):
    """Represents a message in OpenAI responses."""
    role: Literal["assistant"]
    content: Optional[str] = None
    tool_calls: Optional[List[OpenAIToolCall]] = None

    def __str__(self):
        result = f"Role: {self.role}\n"
        if self.content:
            result += f"Content:\n{textwrap.indent(self.content, '  ')}\n"
        if self.tool_calls:
            tool_calls_str = "\n".join(str(tool_call) for tool_call in self.tool_calls)
            result += f"Tool Calls:\n{textwrap.indent(tool_calls_str, '  ')}"
        return result

class OpenAIChoice(BaseModel):
    """Represents a choice in OpenAI responses."""
    index: int
    message: OpenAIMessage
    finish_reason: str

    def __str__(self):
        return f"""Choice {self.index}:
{textwrap.indent(str(self.message), '  ')}
  Finish reason: {self.finish_reason}"""

class OpenAIUsage(BaseModel):
    """Represents token usage in OpenAI responses."""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

    def __str__(self):
        return f"""Usage:
  Prompt tokens: {self.prompt_tokens}
  Completion tokens: {self.completion_tokens}
  Total tokens: {self.total_tokens}"""

class OpenAIResponse(AIResponse):
    """Represents a completion response from the OpenAI API."""
    object: Literal["chat.completion"] = Field(..., description="Object type")
    choices: List[OpenAIChoice] = Field(..., description="List of generated choices")

    @classmethod
    def from_completion(cls, completion: Any, provider: str, model: str) -> 'OpenAIResponse':
        completion_data = completion.model_dump(exclude={'usage'})
        
        for field in ['provider', 'model', 'created_at', 'total_tokens', 'prompt_tokens', 'completion_tokens']:
            completion_data.pop(field, None)
        
        return cls(
            provider=provider,
            model=model,
            created_at=datetime.fromtimestamp(completion.created),
            total_tokens=completion.usage.total_tokens,
            prompt_tokens=completion.usage.prompt_tokens,
            completion_tokens=completion.usage.completion_tokens,
            **completion_data
        )

    def get_message_content(self) -> str:
        if not self.choices:
            return ""
        
        message = self.choices[0].message
        content_parts = []
        
        if message.content:
            content_parts.append(message.content)
        
        if message.tool_calls:
            for tool_call in message.tool_calls:
                if tool_call.type == "function":
                    function_call = f"[Function Call: {tool_call.function.name}]\nArguments: {tool_call.function.arguments}"
                    content_parts.append(function_call)
        
        return "\n\n".join(content_parts)

    def __str__(self):
        choices_str = "\n".join(f"  {i+1}. {textwrap.indent(str(choice), '     ').strip()}" 
                                for i, choice in enumerate(self.choices))
        return f"""{super().__str__()}
  Object: {self.object}
  Choices:
{choices_str}"""