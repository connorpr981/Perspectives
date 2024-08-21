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
    - Sections containing 4-16 turns
    - Clear thematic boundaries between sections
    - Analytical, objective titles and descriptions
    - A logical progression of topics throughout the interview

    Attributes:
        overall_assessment (str): A concise evaluation of the transcript's structure, highlighting adherence to the ideal structure and primary areas for improvement.
        thematic_integrity (str): Analysis of how well each section maintains a cohesive theme, identifying any that are too broad or narrow.
        section_length (str): Evaluation of section lengths, noting any that are too short (less than 4 turns) or too long (more than 16 turns).
        content_representation (str): Assessment of how accurately and objectively titles, subtitles, and descriptions reflect section content.
        narrative_flow (str): Insights into how well the structure captures the logical progression and interconnection of topics throughout the interview.
        balance (str): Analysis of the overall distribution of sections, focusing on adherence to the 4-16 turn guideline and identifying any imbalances or bloated sections.
        key_improvements (List[str]): Prioritized list of specific, actionable recommendations to enhance the transcript's structure, focusing on achieving the ideal balance.
    """
    overall_assessment: str = Field(..., description="Concise evaluation highlighting adherence to the ideal structure and primary areas for improvement")
    thematic_integrity: str = Field(..., description="Analysis of thematic cohesion within sections, identifying any that are too broad or narrow")
    section_length: str = Field(..., description="Evaluation of section lengths, noting any that are too short (less than 4 turns) or too long (more than 16 turns)")
    content_representation: str = Field(..., description="Assessment of how accurately and objectively titles, subtitles, and descriptions reflect section content")
    narrative_flow: str = Field(..., description="Insights into how well the structure captures the logical progression and interconnection of topics")
    balance: str = Field(..., description="Analysis of the overall distribution of sections, focusing on adherence to the 4-16 turn guideline and identifying any imbalances or bloated sections")
    key_improvements: List[str] = Field(..., description="Prioritized list of specific, actionable recommendations to achieve the ideal structure")

class ThemeGuide(BaseModel):
    """
    Represents a high-level guide to the structure and themes of the interview.

    Attributes:
        overall_structure (str): A brief overview of the interview's structure and flow.
        main_themes (List[str]): A list of the primary themes or topics discussed in the interview.
        theme_progression (str): A description of how themes evolve and interconnect throughout the interview.
        key_points (List[str]): A list of the most significant points or insights from the interview.
    """
    overall_structure: str = Field(..., description="Brief overview of the interview's structure and flow")
    main_themes: List[str] = Field(..., description="List of primary themes or topics discussed")
    theme_progression: str = Field(..., description="Description of how themes evolve and interconnect")
    key_points: List[str] = Field(..., description="List of the most significant points or insights")

### PROMPTS ###

SECTIONING_SYSTEM_PROMPT = """You are a world-class qualitative researcher with extensive expertise in content analysis, thematic structuring, and discourse analysis. Your task is to create a meaningful, well-structured representation of a given interview podcast transcript, with the ultimate goal of facilitating a closer examination of the guest's responses to the host's questions.

Key guidelines:
1. Divide the transcript into non-overlapping sections based on primary themes and content, not structural elements. This will allow for a more focused analysis of the guest's responses within each thematic context.
2. Each section should have sufficient depth, encompassing 4-16 turns to capture a complete thematic unit and the full context of the guest's responses.
3. Sections should begin with an interviewer turn to maintain context and highlight the relationship between questions and answers.
4. Always keep questions and their corresponding answers together within the same section. Never separate them, as this ensures a comprehensive view of the guest's responses in relation to the questions asked.
5. Provide analytical, objective descriptions for titles, subtitles, and summaries, following these specific guidelines:
   - Title: A concise (3-7 words), analytical phrase capturing the main theme or topic of the section, reflecting the core of the guest's responses.
   - Subtitle: A brief (10-15 words) interpretive description that provides context or a key insight about the section's content, highlighting the guest's perspective.
   - Description: A one-sentence (15-25 words) summary of the section's key points, focusing on the most important ideas discussed by the guest.
6. Focus on how question topics evolve throughout the interview, capturing the logical progression of the conversation and the development of the guest's thoughts and responses.
7. Incorporate introductions and conclusions into the first and last sections respectively, but do not make them the primary focus of these sections unless exceptionally long (more than 8 turns).
8. Avoid creating separate sections for greetings, introductions, or conclusions unless they are exceptionally long.

When identifying distinct topics or themes, consider:
- Shifts in main subjects
- Introduction of new concepts by the guest
- Changes in perspective or approach to a topic in the guest's responses
- Transitions between broader themes and specific examples in the dialogue

Aim for a balance between thematic integrity and appropriate section length, always prioritizing content over structure. Remember that the primary goal is to create a meaningful representation of the interview's content that facilitates a deeper understanding of the guest's responses and perspectives.
"""

SECTIONING_USER_PROMPT = """Analyze the following interview podcast transcript and divide it into meaningful sections according to the guidelines provided. Structure your response using the StructuredTranscript model, which contains a list of Section objects. The ultimate goal is to create a structure that allows for a closer examination of the guest's responses to the host's questions.

Remember to focus on the primary content and themes of the interview, not structural elements. Introductions and conclusions should be part of the first and last sections respectively, but should not be their main focus unless exceptionally long. Ensure that each section provides a clear context for understanding the guest's responses within the thematic framework of the conversation.

Transcript:

{formatted_transcript}
"""

CRITICISM_PROMPT = """As an expert qualitative researcher, provide targeted feedback on the structure of the following transcript. Focus solely on the structural aspects that align with our goals for an ideal interview transcript structure, keeping in mind that our ultimate objective is to facilitate a closer examination of the guest's responses to the host's questions.

Original Transcript:
{formatted_transcript}

Proposed Structured Transcript:
{structured_transcript}

Analyze the structure using the Criticism model, providing specific feedback and recommendations for improvement. Focus on:
1. Thematic integrity: Ensure each section maintains a cohesive theme without being too broad or narrow, allowing for a clear context to examine the guest's responses.
2. Section length: Aim for sections containing 4-16 turns, identifying any that are too short or long. For sections exceeding 16 turns:
   a. Identify natural thematic breaks or shifts in the conversation.
   b. Suggest splitting the section at these points, ensuring each new section maintains thematic coherence.
   c. Recommend new titles, subtitles, and descriptions for the split sections.
3. Content representation: Evaluate how well titles, subtitles, and descriptions reflect the content objectively and analytically, with a focus on highlighting the guest's key points and perspectives.
4. Narrative flow: Assess the logical progression and interconnection of topics throughout the interview, ensuring that the development of the guest's thoughts is clearly represented.
5. Handling of introductions and conclusions: Ensure these are incorporated into the first and last sections without being their primary focus, unless they contain significant content from the guest.
6. Balance: Analyze the overall distribution of sections, focusing on adherence to the 4-16 turn guideline and identifying any imbalances or bloated sections that might obscure the guest's responses.

Provide actionable recommendations to improve the structure while maintaining our key principles:
- Content-based sectioning (not based on structural elements)
- Clear thematic boundaries between sections
- Appropriate section lengths (4-16 turns)
- Analytical and objective content representation
- Logical topic progression
- Balanced distribution of sections
- Facilitation of closer examination of guest responses

When suggesting improvements for overly long sections, provide specific guidance on where to split the section and how to maintain thematic coherence in the resulting new sections.

Do not suggest changes that contradict these principles or our overall goals for the transcript structure.
"""

FINAL_SECTIONING_PROMPT = """Revise the structured transcript based on the expert criticism while adhering to the original sectioning guidelines. Ensure that each section captures a complete thematic unit with appropriate depth, focusing on content rather than structural elements. Remember that our ultimate goal is to create a structure that allows for a closer examination of the guest's responses to the host's questions.

Expert Criticism:
{criticism}

Provide an improved version of the StructuredTranscript, addressing the feedback and maintaining the key sectioning principles, including:
1. Content-based thematic coherence
2. Clear section boundaries
3. Accurate content representation, highlighting the guest's key points and perspectives
4. Logical narrative flow that shows the development of the guest's thoughts
5. Optimal section length (4-16 turns)
6. Appropriate incorporation of introductions and conclusions into the first and last sections without making them the primary focus
7. Balanced distribution of sections that facilitates analysis of the guest's responses

Remember to prioritize the main themes and content of the interview when creating sections, always keeping in mind how each section contributes to our understanding of the guest's responses and viewpoints.
"""

THEME_GUIDE_PROMPT = """As an expert in content analysis, review the following interview transcript and create a high-level guide to its structure and themes. This guide will be used to inform the subsequent sectioning process, ensuring that the final structure accurately reflects the content and flow of the interview.

Focus on identifying the main themes, their progression, and the overall structure of the interview. Pay particular attention to the interviewer's questions and how they guide the conversation, as well as the guest's key points and insights.

Transcript:
{formatted_transcript}

Provide your analysis in the form of a ThemeGuide object, which includes:
1. An overall_structure summary
2. A list of main_themes
3. A description of the theme_progression
4. A list of key_points from the interview

Your guide should provide a clear roadmap for understanding the interview's content and structure, facilitating the creation of meaningful sections that allow for a closer examination of the guest's responses to the host's questions.
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
    Gets the sections of the transcript by first creating a theme guide,
    then sending a prompt to the LLM to get the sections,
    then requesting criticism, and finally generating an improved version.
    """
    formatted_transcript = format_transcript_for_sectioning(transcript_data)
    
    # Step 1: Generate Theme Guide
    theme_guide_messages = Messages()
    theme_guide_messages.add_system_message(SECTIONING_SYSTEM_PROMPT)
    theme_guide_messages.add_user_message(THEME_GUIDE_PROMPT.format(formatted_transcript=formatted_transcript))
    
    theme_guide, _ = get_response(
        provider="openai",
        messages=theme_guide_messages,
        response_model=ThemeGuide,
    )
    
    # Step 2: Initial structuring
    sectioning_messages = Messages()
    sectioning_messages.add_system_message(SECTIONING_SYSTEM_PROMPT)
    sectioning_messages.add_user_message(f"""
    Here's a high-level guide to the structure and themes of the interview:
    {theme_guide.model_dump_json(indent=2)}
    
    Using this guide, please structure the following transcript:
    
    {SECTIONING_USER_PROMPT.format(formatted_transcript=formatted_transcript)}
    """)
    
    initial_response, _ = get_response(
        provider="openai",
        messages=sectioning_messages,
        response_model=StructuredTranscript,
    )
    sectioning_messages.add_assistant_message(initial_response.model_dump_json(indent=2))
    
    # Step 3: Criticism
    criticism_messages = Messages()
    criticism_messages.add_system_message(SECTIONING_SYSTEM_PROMPT)
    criticism_messages.add_user_message(CRITICISM_PROMPT.format(
        formatted_transcript=formatted_transcript,
        structured_transcript=initial_response.model_dump_json(indent=2)
    ))
    
    criticism_response, _ = get_response(
        provider="openai",
        messages=criticism_messages,
        response_model=Criticism,
    )
    
    # Step 4: Final structuring
    sectioning_messages.add_user_message(FINAL_SECTIONING_PROMPT.format(
        criticism=criticism_response.model_dump_json(indent=2)
    ))
    
    final_response, _ = get_response(
        provider="openai",
        messages=sectioning_messages,
        response_model=StructuredTranscript,
    )
    
    return final_response.model_dump()['sections']