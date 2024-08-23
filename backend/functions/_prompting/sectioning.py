from typing import Any, Dict, List
from pydantic import BaseModel, Field
from _llm.models.message_models import Messages
from _llm.llm_processing import get_response
import traceback

### RESPONSE MODELS ###

class Section(BaseModel):
    """
    Represents a section of the interview transcript.
    """
    title: str = Field(..., description="Concise (3-7 words) phrase capturing the section's main theme")
    subtitle: str = Field(..., description="A brief (10-15 words) elaboration on the title")
    description: str = Field(..., description="A summary (2-3 sentences) of the section's content")
    start_turn: int = Field(..., description="Turn index where this section begins (must be a host turn)")
    end_turn: int = Field(..., description="Turn index where this section ends (must be a guest turn)")

    def __str__(self) -> str:
        return f"""
## {self.title}
### {self.subtitle}

{self.description}

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
1. Divide the transcript into broad, non-overlapping sections based on primary themes and content of the dialogue.
2. Each section must begin with a host turn and end with a guest turn.
3. Sections should typically encompass multiple question-answer exchanges to capture complete thematic units.
4. Provide for each section:
   - A concise (3-7 words) title capturing the main theme
   - A brief (10-15 words) subtitle elaborating on the title
   - A summary (2-3 sentences) describing the section's content
5. Focus on how question topics evolve, capturing the logical progression of the conversation.
6. Ignore structural aspects like introductions, conclusions, or pleasantries when creating section titles, subtitles, and descriptions.
7. Include introductory and concluding turns in the first and last sections respectively, but focus on the substantive content discussed.

When identifying distinct topics or themes, consider:
- Shifts in main subjects
- Transitions between broader themes and specific examples
- The core ideas and arguments presented, rather than conversational formalities

Aim for a balance between thematic integrity and appropriate section length, prioritizing content over structure. The first section should start with turn 0, and the last section should end with the last turn in the transcript.

For reference:
- The host's name is "Dwarkesh Patel".
- Each section must start with a turn from the host and end with a turn from the guest.
- Focus on the substantive content of the dialogue rather than structural elements or pleasantries.
"""

SECTIONING_USER_PROMPT = """Analyze the following interview podcast transcript and divide it into meaningful sections according to the guidelines provided. Structure your response using the StructuredTranscript model, which contains a list of Section objects. The goal is to create a structure that allows for a broader examination of the dialogue themes.

Focus on the primary content and themes of the interview. Ensure that each section provides a clear context for understanding the dialogue within the thematic framework of the conversation. Remember, each section must start with a host turn and end with a guest turn.

Each turn in the transcript is formatted as follows:
[Turn X] Role (Speaker): Action
Text: Full text of the turn

Use both the action summary and the full text to make informed decisions about sectioning. 

Transcript:

{formatted_transcript}
"""

### FUNCTIONS ###

def format_transcript_for_sectioning(transcript_data: Dict[str, Any]) -> str:
    """
    Formats the turn data for sectioning, including turn index, role, speaker, action, and full text.
    Emphasizes the host-guest turn structure.
    """
    formatted_turns = []
    
    for turn in transcript_data['turns']:
        full_text = " ".join([sentence['clean_text'] for sentence in turn['sentences']])
        formatted_turn = f"[Turn {turn['index']}] {turn['role']} ({turn['speaker']}): {turn['action']}\nText: {full_text}"
        formatted_turns.append(formatted_turn)
    
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
            provider="anthropic",
            messages=sectioning_messages,
            response_model=StructuredTranscript
        )

        return response.model_dump()['sections']
    except Exception as e:
        print(f"Error in get_sections:")
        print(traceback.format_exc())
        raise