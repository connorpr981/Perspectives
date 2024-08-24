from typing import Any, Dict, List
from pydantic import BaseModel, Field
from _llm.models.message_models import Messages
from _llm.llm_processing import get_response
import traceback

### RESPONSE MODELS ###
class TurnTag(BaseModel):
    turn_index: int = Field(..., description="The index of the turn in the transcript")
    action: str = Field(..., description="The action of the turn, in sentence case (first letter capitalized), as a complete phrase but not a full sentence, including prepositions if necessary (e.g. 'Discussing climate change', 'Asking about future plans', 'Clarifying previous point', 'Suggesting new solution', 'Interrupting with question')")
    people: List[str] = Field(default_factory=list, description="List of people mentioned in this turn")
    places: List[str] = Field(default_factory=list, description="List of places mentioned in this turn")
    things: List[str] = Field(default_factory=list, description="List of significant things or concepts mentioned in this turn")

class TurnTags(BaseModel):
    tags: List[TurnTag] = Field(..., description="A list of tags for the transcript")

### PROMPTS ###
CHUNK_SIZE = 20  # Number of turns to process in each chunk

TAGGING_SYSTEM_PROMPT = """You are a world-class qualitative researcher with extensive expertise in content analysis, thematic structuring, and discourse analysis. 
Your task is to create a meaningful, well-structured representation of a given interview podcast transcript chunk, with the ultimate goal of facilitating a closer examination of the dialogue.

Instructions:
1. You will be given a chunk of turns from a transcript, and you will need to tag each turn with an action, people mentioned, places mentioned, and significant things or concepts discussed.
2. The action should be in sentence case (first letter capitalized), as a complete phrase but not a full sentence, and include prepositions if necessary (e.g. 'Discussing climate change', 'Asking about future plans', 'Clarifying previous point', 'Suggesting new solution', 'Interrupting with question').
3. Focus on capturing the essence of the turn's content and its role in the conversation.
4. For people, places, and things:
   - Include only those explicitly mentioned in the turn.
   - Use proper nouns where applicable.
   - For things, focus on significant concepts, objects, or ideas central to the discussion.

Important:
- Ensure the action is specific enough to convey the turn's purpose but general enough to be applicable across similar turns.
- Maintain consistency with any previous tags provided for context.
- Use prepositions when necessary for clarity and grammatical correctness.
- Use sentence case (capitalize the first letter, rest lowercase) for each action.
- Actions should be complete phrases but not full sentences (no period at the end).
- Lists for people, places, and things can be empty if none are mentioned.

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
        if tag.people:
            turn_info += f"\n  People: {', '.join(tag.people)}"
        if tag.places:
            turn_info += f"\n  Places: {', '.join(tag.places)}"
        if tag.things:
            turn_info += f"\n  Things: {', '.join(tag.things)}"
        formatted_tags.append(turn_info)
    return "\n\n".join(formatted_tags)