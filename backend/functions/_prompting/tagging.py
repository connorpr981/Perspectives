from typing import Any, Dict, List
from pydantic import BaseModel, Field
from _llm.models.message_models import Messages
from _llm.llm_processing import get_response
import traceback

### RESPONSE MODELS ###
class TurnTag(BaseModel):
    turn_index: int = Field(..., description="The index of the turn in the transcript")
    action: str = Field(..., description="The action of the turn, in sentence case (first letter capitalized), as a complete phrase but not a full sentence, including prepositions if necessary")
    key_terms: List[str] = Field(default_factory=list, description="List of key terms that might need definitions or explanations")

class TurnTags(BaseModel):
    tags: List[TurnTag] = Field(..., description="A list of tags for the transcript")

### PROMPTS ###
CHUNK_SIZE = 20  # Number of turns to process in each chunk

TAGGING_SYSTEM_PROMPT = """You are a world-class qualitative researcher with extensive expertise in content analysis, thematic structuring, and discourse analysis. 
Your task is to create a meaningful, well-structured representation of a given interview podcast transcript chunk, identifying terms that might need definitions or explanations for a general audience.

Instructions:
1. For each turn in the transcript chunk, provide an action that summarizes the turn's purpose and a list of key terms that might need definitions.
2. The action should be in sentence case (first letter capitalized), as a complete phrase but not a full sentence, and include prepositions if necessary (e.g., 'Discussing climate change', 'Explaining quantum computing', 'Comparing economic policies').
3. For key terms:
   - Include proper nouns, technical terms, jargon, acronyms, and any words or phrases that might not be immediately clear to a general audience.
   - Use title case for all key terms (capitalize the first letter of each major word).
   - For acronyms, include the full spelling in title case with the acronym in parentheses next to it when first mentioned.
   - Include terms even if they've been mentioned in previous turns, as each turn's list should be self-contained.
   - Focus on terms that are central to understanding the content of the turn.

Examples of key terms:
- People: 'Elon Musk', 'Alan Turing', 'Angela Merkel'
- Organizations: 'NASA (National Aeronautics and Space Administration)', 'WHO (World Health Organization)'
- Places: 'Silicon Valley', 'CERN (European Organization for Nuclear Research)'
- Concepts: 'Machine Learning', 'Quantitative Easing', 'Blockchain'
- Events: 'Arab Spring', 'Bretton Woods Conference'
- Technical terms: 'RNA (Ribonucleic Acid)', 'Dark Matter', 'Quantum Entanglement'

Important:
- Ensure the action captures the main purpose or content of the turn.
- Include only terms that are actually mentioned or directly relevant to the turn's content.
- Aim for clarity and relevance in selecting key terms. Not every proper noun or technical term needs to be included, only those that significantly contribute to understanding the content.
- Maintain strict consistency in how you format and spell key terms across all turns. If a term has been mentioned before, use exactly the same formatting and spelling as in its previous occurrence.
- Always use title case for key terms, capitalizing the first letter of each major word (e.g., 'Machine Learning', 'Artificial Intelligence', 'World War II').
- For acronyms, use the full spelling in title case with the acronym in parentheses on first mention (e.g., 'Artificial Intelligence (AI)'). In subsequent mentions within the same turn or later turns, use just the acronym (e.g., 'AI').
- The list of key terms can be empty if the turn doesn't contain any terms likely to need definition for a general audience.
- Pay close attention to capitalization, spacing, and punctuation when formatting key terms.

This transcript chunk has {num_turns} turns. Ensure that you tag all turns in the chunk.
"""

### FUNCTIONS ###
def get_tags(transcript_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Formats the transcript and sends it to the LLM to obtain tags in chunks.
    """
    try:
        all_tags = []
        turns = transcript_data['turns']
        num_turns = len(turns)
        
        for i in range(0, num_turns, CHUNK_SIZE):
            chunk = turns[i:i+CHUNK_SIZE]
            chunk_transcript = format_transcript_chunk(chunk)
            
            tagging_messages = Messages()
            tagging_messages.add_system_message(TAGGING_SYSTEM_PROMPT.format(num_turns=len(chunk)))
            
            # Add context from previous tags
            if all_tags:
                context = format_tag_context(all_tags[-CHUNK_SIZE:])
                tagging_messages.add_user_message(f"Previous tags:\n{context}\n\nContinue tagging with the following transcript chunk: {chunk_transcript}")
            else:
                # Add this line to ensure there's always a user message
                tagging_messages.add_user_message(f"Tag the following transcript chunk: {chunk_transcript}")
                        
            chunk_tags, _ = get_response(
                provider="openai",
                messages=tagging_messages,
                response_model=TurnTags
            )
            
            # Adjust turn indices to match the full transcript
            for tag in chunk_tags.tags:
                tag.turn_index += i
            
            all_tags.extend(chunk_tags.tags)
        
        return all_tags
    except Exception as e:
        error_message = f"Error in get_tags: {str(e)}\n{traceback.format_exc()}"
        print(error_message)
        raise

def format_transcript_chunk(chunk: List[Dict[str, Any]]) -> str:
    """
    Formats a chunk of the transcript for tagging.
    """
    formatted_turns = []
    for i, turn in enumerate(chunk, 0):
        role = turn['role']
        clean_content = ' '.join(sentence['clean_text'] for sentence in turn['sentences'])
        formatted_turn = f"[Turn {i}] {role} ({turn['speaker']}): {clean_content}"
        formatted_turns.append(formatted_turn)
    
    return "\n\n".join(formatted_turns)

def format_tag_context(tags: List[TurnTag]) -> str:
    """
    Formats the previous tags as context for the next chunk.
    """
    formatted_tags = []
    for tag in tags:
        turn_info = f"Turn {tag.turn_index}: {tag.action}"
        if tag.key_terms:
            turn_info += f"\n  Key terms: {', '.join(tag.key_terms)}"
        formatted_tags.append(turn_info)
    return "\n\n".join(formatted_tags)