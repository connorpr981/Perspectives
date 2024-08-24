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

def process_transcript(transcript_id, args):
    if args.section:
        generate_sections(transcript_id)
    if args.tag:
        generate_tags(transcript_id)

def main():
    parser = argparse.ArgumentParser(description="Process transcripts and generate sections")
    parser.add_argument("--read", action="store_true", help="Read transcripts from storage")
    parser.add_argument("--section", action="store_true", help="Generate sections for transcripts")
    parser.add_argument("--tag", action="store_true", help="Generate tags for transcripts")
    parser.add_argument("--print", action="store_true", help="Print Firestore data")
    parser.add_argument("--all", action="store_true", help="Process all transcripts instead of just one")
    args = parser.parse_args()

    if not (args.read or args.section or args.tag or args.print):
        parser.error("At least one of --read, --section, --tag, or --print must be specified")

    transcript_ids = []

    if args.read:
        print("Reading transcripts from storage...")
        for filename in TRANSCRIPTS:
            transcript_id = read_transcript(filename)
            if transcript_id:
                transcript_ids.append(transcript_id)
        if not args.all:
            transcript_ids = [random.choice(transcript_ids)]

    if args.section or args.tag:
        if not transcript_ids:
            print("Fetching transcript IDs from Firestore...")
            transcript_ids = get_transcript_ids_from_firestore()
        
        if not args.all:
            transcript_ids = [random.choice(transcript_ids)]
        else:
            print("Shuffling transcript order...")
            random.shuffle(transcript_ids)
        
        if args.all:
            print(f"Processing all transcripts with 5 workers...")
            with ThreadPoolExecutor(max_workers=5) as executor:
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