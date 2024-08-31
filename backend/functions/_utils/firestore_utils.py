import os
import logging
from google.cloud import firestore
from typing import Any, Dict, List
from datetime import datetime

def get_firestore_client():
    if os.environ.get("FIRESTORE_EMULATOR_HOST"):
        return firestore.Client(project="perspectives-f2e80")
    return firestore.Client()

def delete_collection(collection_ref, batch_size=100):
    docs = collection_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        doc.reference.delete()
        deleted += 1

    if deleted >= batch_size:
        return delete_collection(collection_ref, batch_size)

def get_document(collection: str, doc_id: str) -> Dict[str, Any]:
    db = get_firestore_client()
    doc_ref = db.collection(collection).document(doc_id)
    doc = doc_ref.get()
    if not doc.exists:
        raise ValueError(f"Document with ID {doc_id} not found in {collection}")
    return doc.to_dict()

def update_document(collection: str, doc_id: str, data: Dict[str, Any]):
    db = get_firestore_client()
    db.collection(collection).document(doc_id).update(data)

def create_subcollection_document(parent_collection: str, parent_id: str, subcollection: str, data: Dict[str, Any]) -> str:
    db = get_firestore_client()
    doc_ref = db.collection(parent_collection).document(parent_id).collection(subcollection).document()
    doc_ref.set(data)
    return doc_ref.id

def print_firestore_data():
    print("Printing Firestore data:")
    db = get_firestore_client()
    docs = db.collection("transcripts").get()
    if not docs:
        print("No documents found in 'transcripts' collection.")
    for doc in docs:
        print(f"Document ID: {doc.id}")
        print(f"Document data: {doc.to_dict()}")
        print("---")

def update_or_create_tag(tag_term: str, turn_ids: List[str], transcript_id: str):
    db = get_firestore_client()
    tags_collection = db.collection('tags')
    
    existing_tag_query = tags_collection.where('term', '==', tag_term).limit(1)
    existing_tag_docs = existing_tag_query.get()
    
    current_time = datetime.utcnow()
    
    if existing_tag_docs:
        existing_tag = existing_tag_docs[0]
        existing_data = existing_tag.to_dict()
        existing_refs = {(ref['transcript_id'], ref['turn_id']) for ref in existing_data.get('turn_refs', [])}
        new_refs = {(transcript_id, turn_id) for turn_id in turn_ids}
        updated_refs = list(existing_refs.union(new_refs))
        
        existing_tag.reference.update({
            'turn_refs': [{'transcript_id': t_id, 'turn_id': turn_id} for t_id, turn_id in updated_refs],
            'last_updated': current_time
        })
    else:
        tags_collection.add({
            'term': tag_term,
            'turn_refs': [{'transcript_id': transcript_id, 'turn_id': turn_id} for turn_id in turn_ids],
            'last_updated': current_time
        })

def update_tag_context(tag_ref: firestore.DocumentReference, turn_id: str, context: str):
    logging.info(f"Entering update_tag_context for tag {tag_ref.id} and turn {turn_id}")
    tag_doc = tag_ref.get()
    logging.info(f"Tag document retrieved: {tag_doc.id}")
    tag_data = tag_doc.to_dict()
    turn_refs = tag_data.get('turn_refs', [])
    
    for turn_ref in turn_refs:
        if turn_ref['turn_id'] == turn_id:
            turn_ref['context'] = context
            break
    else:
        logging.warning(f"Turn ID {turn_id} not found in tag {tag_ref.id}")
        return

    logging.info(f"Updating tag {tag_ref.id} with new turn_refs")
    tag_ref.update({
        'turn_refs': turn_refs
    })
    logging.info(f"Tag {tag_ref.id} updated successfully")

def update_turn_tag_context(turn_ref: firestore.DocumentReference, tag_term: str, context: str):
    logging.info(f"Entering update_turn_tag_context for turn {turn_ref.id} and tag {tag_term}")
    turn_doc = turn_ref.get()
    logging.info(f"Turn document retrieved: {turn_doc.id}")
    turn_data = turn_doc.to_dict()
    current_tag_contexts = turn_data.get('tag_contexts', [])
    
    for tag_context in current_tag_contexts:
        if tag_context['term'] == tag_term:
            tag_context['context'] = context
            break
    else:
        current_tag_contexts.append({
            'term': tag_term,
            'context': context
        })
    
    logging.info(f"Updating turn {turn_ref.id} with new tag_contexts")
    turn_ref.update({
        'tag_contexts': current_tag_contexts
    })
    logging.info(f"Turn {turn_ref.id} updated successfully")

def print_all_tags():
    db = get_firestore_client()
    tags_collection = db.collection('tags')
    all_tags = tags_collection.stream()
    
    print("All tags in the collection:")
    tag_count = 0
    for tag in all_tags:
        tag_count += 1
        tag_data = tag.to_dict()
        print(f"Tag {tag_count}:")
        print(f"  ID: {tag.id}")
        print(f"  Term: {tag_data.get('term')}")
        print(f"  Turn refs: {tag_data.get('turn_refs')}")
        print("---")
    
    print(f"Total tags found: {tag_count}")