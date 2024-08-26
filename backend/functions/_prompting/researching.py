import logging
from typing import Any, Dict, List
from pydantic import BaseModel, Field
from _llm.models.message_models import Messages
import traceback
import os
from openai import OpenAI

### PROMPTS ###
TAG_RELEVANCE_SYSTEM_PROMPT = """You are an expert in defining terms within specific contexts. Your task is to provide a concise, one-sentence definition for a given tag, considering the context of a single turn in a transcript.

Focus solely on defining the tag in a way that helps the reader better understand what the speaker is saying in the provided turn. Do not explain the relevance or make assumptions about other parts of the conversation."""

TAG_RELEVANCE_USER_PROMPT = """Provide a one-sentence definition for the following tag, considering the context of the given turn:

Turn: {turn_content}

Tag: {tag}

Definition (one sentence):"""

### FUNCTIONS ###
def generate_tag_relevance(tag: str, turn_content: str) -> str:
    """
    Generate relevance for a specific tag within a single turn of the transcript.

    Args:
        tag (str): The tag to analyze.
        turn_content (str): The content of the specific turn to analyze.

    Returns:
        str: A string containing the tag's relevance to the turn, including a brief description of the tag.

    Raises:
        Exception: If there's an error in generating the tag relevance.

    Note:
        This function makes only one tool/function call to the LLM.
    """
    logging.info(f"Generating tag relevance for tag: {tag}")
    
    messages = Messages()
    messages.add_system_message(TAG_RELEVANCE_SYSTEM_PROMPT)
    messages.add_user_message(TAG_RELEVANCE_USER_PROMPT.format(tag=tag, turn_content=turn_content))
    
    client = OpenAI(api_key=os.getenv("PERPLEXITY_API_KEY"), base_url="https://api.perplexity.ai")

    try:
        response = client.chat.completions.create(
            model="llama-3.1-sonar-huge-128k-online",
            messages=messages.to_api_format(),
        )
        tag_relevance = response.choices[0].message.content
        logging.info(f"Successfully generated tag relevance for tag: {tag}\n{tag_relevance}")
        return tag_relevance
    except Exception as e:
        error_message = f"Error in generate_tag_relevance for tag '{tag}': {str(e)}\n{traceback.format_exc()}"
        logging.error(error_message)
        raise