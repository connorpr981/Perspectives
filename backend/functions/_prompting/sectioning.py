from typing import Any, Dict, List
from pydantic import BaseModel, Field
from _llm.models.message_models import Messages
from _llm.llm_processing import get_response

### RESPONSE MODELS ###

class Section(BaseModel):
    """
    Represents a section of the interview transcript.

    Attributes:
        title (str): An analytical, objective title summarizing the section's main theme.
        subtitle (str): A brief, interpretive description of the section's content.
        description (str): A one-sentence summary of the section's key points.
        start_turn (int): The turn number where this section begins.
        end_turn (int): The turn number where this section ends.
    """
    title: str = Field(..., description="Analytical, objective title summarizing the section's main theme")
    subtitle: str = Field(..., description="Brief, interpretive description of the section's content")
    description: str = Field(..., description="One-sentence summary of the section's key points")
    start_turn: int = Field(..., description="Turn number where this section begins")
    end_turn: int = Field(..., description="Turn number where this section ends")

class StructuredTranscript(BaseModel):
    """
    Represents the entire structured transcript divided into sections.

    Attributes:
        sections (List[Section]): A list of Section objects representing the structured transcript.
    """
    sections: List[Section] = Field(..., description="List of sections representing the structured transcript")

class Criticism(BaseModel):
    """
    Represents expert criticism of a structured transcript, focusing on actionable feedback to achieve an optimal balance of depth and conciseness.

    The ideal structure should have:
    - Sections typically containing 4-8 turns (2-4 question-answer pairs)
    - Clear thematic boundaries between sections
    - Analytical, objective titles and descriptions
    - A logical progression of topics throughout the interview

    Attributes:
        overall_assessment (str): A concise evaluation of the transcript's structure, highlighting adherence to the ideal structure and primary areas for improvement.
        thematic_integrity (str): Analysis of how well each section maintains a cohesive theme, identifying any that are too broad or narrow.
        section_length (str): Evaluation of section lengths, noting any that are too short (less than 4 turns) or too long (more than 8 turns).
        content_representation (str): Assessment of how accurately and objectively titles, subtitles, and descriptions reflect section content.
        narrative_flow (str): Insights into how well the structure captures the logical progression and interconnection of topics throughout the interview.
        key_improvements (List[str]): Prioritized list of specific, actionable recommendations to enhance the transcript's structure, focusing on achieving the ideal balance.
    """
    overall_assessment: str = Field(..., description="Concise evaluation highlighting adherence to the ideal structure and primary areas for improvement")
    thematic_integrity: str = Field(..., description="Analysis of thematic cohesion within sections, identifying any that are too broad or narrow")
    section_length: str = Field(..., description="Evaluation of section lengths, noting any that are too short (less than 4 turns) or too long (more than 8 turns)")
    content_representation: str = Field(..., description="Assessment of how accurately and objectively titles, subtitles, and descriptions reflect section content")
    narrative_flow: str = Field(..., description="Insights into how well the structure captures the logical progression and interconnection of topics")
    key_improvements: List[str] = Field(..., description="Prioritized list of specific, actionable recommendations to achieve the ideal structure")

### PROMPTS ###

SECTIONING_SYSTEM_PROMPT = """You are a world-class qualitative researcher with extensive expertise in content analysis, thematic structuring, and discourse analysis. Your task is to create a meaningful, well-structured representation of a given interview podcast transcript.

Key guidelines:
1. Divide the transcript into non-overlapping sections based on related questions and themes.
2. Each section should have sufficient depth, typically encompassing at least four turns to capture a complete thematic unit.
3. Sections should begin with an interviewer turn to maintain context.
4. Ensure coherence by keeping related questions and answers together within a section.
5. Provide analytical, objective descriptions for titles, subtitles, and summaries.
6. Focus on how question topics evolve throughout the interview.

When identifying distinct topics or themes, consider shifts in main subjects, new concepts, changes in perspective, and transitions between broader themes and specific examples. Aim for a balance between thematic integrity and appropriate section length.
"""

SECTIONING_USER_PROMPT = """Analyze the following interview podcast transcript and divide it into meaningful sections according to the guidelines provided. Structure your response using the StructuredTranscript model, which contains a list of Section objects.

Transcript:

{formatted_transcript}
"""

CRITICISM_PROMPT = """As an expert qualitative researcher, provide nuanced and precise feedback on the following structured transcript. Consider both the original transcript and the proposed structure.

Original Transcript:
{formatted_transcript}

Proposed Structured Transcript:
{structured_transcript}

Analyze the aspects defined in the Criticism model, providing specific criticism and recommendations for improvement. Pay particular attention to the thematic integrity, section boundaries, content representation, narrative flow, and overall balance of the structure.
"""

FINAL_SECTIONING_PROMPT = """Revise the structured transcript based on the expert criticism while adhering to the original sectioning guidelines. Ensure that each section captures a complete thematic unit with appropriate depth.

Original Transcript:
{formatted_transcript}

Initial Structured Transcript:
{initial_structured_transcript}

Expert Criticism:
{criticism}

Provide an improved version of the StructuredTranscript, addressing the feedback and maintaining the key sectioning principles, including thematic coherence, clear section boundaries, accurate content representation, logical narrative flow, and optimal section length.
"""

### FUNCTIONS ###

def format_transcript_for_sectioning(transcript_data: Dict[str, Any]) -> str:
    """
    Formats the transcript data as a string for sectioning by including the turn number, speaker role, speaker name, and text for each turn.
    """
    formatted_turns = []
    for i, turn in enumerate(transcript_data['turns'], 1):
        role = turn['role']
        formatted_turn = f"[Turn {i}] {role} ({turn['speaker']}): {turn['content']}"
        formatted_turns.append(formatted_turn)
    
    return "\n\n".join(formatted_turns)

def get_sections(transcript_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Gets the sections of the transcript by sending a prompt to the LLM to get the sections,
    then requesting criticism, and finally generating an improved version.
    """
    formatted_transcript = format_transcript_for_sectioning(transcript_data)
    
    # Step 1: Initial structuring
    messages = Messages()
    messages.add_system_message(SECTIONING_SYSTEM_PROMPT)
    messages.add_user_message(SECTIONING_USER_PROMPT.format(formatted_transcript=formatted_transcript))
    
    initial_response, _ = get_response(
        provider="anthropic",
        messages=messages,
        response_model=StructuredTranscript,
    )
    
    # Step 2: Criticism
    messages = Messages()
    messages.add_system_message(SECTIONING_SYSTEM_PROMPT)
    messages.add_user_message(CRITICISM_PROMPT.format(
        formatted_transcript=formatted_transcript,
        structured_transcript=initial_response.model_dump_json(indent=2)
    ))
    
    criticism_response, _ = get_response(
        provider="anthropic",
        messages=messages,
        response_model=Criticism,
    )
    
    # Step 3: Final structuring
    messages = Messages()
    messages.add_system_message(SECTIONING_SYSTEM_PROMPT)
    messages.add_user_message(FINAL_SECTIONING_PROMPT.format(
        formatted_transcript=formatted_transcript,
        initial_structured_transcript=initial_response.model_dump_json(indent=2),
        criticism=criticism_response.model_dump_json(indent=2)
    ))
    
    final_response, _ = get_response(
        provider="anthropic",
        messages=messages,
        response_model=StructuredTranscript,
    )
    
    return final_response.model_dump()['sections']