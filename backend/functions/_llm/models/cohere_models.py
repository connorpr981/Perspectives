from typing import List, Literal, Optional, Any, Dict
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, UTC
import textwrap
from .base_models import AIResponse

class CohereToolCall(BaseModel):
    name: str
    parameters: Dict[str, Any]

class CohereChatMessage(BaseModel):
    role: Literal["USER", "CHATBOT"]
    message: str
    tool_calls: Optional[List[CohereToolCall]] = None

class CohereMetaBilledUnits(BaseModel):
    input_tokens: int
    output_tokens: int

class CohereMeta(BaseModel):
    billed_units: CohereMetaBilledUnits

class CohereResponse(AIResponse):
    """Represents a completion response from the Cohere API."""
    model_config = ConfigDict(populate_by_name=True)

    text: str = Field(..., description="Generated text")
    generation_id: str = Field(..., description="Unique generation ID")
    finish_reason: str = Field(..., description="Reason for finishing the generation")
    tool_calls: Optional[List[CohereToolCall]] = Field(None, description="Tool calls made during generation")
    chat_history: List[CohereChatMessage] = Field(..., description="Chat history")
    meta: CohereMeta = Field(..., description="Metadata about the response")

    @classmethod
    def from_completion(cls, completion: Any, provider: str, model: str) -> 'CohereResponse':
        return cls(
            provider=provider,
            model=model,
            created_at=datetime.now(UTC),
            total_tokens=completion.meta.billed_units.input_tokens + completion.meta.billed_units.output_tokens,
            prompt_tokens=completion.meta.billed_units.input_tokens,
            completion_tokens=completion.meta.billed_units.output_tokens,
            id=completion.generation_id,
            **completion.model_dump()
        )

    def get_message_content(self) -> str:
        return self.text

    def __str__(self):
        tool_calls_str = "\n".join(f"    - {call.name}: {call.parameters}" for call in (self.tool_calls or []))
        chat_history_str = "\n".join(f"    - {msg.role}: {msg.message}" for msg in self.chat_history)
        return f"""{super().__str__()}
  Text: {self.text}
  Generation ID: {self.generation_id}
  Finish reason: {self.finish_reason}
  Tool calls:
{tool_calls_str}
  Chat history:
{chat_history_str}
  Billed units:
    Input tokens: {self.meta.billed_units.input_tokens}
    Output tokens: {self.meta.billed_units.output_tokens}"""