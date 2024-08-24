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
    end_turn: int = Field(..., description="Index of the last turn in this section (must be a guest turn)")

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

SECTIONING_SYSTEM_PROMPT = """You are an expert in content analysis and thematic structuring. Your task is to divide a podcast interview transcript into meaningful sections.

Guidelines:
1. Divide the transcript into sections based on primary themes and content.
2. Each section must begin with a host turn and end with a guest turn.
3. Group turns primarily by content and thematic coherence.
4. Sections should be between 8-12 turns long, whichever length makes most sense based on the context.
5. There should be absolutely no sections shorter than 4 turns.
6. Be attentive to natural topic transitions, which often occur when the host asks a new question.
7. Consider the flow of the conversation and how ideas develop throughout the interview.
8. Recognize that some topics may be revisited or expanded upon later in the interview; these can be separate sections if substantial new information is added.
9. Be aware of segment breaks, introductions, or conclusions that may be present in the podcast format.
10. For each section, provide:
    - A concise (3-7 words) title
    - A brief (10-15 words) subtitle
    - A summary (2-3 sentences) of the content
    - The start turn index (must be a host turn)
    - The end turn index (must be a guest turn)
11. Focus on the logical progression of the conversation and core ideas presented.
12. The first section should start with turn 0, and the last section should end with the last turn in the transcript.
13. Pay attention to key terms mentioned in each turn, as they may indicate important topics or themes.
14. If a thematic break occurs slightly before or after the 8-12 turn range, prioritize the thematic coherence over strict adherence to the turn count.
15. In cases where a section would exceed 12 turns, look for the most natural breaking point within the 8-12 turn range.

Remember: The goal is to create meaningful, coherent sections that accurately represent the content and flow of the interview while adhering to the specified turn count guidelines.
"""

SECTIONING_USER_PROMPT = """Analyze the following interview transcript and divide it into sections according to the guidelines provided. Structure your response using the StructuredTranscript model.

Each turn in the transcript is formatted as:
[Turn X] Role (Speaker): Action
(Optional) Key Terms: List of key terms mentioned in the turn, if any
Text: Full text of the turn

Use both the action summary and the full text for sectioning. Provide the start and end turn indices for each section.

Transcript:

{formatted_transcript}
"""

### FUNCTIONS ###

def format_transcript_for_sectioning(transcript_data: Dict[str, Any]) -> str:
    formatted_turns = []
    for turn in transcript_data['turns']:
        index = turn['index']
        role = turn['role']
        speaker = turn['speaker']
        action = turn['action']
        key_terms = ", ".join(turn['key_terms']) if turn['key_terms'] else "None"
        full_text = " ".join([sentence['clean_text'] for sentence in turn['sentences']])
        if key_terms:
            formatted_turn = f"[Turn {index}] {role} ({speaker}): {action}\nKey Terms: {key_terms}\nText: {full_text}"
        else:
            formatted_turn = f"[Turn {index}] {role} ({speaker}): {action}\nText: {full_text}"
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