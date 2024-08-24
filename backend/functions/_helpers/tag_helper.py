from typing import List, Dict, Any
from google.cloud.firestore_v1.document import DocumentReference
from pydantic import BaseModel
from _utils.firestore_utils import get_firestore_client

def create_tag_index(tags: List[BaseModel], transcript_id: str) -> Dict[str, List[DocumentReference]]:
    """
    Creates a dictionary where keys are unique key terms and values are lists of turn references where they appear.
    
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
        
        for key_term in tag_dict['key_terms']:
            if key_term not in tag_index:
                tag_index[key_term] = []
            tag_index[key_term].append(turn_ref)
    
    return tag_index

def create_tags_collection(tag_index: Dict[str, List[DocumentReference]]) -> None:
    """
    Creates a new 'tags' collection in Firestore with tag documents containing turn references.
    
    :param tag_index: Dictionary mapping key terms to lists of turn references
    """
    db = get_firestore_client()
    tags_collection = db.collection('tags')
    
    for key_term, turn_refs in tag_index.items():
        tag_doc = tags_collection.document()
        tag_doc.set({
            'term': key_term,
            'turn_refs': turn_refs
        })

def generate_tag_info(tags: List[BaseModel]) -> List[Dict[str, Any]]:
    """
    Retrieves information about tags, including their turn index.
    """
    return [tag.model_dump() for tag in tags]