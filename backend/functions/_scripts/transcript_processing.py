from typing import Dict, Any, List
from _utils.firestore_utils import get_firestore_client, delete_collection, get_document, update_document, create_subcollection_document

def get_transcript_data(transcript_id: str) -> Dict[str, Any]:
    transcript_data = get_document('transcripts', transcript_id)
    db = get_firestore_client()
    turns = db.collection('transcripts').document(transcript_id).collection('turns').order_by('index').stream()
    transcript_data['turns'] = [turn.to_dict() for turn in turns]
    return transcript_data

def update_firestore_with_sections(transcript_id: str, sections: List[Dict[str, Any]]) -> None:
    db = get_firestore_client()
    transcript_ref = db.collection('transcripts').document(transcript_id)
    
    for section in sections:
        section_id = create_subcollection_document('transcripts', transcript_id, 'sections', section)
        
        turns = transcript_ref.collection('turns').where('index', '>=', section['start_turn']).where('index', '<=', section['end_turn']).stream()
        for turn in turns:
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