from typing import Any, Dict, List
from pydantic import BaseModel, Field
from _llm.models.message_models import Messages
from _llm.llm_processing import get_response
import traceback

### RESPONSE MODELS ###

class Section(BaseModel):
    """
    Represents a section of the interview transcript.
    
    Attributes:
        title (str): Concise phrase capturing the section's main theme.
        subtitle (str): Brief elaboration on the title.
        description (str): Summary of the section's content.
        start_turn (int): Index of the first turn in this section.
        end_turn (int): Index of the last turn in this section.
    """
    title: str = Field(..., description="Concise (3-7 words) phrase capturing the section's main theme")
    subtitle: str = Field(..., description="A brief (10-15 words) elaboration on the title")
    description: str = Field(..., description="A summary (2-3 sentences) of the section's content")
    start_turn: int = Field(..., description="Index of the first turn in this section (must be a host turn)")
    end_turn: int = Field(..., description="Index of the last turn in this section (must be a guest turn at least 5 turns after the start turn)")

    @property
    def length(self) -> int:
        return self.end_turn - self.start_turn + 1

    def __str__(self) -> str:
        return f"## {self.title}\n### {self.subtitle}\n\n{self.description}\n\nTurns: {self.start_turn} - {self.end_turn} (Length: {self.length})"

class StructuredTranscript(BaseModel):
    """
    Represents the entire structured transcript divided into sections of 6-12 turns.
    """
    sections: List[Section] = Field(..., description="List of sections representing the structured transcript")

    def __str__(self) -> str:
        return "\n".join(str(section) for section in self.sections)

### PROMPTS ###

SECTIONING_SYSTEM_PROMPT = """You are an expert in content analysis and thematic structuring. Your task is to divide an interview transcript into meaningful sections.

Guidelines:
1. Divide the transcript into sections based on primary themes and content.
2. Each section must begin with a host turn and end with a guest turn.
3. Sections should be 6-12 turns long.
4. For each section, provide:
   - A concise (3-7 words) title
   - A brief (10-15 words) subtitle
   - A summary (2-3 sentences) of the content
   - The start turn index (must be a host turn)
   - The end turn index (must be a guest turn)
5. Focus on the logical progression of the conversation and core ideas presented.
6. The first section should start with turn 0, and the last section should end with the last turn in the transcript.
"""

SECTIONING_USER_PROMPT = """Analyze the following interview transcript and divide it into sections according to the guidelines provided. Structure your response using the StructuredTranscript model.

Each turn in the transcript is formatted as:
[Turn X] Role (Speaker): Action
Text: Full text of the turn

Use both the action summary and the full text for sectioning. Provide the start and end turn indices for each section.

Transcript:

{formatted_transcript}
"""

### FUNCTIONS ###

def format_transcript_for_sectioning(transcript_data: Dict[str, Any]) -> str:
    formatted_turns = []
    for turn in transcript_data['turns']:
        full_text = " ".join([sentence['clean_text'] for sentence in turn['sentences']])
        formatted_turn = f"[Turn {turn['index']}] {turn['role']} ({turn['speaker']}): {turn['action']}\nText: {full_text}"
        formatted_turns.append(formatted_turn)
    return "\n\n".join(formatted_turns)

def get_sections(transcript_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    try:
        formatted_transcript = format_transcript_for_sectioning(transcript_data)
        
        sectioning_messages = Messages()
        sectioning_messages.add_system_message(SECTIONING_SYSTEM_PROMPT)
        sectioning_messages.add_user_message(SECTIONING_USER_PROMPT.format(formatted_transcript=formatted_transcript))
        
        response, _ = get_response(
            provider="anthropic",
            messages=sectioning_messages,
            response_model=StructuredTranscript
        )

        return response.model_dump()['sections']
    except Exception as e:
        print(f"Error in get_sections:")
        print(traceback.format_exc())
        raise