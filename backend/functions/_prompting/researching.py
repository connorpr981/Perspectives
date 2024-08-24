from typing import Any, Dict, List
from pydantic import BaseModel, Field
from _llm.models.message_models import Messages
from _llm.llm_processing import get_response
import traceback

### RESPONSE MODELS ###
class TagContext(BaseModel):
    """Context about the tag for the reader of the turn"""
    about: str = Field(..., description="A concise and unbiased description of the tag")
    relevance: str = Field(..., description="A concise description of the relevance of the tag to the turn")

### PROMPTS ###
TAG_CONTEXT_SYSTEM_PROMPT = """You are an expert in analyzing and contextualizing information. Your task is to provide context for a specific tag within a turn of a transcript.

Given a tag and the content of a turn, you need to:
1. Provide a concise and unbiased description of the tag.
2. Explain the relevance of the tag to the specific turn.

Keep your responses brief and to the point."""

TAG_CONTEXT_USER_PROMPT = """Tag: {tag}

Turn content: {turn_content}

Please provide:
1. A concise and unbiased description of the tag.
2. A concise description of the relevance of the tag to this specific turn."""

### FUNCTIONS ###
def generate_tag_context(tag: str, turn_content: str) -> TagContext:
    messages = Messages()
    messages.add_system_message(TAG_CONTEXT_SYSTEM_PROMPT)
    messages.add_user_message(TAG_CONTEXT_USER_PROMPT.format(tag=tag, turn_content=turn_content))

    try:
        tag_context, _ = get_response(
            provider="perplexity",
            messages=messages,
            response_model=TagContext
        )
        return tag_context
    except Exception as e:
        error_message = f"Error in generate_tag_context: {str(e)}\n{traceback.format_exc()}"
        print(error_message)
        raise