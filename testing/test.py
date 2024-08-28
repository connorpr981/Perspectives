import argparse
import requests
from google.cloud import firestore
import traceback
import os
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "http://127.0.0.1:5001/perspectives-f2e80/us-central1"
TRANSCRIPTS = [
    "dwarkesh_zuck.json",
    "dwarkesh_fchollet.json",
    "dwarkesh_pcollison.json",
    "dwarkesh_patio11.json",
    "dwarkesh_tonyblair.json"
]

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
db = firestore.Client(project="perspectives-f2e80")

def read_transcript(filename):
    url = f"{BASE_URL}/read_transcript_from_storage?filename={filename}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.split(": ")[-1].strip()
    else:
        print(f"Error reading transcript {filename}: {response.text}")
        return None

def is_transcript_sectioned(transcript_id):
    doc_ref = db.collection("transcripts").document(transcript_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get('sectioned', False)
    return False

def is_transcript_tagged(transcript_id):
    doc_ref = db.collection("transcripts").document(transcript_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get('tagged', False)
    return False

def generate_sections(transcript_id):
    if is_transcript_sectioned(transcript_id):
        print(f"Transcript {transcript_id} is already sectioned. Skipping.")
        return False

    url = f"{BASE_URL}/generate_transcript_sections?transcript_id={transcript_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"Sections generated for transcript {transcript_id}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error generating sections for transcript {transcript_id}: {str(e)}")
        return False

def generate_tags(transcript_id):
    if is_transcript_tagged(transcript_id):
        print(f"Transcript {transcript_id} is already tagged. Skipping.")
        return

    url = f"{BASE_URL}/get_turn_tags?transcript_id={transcript_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"Tags generated for transcript {transcript_id}")
    except requests.exceptions.RequestException as e:
        print(f"Error generating tags for transcript {transcript_id}: {str(e)}")

def generate_tag_contexts(transcript_id):
    url = f"{BASE_URL}/generate_tag_contexts?transcript_id={transcript_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"Tag contexts generated for transcript {transcript_id}")
    except requests.exceptions.RequestException as e:
        print(f"Error generating tag contexts for transcript {transcript_id}: {str(e)}")

def generate_enrichment_questions(transcript_id):
    url = f"{BASE_URL}/generate_transcript_enrichment_questions?transcript_id={transcript_id}"
    try:
        print(f"Sending request to generate enrichment questions for transcript {transcript_id}")
        print(f"URL: {url}")
        response = requests.get(url, timeout=600)  # 10-minute timeout
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text}")
        response.raise_for_status()
        print(f"Enrichment questions generated for transcript {transcript_id}")
    except requests.exceptions.RequestException as e:
        print(f"Error generating enrichment questions for transcript {transcript_id}: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response content: {e.response.text}")
        else:
            print("No response content available")

def generate_reflective_questions(transcript_id):
    url = f"{BASE_URL}/generate_transcript_reflective_questions?transcript_id={transcript_id}"
    try:
        print(f"Sending request to generate reflective questions for transcript {transcript_id}")
        print(f"URL: {url}")
        response = requests.get(url, timeout=600)  # 10-minute timeout
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text}")
        response.raise_for_status()
        print(f"Reflective questions generated for transcript {transcript_id}")
    except requests.exceptions.RequestException as e:
        print(f"Error generating reflective questions for transcript {transcript_id}: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response content: {e.response.text}")
        else:
            print("No response content available")

def print_questions(transcript_id):
    db = firestore.Client()
    transcript_ref = db.collection('transcripts').document(transcript_id)
    sections = transcript_ref.collection('sections').stream()

    for section in sections:
        print(f"\nSection: {section.id}")
        questions = section.reference.collection('questions').stream()
        for question in questions:
            q_data = question.to_dict()
            print(f"Turn {q_data['turn_index']} - {q_data['type'].capitalize()}: {q_data['question']}")
            if q_data['type'] == 'enrichment':
                print(f"  Information Type: {q_data['information_type']}")
                print(f"  Requires Current Info: {q_data['requires_current_info']}")
            elif q_data['type'] == 'reflective':
                print(f"  Perspectives: {', '.join(q_data['perspectives'])}")

def get_transcript_ids_from_firestore():
    transcripts_ref = db.collection("transcripts")
    docs = transcripts_ref.stream()
    return [doc.id for doc in docs]

def print_firestore_data():
    print("Printing Firestore data:")
    docs = db.collection("transcripts").get()
    if not docs:
        print("No documents found in 'transcripts' collection.")
    for doc in docs:
        print(f"Document ID: {doc.id}")
        print(f"Document data: {doc.to_dict()}")
        
        # Print turns and their tags, ordered by index
        turns = doc.reference.collection('turns').order_by('index').stream()
        for turn in turns:
            turn_data = turn.to_dict()
            print(f"  Turn {turn_data['index']}: {turn_data.get('action', 'No action')}")
        
        print("---")

def answer_enrichment_questions(transcript_id):
    url = f"{BASE_URL}/answer_enrichment_questions?transcript_id={transcript_id}"
    try:
        print(f"Sending request to answer enrichment questions for transcript {transcript_id}")
        print(f"URL: {url}")
        response = requests.get(url, timeout=600)  # 10-minute timeout
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text}")
        response.raise_for_status()
        print(f"Enrichment questions answered for transcript {transcript_id}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error answering enrichment questions for transcript {transcript_id}: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response content: {e.response.text}")
        else:
            print("No response content available")
        return False

def process_transcript(transcript_id, args):
    if args.section:
        generate_sections(transcript_id)
    if args.tag:
        generate_tags(transcript_id)
    if args.context:
        generate_tag_contexts(transcript_id)
    if args.enrichment_question:
        generate_enrichment_questions(transcript_id)
    if args.reflective_question:
        generate_reflective_questions(transcript_id)
    if args.answer_enrichment:
        print(f"Attempting to answer enrichment questions for transcript {transcript_id}")
        success = answer_enrichment_questions(transcript_id)
        if success:
            print(f"Successfully answered enrichment questions for transcript {transcript_id}")
        else:
            print(f"Failed to answer enrichment questions for transcript {transcript_id}")
    if args.print_questions:
        print_questions(transcript_id)

def main():
    parser = argparse.ArgumentParser(description="Process transcripts, generate sections, tags, tag contexts, and questions")
    parser.add_argument("--read", action="store_true", help="Read transcripts from storage")
    parser.add_argument("--section", action="store_true", help="Generate sections for transcripts")
    parser.add_argument("--tag", action="store_true", help="Generate tags for transcripts")
    parser.add_argument("--context", action="store_true", help="Generate tag contexts for transcripts")
    parser.add_argument("--enrichment_question", action="store_true", help="Generate enrichment questions for transcripts")
    parser.add_argument("--reflective_question", action="store_true", help="Generate reflective questions for transcripts")
    parser.add_argument("--print_questions", action="store_true", help="Print questions for transcripts")
    parser.add_argument("--print", action="store_true", help="Print Firestore data")
    parser.add_argument("--all", action="store_true", help="Process all transcripts instead of just one")
    parser.add_argument("--answer_enrichment", action="store_true", help="Answer enrichment questions for transcripts")
    args = parser.parse_args()

    if not (args.read or args.section or args.tag or args.context or args.enrichment_question or args.reflective_question or args.answer_enrichment or args.print_questions or args.print):
        parser.error("At least one of --read, --section, --tag, --context, --enrichment_question, --reflective_question, --answer_enrichment, --print_questions, or --print must be specified")

    transcript_ids = []

    if args.read:
        print("Reading transcripts from storage...")
        for filename in TRANSCRIPTS:
            transcript_id = read_transcript(filename)
            if transcript_id:
                transcript_ids.append(transcript_id)
        if not args.all:
            transcript_ids = [random.choice(transcript_ids)]

    if args.section or args.tag or args.context or args.enrichment_question or args.reflective_question or args.answer_enrichment or args.print_questions:
        if not transcript_ids:
            print("Fetching transcript IDs from Firestore...")
            transcript_ids = get_transcript_ids_from_firestore()
        
        if not args.all:
            transcript_ids = [random.choice(transcript_ids)]
        else:
            print("Shuffling transcript order...")
            random.shuffle(transcript_ids)
        
        if args.all:
            print(f"Processing all transcripts with 2 workers...")
            with ThreadPoolExecutor(max_workers=2) as executor:
                futures = [executor.submit(process_transcript, transcript_id, args) for transcript_id in transcript_ids]
                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        print(f"An error occurred while processing a transcript: {str(e)}")
        else:
            print(f"Processing one transcript...")
            process_transcript(transcript_ids[0], args)

    if args.print:
        print_firestore_data()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        print(traceback.format_exc())