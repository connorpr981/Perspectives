from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from _llm.models.message_models import Messages
from _llm.llm_processing import get_response
from _utils.firestore_utils import get_firestore_client
import traceback
import logging
from _helpers.question_helper import generate_questions, format_section_for_questioning
from datetime import datetime

current_date = datetime.now().strftime("%Y-%m-%d")

### RESPONSE MODELS ###

class Perspective(BaseModel):
    name: str = Field(..., description="The name of the specific group or individual type")

class ReflectiveQuestion(BaseModel):
    question: str = Field(..., description="The reflective question that encourages critical thinking")
    action: str = Field(..., description="A short, descriptive gerund phrase summarizing the question's focus")
    perspectives: List[Perspective] = Field(
        ...,
        min_items=3,
        max_items=5,
        description="List of 3-5 specific groups or types of individuals who would have unique viewpoints on this question"
    )

class ReflectiveQuestions(BaseModel):
    """
    Represents reflective questions generated for a specific turn in the transcript.

    Attributes:
        turn_index (int): The index of the turn in the transcript.
        reflective_questions (List[ReflectiveQuestion]): List of questions that encourage reflection and consideration of multiple perspectives.
    """
    turn_index: int = Field(..., description="The index of the turn in the transcript")
    reflective_questions: List[ReflectiveQuestion] = Field(
        ...,
        min_items=1,
        max_items=5,
        description="List of 1-5 questions that encourage reflection and consideration of multiple perspectives."
    )

class SectionReflectiveQuestions(BaseModel):
    """
    Represents a collection of reflective questions for a section of the transcript.

    Attributes:
        questions (Optional[List[ReflectiveQuestions]]): A list of ReflectiveQuestions objects for the transcript section, if any.
    """
    questions: Optional[List[ReflectiveQuestions]] = Field(None, description="A list of reflective questions for the transcript section, if any")

### PROMPTS ###

REFLECTIVE_QUESTIONING_SYSTEM_PROMPT = f"""You are an expert in generating thought-provoking, reflective questions based on interview topics. Your task is to create reflective questions for each turn in the given transcript section that would benefit from multiple, specific perspectives. Today's date is {current_date}.

Goal: Encourage critical thinking and consideration of diverse viewpoints related to the topics discussed, without summarizing the transcript or inviting debate on sensitive issues.

Guidelines for Reflective Questions:
1. Generate 1-5 reflective questions per turn.
2. Questions should:
   - Encourage critical thinking and consideration of multiple viewpoints.
   - Be open-ended and not have a single "correct" answer.
   - Relate directly to the content of the turn without referencing it explicitly.
   - Be suitable for thoughtful discussion or personal reflection.
   - Avoid being overly controversial or divisive.
   - Be answerable based on real-world knowledge and experiences.

3. For each reflective question, specify:
   - An action: A short, descriptive gerund phrase summarizing the question's focus (e.g., "Exploring ethical implications", "Considering long-term consequences", "Analyzing cultural differences").
   - 3-5 specific groups or types of individuals who would have unique viewpoints on this question.
   - Use Title Case for each perspective name.

4. Ensuring Diversity and Specificity in Perspectives:
   - Aim for a diverse range of perspectives across questions to provide a well-rounded reflective experience.
   - Be very specific in choosing perspectives, avoiding broad categories.
   - Consider demographics, professions, experiences, and cultural backgrounds when selecting perspectives.
   - Ensure that the perspectives are directly relevant to the question and would provide meaningful insights.

Examples of Good Reflective Questions with Actions and Perspectives:
1. Question: "How might the widespread adoption of AI in healthcare affect the quality and accessibility of patient care?"
   Action: Evaluating AI's impact on healthcare
   Perspectives:
   - Elderly Patients In Rural Areas
   - Tech-Savvy Doctors In Urban Hospitals
   - Health Insurance Company Executives
   - AI Researchers In Medical Diagnostics
   - Nurses In Understaffed Community Clinics

2. Question: "What are the potential long-term impacts of remote work on urban development and community structures?"
   Action: Analyzing remote work's societal effects
   Perspectives:
   - Small Town Mayors
   - Commercial Real Estate Developers
   - Work-From-Home Parents
   - Local Small Business Owners
   - Urban Transportation Planners

Examples of Bad Reflective Questions:
1. "Is artificial intelligence good or bad for society?" (Too broad and simplistic)
2. "What did the speaker say about climate change?" (Directly references the transcript)
3. "Who is responsible for solving world hunger?" (Too complex and potentially divisive)
4. "How will technology change in the next 100 years?" (Too speculative and broad)
5. "What is the best way to learn a new language?" (Lacks depth for multiple perspectives)

Remember:
- Questions should encourage thoughtful reflection and consideration of multiple, specific viewpoints related to the topics discussed in each turn.
- Aim for a mix of question types and perspectives across the section to provide a well-rounded reflective experience.
- Each question should be crafted to elicit diverse, thoughtful responses based on real-world knowledge and experiences.
- Avoid questions that are too speculative, broad, or lacking in potential for diverse perspectives.

This transcript section has {{num_turns}} turns. Generate reflective questions for all turns in the section.
"""

REFLECTIVE_QUESTIONING_USER_PROMPT = """Generate reflective questions for the following transcript section topics:

{formatted_section}

Structure your response using the SectionReflectiveQuestions model, ensuring each turn has 1-5 reflective questions with the appropriate action and perspectives specified.
"""

### FUNCTIONS ###

def get_reflective_questions_for_section(section_data: Dict[str, Any]) -> Optional[List[ReflectiveQuestions]]:
    """
    Generate reflective questions for a given section of the transcript.

    Args:
        section_data (Dict[str, Any]): The data for a section of the transcript.

    Returns:
        Optional[List[ReflectiveQuestions]]: A list of ReflectiveQuestions objects for the section, or None if an error occurs.
    """
    try:
        formatted_section = format_section_for_questioning(section_data)
        
        questioning_messages = Messages()
        questioning_messages.add_system_message(REFLECTIVE_QUESTIONING_SYSTEM_PROMPT.format(num_turns=len(section_data['turns']), current_date=current_date))
        questioning_messages.add_user_message(REFLECTIVE_QUESTIONING_USER_PROMPT.format(formatted_section=formatted_section))
        
        response, _ = get_response(
            provider="anthropic",
            messages=questioning_messages,
            response_model=SectionReflectiveQuestions
        )

        return response.questions
    except Exception as e:
        error_message = f"Error in get_reflective_questions_for_section: {str(e)}\n{traceback.format_exc()}"
        logging.error(error_message)
        raise

def get_reflective_questions(transcript_id: str, test_mode: bool = False) -> List[ReflectiveQuestions]:
    """
    Generate reflective questions for all sections of a transcript.

    Args:
        transcript_id (str): The ID of the transcript.
        test_mode (bool, optional): If True, only process the first section. Defaults to False.

    Returns:
        List[ReflectiveQuestions]: A list of ReflectiveQuestions objects for all processed sections.
    """
    return generate_questions(transcript_id, get_reflective_questions_for_section, "reflective", test_mode)