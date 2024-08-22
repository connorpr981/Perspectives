import os
from google.cloud import firestore
from typing import Any, Dict, List

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