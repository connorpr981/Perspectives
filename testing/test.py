import argparse
import requests
import time
from google.cloud import firestore
import os

BASE_URL = "http://127.0.0.1:5001/perspectives-f2e80/us-central1"
TRANSCRIPTS = [
    "dwarkesh_zuck.json",
    "dwarkesh_fchollet.json",
    "dwarkesh_pcollison.json",
    "dwarkesh_patio11.json",
    "dwarkesh_tonyblair.json"
]

# Set up Firestore emulator
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

def generate_sections(transcript_id):
    url = f"{BASE_URL}/generate_transcript_sections?transcript_id={transcript_id}"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Sections generated for transcript {transcript_id}")
    else:
        print(f"Error generating sections for transcript {transcript_id}: {response.text}")

def get_transcript_ids_from_firestore():
    transcripts_ref = db.collection("transcripts")
    docs = transcripts_ref.stream()
    return [doc.id for doc in docs]

def main():
    parser = argparse.ArgumentParser(description="Process transcripts and generate sections")
    parser.add_argument("--read", action="store_true", help="Read transcripts from storage")
    parser.add_argument("--generate", action="store_true", help="Generate sections for transcripts")
    args = parser.parse_args()

    if not (args.read or args.generate):
        parser.error("At least one of --read or --generate must be specified")

    transcript_ids = []

    if args.read:
        print("Reading transcripts from storage...")
        for filename in TRANSCRIPTS:
            transcript_id = read_transcript(filename)
            if transcript_id:
                transcript_ids.append(transcript_id)
            time.sleep(1)  # Add a small delay between requests

    if args.generate:
        if not transcript_ids:
            print("Fetching transcript IDs from Firestore...")
            transcript_ids = get_transcript_ids_from_firestore()
        
        print("Generating sections for transcripts...")
        for transcript_id in transcript_ids:
            generate_sections(transcript_id)
            time.sleep(1)  # Add a small delay between requests

if __name__ == "__main__":
    main()