from __future__ import annotations
from typing import Literal, Optional, Dict, Any, Type
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, UTC
from abc import ABC, abstractmethod
import textwrap
from .message_models import Message

ProviderLiteral = Literal["anthropic", "openai", "cohere"]

class BaseResponseMetadata(BaseModel):
    """Base class for provider-agnostic response metadata."""
    model_config = ConfigDict(populate_by_name=True)

    provider: ProviderLiteral
    model: str
    created_at: datetime
    total_tokens: int
    prompt_tokens: int
    completion_tokens: int

    def __str__(self):
        return f"""Metadata:
  Provider: {self.provider}
  Model: {self.model}
  Created at: {self.created_at.isoformat(sep=' ', timespec='seconds')}
  Tokens:
    Total: {self.total_tokens}
    Prompt: {self.prompt_tokens}
    Completion: {self.completion_tokens}"""

class AIResponse(BaseResponseMetadata, ABC):
    """Abstract base class for AI responses with common functionality."""
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description="Unique identifier for the response")
    response_model_dump: Optional[Dict[str, Any]] = None

    @classmethod
    @abstractmethod
    def from_completion(cls, completion: Any, provider: str, model: str) -> AIResponse:
        """Create an AIResponse instance from a completion object."""
        pass

    @abstractmethod
    def get_message_content(self) -> str:
        """Returns the content of the response."""
        pass

    def to_message(self) -> Message:
        """Converts the response to a Message object."""
        return Message(role="assistant", content=self.get_message_content())

    @classmethod
    def extract_metadata(cls, response: AIResponse) -> BaseResponseMetadata:
        """Extracts provider-agnostic metadata from the response."""
        return BaseResponseMetadata(
            provider=response.provider,
            model=response.model,
            created_at=response.created_at,
            total_tokens=response.total_tokens,
            prompt_tokens=response.prompt_tokens,
            completion_tokens=response.completion_tokens
        )

    def __str__(self):
        return f"""AIResponse:
  ID: {self.id}
{textwrap.indent(super().__str__(), '  ')}
  Content:
{textwrap.indent(self.get_message_content(), '    ')}"""