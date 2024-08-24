from typing import List, Dict, Any, Callable
from google.cloud.firestore_v1.document import DocumentReference
from pydantic import BaseModel
from _utils.firestore_utils import get_firestore_client
from google.cloud.firestore_v1 import WriteBatch
import logging

def create_tag_index(tags: List[BaseModel], transcript_id: str) -> Dict[str, List[DocumentReference]]:
    """
    Creates a dictionary where keys are unique key terms and values are lists of turn references where they appear.
    Also includes links and titles from the sentences' extracted_information.
    
    :param tags: List of TurnTag objects as returned by get_tags()
    :param transcript_id: ID of the transcript
    :return: Dictionary mapping key terms to lists of turn references
    """
    db = get_firestore_client()
    tag_index = {}
    
    for tag in tags:
        tag_dict = tag.model_dump()
        turn_index = tag_dict['turn_index']
        turn_ref = db.collection('transcripts').document(transcript_id).collection('turns').document(f'turn_{turn_index}')
        
        # Process key terms from the tag
        for key_term in tag_dict['key_terms']:
            if key_term not in tag_index:
                tag_index[key_term] = []
            tag_index[key_term].append(turn_ref)
        
        # Fetch sentences for this turn
        sentences = turn_ref.collection('sentences').stream()
        for sentence in sentences:
            sentence_data = sentence.to_dict()
            extracted_info = sentence_data.get('extracted_information', {})
            
            # Process links
            links = extracted_info.get('links', {})
            for link_text, link_url in links.items():
                if link_text not in tag_index:
                    tag_index[link_text] = []
                tag_index[link_text].append(turn_ref)
                
                # Also add the URL as a separate tag
                if link_url not in tag_index:
                    tag_index[link_url] = []
                tag_index[link_url].append(turn_ref)
            
            # Process titles
            titles = extracted_info.get('titles', [])
            for title in titles:
                if title not in tag_index:
                    tag_index[title] = []
                tag_index[title].append(turn_ref)
    
    return tag_index

def create_tags_collection(tag_index: Dict[str, List[DocumentReference]]) -> None:
    """
    Updates the 'tags' collection in Firestore with tag documents containing turn references.
    Deduplicates and updates existing tags using batch writes.
    
    :param tag_index: Dictionary mapping key terms to lists of turn references
    """
    db = get_firestore_client()
    tags_collection = db.collection('tags')
    
    # Create a batch
    batch = db.batch()
    
    for key_term, turn_refs in tag_index.items():
        try:
            # Query for existing tag document
            existing_tag_query = tags_collection.where('term', '==', key_term).limit(1)
            existing_tag_docs = existing_tag_query.get()
            
            if existing_tag_docs:
                # Update existing tag document
                existing_tag = existing_tag_docs[0]
                existing_data = existing_tag.to_dict()
                existing_refs = set(ref['turn_ref'] for ref in existing_data.get('turn_refs', []))
                new_refs = set(turn_refs)
                updated_refs = list(existing_refs.union(new_refs))
                
                batch.update(existing_tag.reference, {
                    'turn_refs': [{'turn_ref': ref} for ref in updated_refs]
                })
                logging.info(f"Queued update for existing tag: {key_term}")
            else:
                # Create new tag document
                new_tag_ref = tags_collection.document()
                batch.set(new_tag_ref, {
                    'term': key_term,
                    'turn_refs': [{'turn_ref': ref} for ref in turn_refs]
                })
                logging.info(f"Queued creation of new tag: {key_term}")
        except Exception as e:
            logging.error(f"Error processing tag {key_term}: {str(e)}")
    
    # Commit the batch
    try:
        batch.commit()
        logging.info("Successfully committed all tag updates")
    except Exception as e:
        logging.error(f"Error committing batch: {str(e)}")

    logging.info("Finished updating tags collection")

def generate_tag_info(tags: List[BaseModel]) -> List[Dict[str, Any]]:
    """
    Retrieves information about tags, including their turn index.
    """
    return [tag.model_dump() for tag in tags]

def update_tags_after_sectioning(transcript_id: str, sections: List[Dict[str, Any]]) -> None:
    db = get_firestore_client()
    tags_collection = db.collection('tags')
    
    # Create a mapping of old turn indices to new turn indices
    turn_mapping = {}
    new_index = 0
    for section in sections:
        for old_index in range(section['start_turn'], section['end_turn'] + 1):
            turn_mapping[old_index] = new_index
            new_index += 1
    
    # Update all tags
    tags = tags_collection.stream()
    batch = db.batch()
    
    for tag in tags:
        tag_data = tag.to_dict()
        updated_refs = []
        for ref in tag_data['turn_refs']:
            old_turn_index = int(ref['turn_ref'].id.split('_')[1])
            if old_turn_index in turn_mapping:
                new_turn_index = turn_mapping[old_turn_index]
                new_ref = db.collection('transcripts').document(transcript_id).collection('turns').document(f'turn_{new_turn_index}')
                updated_refs.append({'turn_ref': new_ref, 'context': ref.get('context', {})})
        
        if updated_refs:
            batch.update(tag.reference, {'turn_refs': updated_refs})
    
    batch.commit()
    logging.info(f"Updated tags for transcript {transcript_id} after sectioning")

def process_transcript_tags(transcript_id: str, generate_tag_context_func: Callable) -> None:
    db = get_firestore_client()
    tags_collection = db.collection('tags')
    transcript_ref = db.collection('transcripts').document(transcript_id)

    # Get all tags that reference this transcript
    tags = tags_collection.where('turn_refs', 'array_contains', transcript_ref).stream()

    for tag in tags:
        tag_data = tag.to_dict()
        tag_term = tag_data['term']
        updated_turn_refs = []

        for turn_ref in tag_data['turn_refs']:
            if turn_ref.parent.parent == transcript_ref:  # Check if the turn belongs to this transcript
                turn_doc = turn_ref.get()
                turn_data = turn_doc.to_dict()
                turn_content = turn_data.get('content', '')

                # Generate tag context
                tag_context = generate_tag_context_func(tag_term, turn_content)

                # Update the turn document with the tag context
                turn_ref.update({
                    'tag_contexts': {
                        tag_term: tag_context.model_dump()
                    }
                })

                # Create a new structure for the turn reference in the tag document
                updated_turn_refs.append({
                    'turn_ref': turn_ref,
                    'context': tag_context.model_dump()
                })

        # Update the tag document with the new turn references structure
        tag.reference.update({
            'turn_refs': updated_turn_refs
        })
        
        logging.info(f"Processed tag '{tag_term}' for transcript {transcript_id}")

    logging.info(f"Completed processing all tags for transcript {transcript_id}")