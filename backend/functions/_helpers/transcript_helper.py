from typing import Dict, Any, List
from _utils.firestore_utils import get_firestore_client, delete_collection, get_document, update_document, create_subcollection_document

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
    
    for section in sections:
        # Create a new section document with start_turn and end_turn
        section_data = {
            'title': section['title'],
            'subtitle': section['subtitle'],
            'description': section['description'],
            'start_turn': section['start_turn'],
            'end_turn': section['end_turn']
        }
        section_id = create_subcollection_document('transcripts', transcript_id, 'sections', section_data)
        
        # Process all turns within the section
        for turn_index in range(section['start_turn'], section['end_turn'] + 1):
            turn_query = transcript_ref.collection('turns').where('index', '==', turn_index)
            turn_docs = turn_query.get()
            
            if not turn_docs:
                print(f"Warning: Turn with index {turn_index} not found in transcript {transcript_id}")
                continue
            
            turn = turn_docs[0]
            turn_data = turn.to_dict()
            new_turn_id = create_subcollection_document('transcripts', transcript_id, f'sections/{section_id}/turns', turn_data)
            
            sentences = turn.reference.collection('sentences').stream()
            for sentence in sentences:
                sentence_data = sentence.to_dict()
                create_subcollection_document('transcripts', transcript_id, f'sections/{section_id}/turns/{new_turn_id}/sentences', sentence_data)
                sentence.reference.delete()
            
            turn.reference.delete()
    
    delete_collection(transcript_ref.collection('turns'))
    update_document('transcripts', transcript_id, {'sectioned': True})

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
        turn_id = create_subcollection_document('transcripts', transcript_ref.id, 'turns', turn_data)

        for sentence in turn["sentences"]:
            create_subcollection_document('transcripts', transcript_ref.id, f'turns/{turn_id}/sentences', sentence)

    return transcript_ref.id

def update_firestore_with_tags(transcript_id: str, tags: List[Dict[str, Any]]) -> None:
    """
    Adds the tag (action, people, places, things) to the firestore document for each turn and updates the 'tagged' flag.
    """
    db = get_firestore_client()
    transcript_ref = db.collection('transcripts').document(transcript_id)
    
    for tag in tags:
        turn_index = tag.turn_index
        turn_ref = transcript_ref.collection('turns').where('index', '==', turn_index).stream()
        
        for turn in turn_ref:
            turn_data = turn.to_dict()
            turn_data['action'] = tag.action
            turn_data['people'] = tag.people
            turn_data['places'] = tag.places
            turn_data['things'] = tag.things
            update_document(f'transcripts/{transcript_id}/turns', turn.id, turn_data)
    
    # Update the 'tagged' flag in the main transcript document
    update_document('transcripts', transcript_id, {'tagged': True})