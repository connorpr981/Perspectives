from typing import List, Dict, Any, Callable
from google.cloud.firestore_v1.document import DocumentReference
from pydantic import BaseModel
from _utils.firestore_utils import get_firestore_client, update_or_create_tag, update_tag_context, update_turn_tag_context
import logging
from _helpers.transcript_helper import find_turn_in_sections
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, List, Tuple
from google.cloud.firestore_v1.document import DocumentReference
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import time

def create_tag_index(tags: List[BaseModel], transcript_id: str) -> Dict[str, List[str]]:
    """
    Creates a dictionary where keys are unique key terms and values are lists of turn IDs.
    
    :param tags: List of TurnTag objects as returned by get_tags()
    :param transcript_id: ID of the transcript
    :return: Dictionary mapping key terms to lists of turn IDs
    """
    db = get_firestore_client()
    transcript_ref = db.collection('transcripts').document(transcript_id)
    turns = {turn.to_dict()['index']: turn.id for turn in transcript_ref.collection('turns').stream()}
    
    tag_index = {}
    
    for tag in tags:
        tag_dict = tag.model_dump()
        turn_index = tag_dict['turn_index']
        turn_id = turns.get(turn_index)
        
        if not turn_id:
            logging.warning(f"Turn with index {turn_index} not found in transcript {transcript_id}")
            continue
        
        # Process key terms from the tag
        for key_term in tag_dict['key_terms']:
            if key_term not in tag_index:
                tag_index[key_term] = []
            tag_index[key_term].append(turn_id)
    
    return tag_index

def create_tags_collection(tag_index: Dict[str, List[str]], transcript_id: str) -> None:
    """
    Updates the 'tags' collection in Firestore with tag documents containing turn references.
    Deduplicates and updates existing tags using batch writes.
    
    :param tag_index: Dictionary mapping key terms to lists of turn IDs
    :param transcript_id: ID of the transcript
    """
    for key_term, turn_ids in tag_index.items():
        try:
            update_or_create_tag(key_term, turn_ids, transcript_id)
            logging.info(f"Updated or created tag: {key_term}")
        except Exception as e:
            logging.error(f"Error processing tag {key_term}: {str(e)}")

    logging.info("Finished updating tags collection")

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10), retry=retry_if_exception_type(ValueError))
def generate_tag_context_with_retry(generate_tag_context_func: Callable, tag_term: str, turn_content: str) -> str:
    result = generate_tag_context_func(tag_term, turn_content)
    time.sleep(3)  # Add a 1-second delay after each API call
    return result

def process_single_tag(tag: DocumentReference, transcript_id: str, transcript_ref: DocumentReference, generate_tag_context_func: Callable, force_regenerate: bool = False) -> Tuple[str, int, int, List[Tuple[str, str]]]:
    tag_data = tag.to_dict()
    tag_term = tag_data['term']
    tag_turn_count = 0
    tag_success_count = 0
    skipped_turns = []

    for turn_ref in tag_data['turn_refs']:
        if turn_ref['transcript_id'] == transcript_id:
            tag_turn_count += 1
            turn_id = turn_ref['turn_id']
            
            logging.info(f"Processing turn {turn_id} for tag {tag_term}")
            turn_data, section_id = find_turn_in_sections(transcript_ref, turn_id)

            if not turn_data:
                logging.warning(json.dumps({
                    "message": "Turn not found",
                    "transcript_id": transcript_id,
                    "tag": tag_term,
                    "turn_id": turn_id
                }))
                continue

            # Check if context already exists
            existing_context = turn_ref.get('context')
            if existing_context and not force_regenerate:
                logging.info(f"Context already exists for turn {turn_id} and tag {tag_term}")
                tag_success_count += 1
                continue

            turn_content = turn_data.get('content', '')

            try:
                tag_context = generate_tag_context_with_retry(generate_tag_context_func, tag_term, turn_content)

                logging.info(f"Updating turn tag context for turn {turn_id} in section {section_id}")
                update_turn_tag_context(transcript_ref.collection('sections').document(section_id).collection('turns').document(turn_id), tag_term, tag_context)
                
                logging.info(f"Updating tag context for tag {tag_term} and turn {turn_id}")
                update_tag_context(tag.reference, turn_id, tag_context)

                tag_success_count += 1

                logging.info(json.dumps({
                    "message": "Tag context generated and updated",
                    "transcript_id": transcript_id,
                    "tag": tag_term,
                    "turn_id": turn_id
                }))
            except Exception as e:
                skipped_turns.append((tag_term, turn_id))
                logging.error(json.dumps({
                    "message": "Failed to generate tag context",
                    "transcript_id": transcript_id,
                    "tag": tag_term,
                    "turn_id": turn_id,
                    "error": str(e)
                }))
                logging.exception("Exception details:")

    return tag_term, tag_turn_count, tag_success_count, skipped_turns

def process_transcript_tags(transcript_id: str, generate_tag_context_func: Callable, force_regenerate: bool = False) -> None:
    db = get_firestore_client()
    transcript_ref = db.collection('transcripts').document(transcript_id)
    tags_collection = db.collection('tags')

    all_tags = tags_collection.stream()
    matching_tags = [tag for tag in all_tags if any(ref['transcript_id'] == transcript_id for ref in tag.to_dict().get('turn_refs', []))]

    logging.info(json.dumps({
        "message": "Matching tags found",
        "transcript_id": transcript_id,
        "tag_count": len(matching_tags)
    }))

    turn_count = 0
    successful_tags = 0
    all_skipped_turns = []

    for tag in matching_tags:  # Process all matching tags
        tag_term, tag_turn_count, tag_success_count, skipped_turns = process_single_tag(tag, transcript_id, transcript_ref, generate_tag_context_func, force_regenerate)
        turn_count += tag_turn_count
        successful_tags += tag_success_count
        all_skipped_turns.extend(skipped_turns)

        logging.info(json.dumps({
            "message": "Tag processing completed",
            "transcript_id": transcript_id,
            "tag": tag_term,
            "turns_processed": tag_turn_count,
            "successful_turns": tag_success_count,
            "skipped_turns": len(skipped_turns)
        }))

    logging.info(json.dumps({
        "message": "Tag context generation completed",
        "transcript_id": transcript_id,
        "total_tags_processed": len(matching_tags),
        "total_turns_processed": turn_count,
        "successful_tags": successful_tags,
        "skipped_turns": len(all_skipped_turns)
    }))

    if all_skipped_turns:
        logging.warning(json.dumps({
            "message": "Skipped turns summary",
            "transcript_id": transcript_id,
            "skipped_turns": all_skipped_turns
        }))