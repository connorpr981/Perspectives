from typing import Dict, Any, List
from _utils.firestore_utils import get_firestore_client, delete_collection, get_document, update_document, create_subcollection_document
import logging

def get_transcript_data(transcript_id: str) -> Dict[str, Any]:
    transcript_data = get_document('transcripts', transcript_id)
    db = get_firestore_client()
    turns = db.collection('transcripts').document(transcript_id).collection('turns').order_by('index').stream()
    transcript_data['turns'] = []
    for turn in turns:
        turn_data = turn.to_dict()
        sentences = turn.reference.collection('sentences').order_by('index').stream()
        turn_data['sentences'] = [sentence.to_dict() for sentence in sentences]
        transcript_data['turns'].append(turn_data)
    return transcript_data

def update_firestore_with_sections(transcript_id: str, sections: List[Dict[str, Any]]) -> None:
    db = get_firestore_client()
    transcript_ref = db.collection('transcripts').document(transcript_id)
    
    # Create a batch for efficient writes
    batch = db.batch()
    
    for section in sections:
        section_data = {
            'title': section['title'],
            'subtitle': section['subtitle'],
            'description': section['description'],
            'start_turn': section['start_turn'],
            'end_turn': section['end_turn']
        }
        section_ref = transcript_ref.collection('sections').document()
        batch.set(section_ref, section_data)
        
        # Process all turns within the section
        for turn_index in range(section['start_turn'], section['end_turn'] + 1):
            turn_query = transcript_ref.collection('turns').where('index', '==', turn_index)
            turn_docs = turn_query.get()
            
            if not turn_docs:
                logging.warning(f"Warning: Turn with index {turn_index} not found in transcript {transcript_id}")
                continue
            
            turn = turn_docs[0]
            turn_data = turn.to_dict()
            
            # Keep the original turn ID
            new_turn_ref = section_ref.collection('turns').document(turn.id)
            batch.set(new_turn_ref, turn_data)
            
            sentences = turn.reference.collection('sentences').stream()
            for sentence in sentences:
                sentence_data = sentence.to_dict()
                new_sentence_ref = new_turn_ref.collection('sentences').document(sentence.id)
                batch.set(new_sentence_ref, sentence_data)
            
            # Don't delete the original turn and sentences, we'll do that later
    
    # Update the transcript document
    batch.update(transcript_ref, {'sectioned': True})
    
    # Commit the batch
    batch.commit()
    
    # Now delete the old turns collection
    delete_collection(transcript_ref.collection('turns'))

def create_firestore_transcript(transcript_data: List[Dict[str, Any]], filename: str) -> str:
    db = get_firestore_client()
    
    transcript_ref = db.collection("transcripts").document()
    transcript_ref.set({
        "filename": filename,
        "num_turns": len(transcript_data)
    })

    for turn in transcript_data:
        turn_data = {
            "index": turn["index"],
            "role": turn["role"],
            "speaker": turn["speaker"],
            "start_time": turn["start_time"],
            "content": turn["content"]
        }
        turn_ref = transcript_ref.collection('turns').document()
        turn_ref.set(turn_data)

        for sentence in turn["sentences"]:
            turn_ref.collection('sentences').document().set(sentence)

    return transcript_ref.id

def update_firestore_with_tags(transcript_id: str, tags: List[Dict[str, Any]]) -> None:
    """
    Adds the tag (action and key_terms) to the firestore document for each turn and updates the 'tagged' flag.
    """
    db = get_firestore_client()
    transcript_ref = db.collection('transcripts').document(transcript_id)
    
    turns = transcript_ref.collection('turns').get()
    turn_dict = {turn.to_dict()['index']: turn.reference for turn in turns}
    
    for tag in tags:
        turn_index = tag.turn_index
        if turn_index not in turn_dict:
            logging.warning(f"Turn with index {turn_index} not found in transcript {transcript_id}")
            continue
        
        turn_ref = turn_dict[turn_index]
        
        try:
            turn_doc = turn_ref.get()
            if not turn_doc.exists:
                logging.warning(f"Turn document not found for index {turn_index} in transcript {transcript_id}")
                continue

            turn_data = turn_doc.to_dict()
            if turn_data is None:
                logging.warning(f"Turn data is None for index {turn_index} in transcript {transcript_id}")
                continue

            turn_data['action'] = tag.action
            turn_data['key_terms'] = tag.key_terms
            turn_ref.set(turn_data, merge=True)
        except Exception as e:
            logging.error(f"Error updating turn {turn_index} in transcript {transcript_id}: {str(e)}")
    
    try:
        update_document('transcripts', transcript_id, {'tagged': True})
    except Exception as e:
        logging.error(f"Error updating 'tagged' flag for transcript {transcript_id}: {str(e)}")

def find_turn_in_sections(transcript_ref, turn_id):
    print(f"Searching for turn {turn_id} in transcript {transcript_ref.id}")
    sections = transcript_ref.collection('sections').stream()
    for section in sections:
        print(f"Checking section {section.id}")
        turn_ref = section.reference.collection('turns').document(turn_id)
        turn_doc = turn_ref.get()
        if turn_doc.exists:
            print(f"Found turn {turn_id} in section {section.id}")
            return turn_doc.to_dict(), section.id
    print(f"Turn {turn_id} not found in any section of transcript {transcript_ref.id}")
    return None, None

def verify_transcript_structure(transcript_id: str):
    db = get_firestore_client()
    transcript_ref = db.collection('transcripts').document(transcript_id)
    
    logging.info(f"Verifying structure for transcript {transcript_id}")
    
    sections = transcript_ref.collection('sections').stream()
    section_count = 0
    total_turns = 0
    
    for section in sections:
        section_count += 1
        section_data = section.to_dict()
        logging.info(f"Section {section.id}:")
        logging.info(f"  Title: {section_data.get('title', 'N/A')}")
        logging.info(f"  Start Turn: {section_data.get('start_turn', 'N/A')}")
        logging.info(f"  End Turn: {section_data.get('end_turn', 'N/A')}")
        
        turns = section.reference.collection('turns').stream()
        turn_count = 0
        for turn in turns:
            turn_count += 1
            turn_data = turn.to_dict()
            logging.info(f"  Turn {turn.id}:")
            logging.info(f"    index: {turn_data.get('index', 'N/A')}")
            logging.info(f"    role: {turn_data.get('role', 'N/A')}")
            logging.info(f"    speaker: {turn_data.get('speaker', 'N/A')}")
        
        logging.info(f"  Total turns in section: {turn_count}")
        total_turns += turn_count
    
    logging.info(f"Total sections in transcript: {section_count}")
    logging.info(f"Total turns across all sections: {total_turns}")