from typing import Any, Dict, List
from pydantic import BaseModel, Field
from _llm.models.message_models import Messages
from _llm.llm_processing import get_response
import traceback
import time

### RESPONSE MODELS ###

class Section(BaseModel):
    """
    Represents a section of the interview transcript.
    """
    title: str = Field(..., description="Concise (3-7 words) analytical phrase capturing the section's main theme")
    start_turn: int = Field(..., description="Turn index where this section begins")
    end_turn: int = Field(..., description="Turn index where this section ends")

    def __str__(self) -> str:
        return f"""
## {self.title}

Turns: {self.start_turn} - {self.end_turn}
"""

class StructuredTranscript(BaseModel):
    """
    Represents the entire structured transcript divided into sections.
    """
    sections: List[Section] = Field(..., description="List of sections representing the structured transcript")

    def __str__(self) -> str:
        return "\n".join(str(section) for section in self.sections)

### PROMPTS ###

SECTIONING_SYSTEM_PROMPT = """You are a world-class qualitative researcher with expertise in content analysis and thematic structuring. Your task is to create a meaningful, well-structured representation of a given interview podcast transcript, focusing on the guest's responses to the host's questions.

Key guidelines:
1. Divide the transcript into non-overlapping sections based on primary themes and content.
2. Each section should encompass 4-16 turns to capture a complete thematic unit.
3. Sections should begin with a host turn to maintain context.
4. Keep questions and their corresponding answers together within the same section.
5. Provide concise (3-7 words) analytical titles for each section, capturing the main theme or topic.
6. Focus on how question topics evolve, capturing the logical progression of the conversation.
7. Incorporate introductions and conclusions into the first and last sections respectively, unless exceptionally long.

When identifying distinct topics or themes, consider:
- Shifts in main subjects
- Transitions between broader themes and specific examples

Aim for a balance between thematic integrity and appropriate section length, prioritizing content over structure. The first section should start with turn 0, and the last section should end with the last turn in the transcript.

For reference:
- The host's name is "Dwarkesh Patel". Each section should start with a turn from the host.
"""

SECTIONING_USER_PROMPT = """Analyze the following interview podcast transcript and divide it into meaningful sections according to the guidelines provided. Structure your response using the StructuredTranscript model, which contains a list of Section objects. The goal is to create a structure that allows for a closer examination of the dialogue.

Focus on the primary content and themes of the interview. Ensure that each section provides a clear context for understanding the dialogue within the thematic framework of the conversation.

Transcript:

{formatted_transcript}
"""

### FUNCTIONS ###

def format_transcript_for_sectioning(transcript_data: Dict[str, Any]) -> str:
    """
    Formats the turn data for sectioning, including turn index, role, speaker, and action.
    """
    formatted_turns = []
    
    for turn in transcript_data['turns']:
        formatted_turns.append(f"[Turn {turn['index']}] {turn['role']} ({turn['speaker']}): {turn['action']}")
    
    return "\n\n".join(formatted_turns)

def get_sections(transcript_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Gets the sections of the transcript by sending a prompt to the LLM with the formatted turn data.
    """
    try:
        formatted_transcript = format_transcript_for_sectioning(transcript_data)
        
        sectioning_messages = Messages()
        sectioning_messages.add_system_message(SECTIONING_SYSTEM_PROMPT)
        sectioning_messages.add_user_message(SECTIONING_USER_PROMPT.format(formatted_transcript=formatted_transcript))
        
        response, _ = get_response(
            provider="openai",
            messages=sectioning_messages,
            response_model=StructuredTranscript
        )

        return response.sections
    except Exception as e:
        print(f"Error in get_sections:")
        print(traceback.format_exc())
        raise