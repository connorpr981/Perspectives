import argparse
import requests
import google.auth
import google.auth.transport.requests
from google.oauth2 import id_token
import traceback
import os
import random
import json

# Update this with your Firebase project ID
PROJECT_ID = "perspectives-f2e80"

# Global variables for credentials and token
credentials, project = google.auth.default(
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

def get_id_token(audience):
    auth_req = google.auth.transport.requests.Request()
    token = id_token.fetch_id_token(auth_req, audience)
    return token

def call_function(function_name, params=None):
    url = FUNCTION_URLS[function_name]
    try:
        id_token = get_id_token(url)
        print(f"Successfully obtained ID token")
    except Exception as e:
        print(f"Error obtaining ID token: {str(e)}")
        print(f"Credentials type: {type(credentials)}")
        print(f"Credentials valid: {credentials.valid}")
        print(f"Credentials expired: {credentials.expired}")
        raise

    print(f"Calling function: {function_name}")
    print(f"URL: {url}")
    print(f"ID Token (first 10 chars): {id_token[:10]}...")
    headers = {
        'Authorization': f'Bearer {id_token}',
        'Content-Type': 'application/json'
    }
    print(f"Request headers: {json.dumps(headers, indent=2)}")
    print(f"Request params: {json.dumps(params, indent=2)}")
    try:
        response = requests.post(url, headers=headers, json=params, timeout=600)
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text[:100]}...")
        print(f"Response headers: {json.dumps(dict(response.headers), indent=2)}")
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error calling function: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        raise

# Update the FUNCTION_URLS with your Cloud Run function URLs
FUNCTION_URLS = {
    "generate_transcript_sections": f"https://generate-transcript-sections-ylvzsbofdq-uc.a.run.app",
    "get_turn_tags": f"https://get-turn-tags-ylvzsbofdq-uc.a.run.app",
    "generate_tag_contexts": f"https://generate-tag-contexts-ylvzsbofdq-uc.a.run.app",
    "generate_transcript_enrichment_questions": f"https://generate-transcript-enrichment-questions-ylvzsbofdq-uc.a.run.app",
    "generate_transcript_reflective_questions": f"https://generate-transcript-reflective-questions-ylvzsbofdq-uc.a.run.app",
    "answer_enrichment_questions": f"https://answer-enrichment-questions-ylvzsbofdq-uc.a.run.app",
}

# Hardcoded transcript IDs
TRANSCRIPT_IDS = [
    "0hqmuLsuQfut6qsSpkET",
    "Gbc289GT8K8hZBOeMYfi",
    "KQ5TAb5DvNjzTjkUBTBx",
    "QjGRwgGV5R8APPlMZH4x",
    "ebd41bRiq56rwHGOMvNE"
]

def generate_sections(transcript_id):
    try:
        response = call_function("generate_transcript_sections", {"transcript_id": transcript_id})
        print(f"Sections generated for transcript {transcript_id}")
        return True
    except Exception as e:
        print(f"Error generating sections for transcript {transcript_id}: {str(e)}")
        return False

def generate_tags(transcript_id):
    try:
        response = call_function("get_turn_tags", {"transcript_id": transcript_id})
        print(f"Tags generated for transcript {transcript_id}")
    except Exception as e:
        print(f"Error generating tags for transcript {transcript_id}: {str(e)}")

def generate_tag_contexts(transcript_id):
    try:
        response = call_function("generate_tag_contexts", {"transcript_id": transcript_id})
        print(f"Tag contexts generated for transcript {transcript_id}")
    except Exception as e:
        print(f"Error generating tag contexts for transcript {transcript_id}: {str(e)}")

def generate_enrichment_questions(transcript_id):
    try:
        response = call_function("generate_transcript_enrichment_questions", {"transcript_id": transcript_id})
        print(f"Enrichment questions generated for transcript {transcript_id}")
    except Exception as e:
        print(f"Error generating enrichment questions for transcript {transcript_id}: {str(e)}")

def generate_reflective_questions(transcript_id):
    try:
        response = call_function("generate_transcript_reflective_questions", {"transcript_id": transcript_id})
        print(f"Reflective questions generated for transcript {transcript_id}")
    except Exception as e:
        print(f"Error generating reflective questions for transcript {transcript_id}: {str(e)}")

def answer_enrichment_questions(transcript_id):
    try:
        response = call_function("answer_enrichment_questions", {"transcript_id": transcript_id})
        print(f"Enrichment questions answered for transcript {transcript_id}")
        return True
    except Exception as e:
        print(f"Error answering enrichment questions for transcript {transcript_id}: {str(e)}")
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

def main():
    parser = argparse.ArgumentParser(description="Process transcripts, generate sections, tags, tag contexts, and questions")
    parser.add_argument("--section", action="store_true", help="Generate sections for transcripts")
    parser.add_argument("--tag", action="store_true", help="Generate tags for transcripts")
    parser.add_argument("--context", action="store_true", help="Generate tag contexts for transcripts")
    parser.add_argument("--enrichment_question", action="store_true", help="Generate enrichment questions for transcripts")
    parser.add_argument("--reflective_question", action="store_true", help="Generate reflective questions for transcripts")
    parser.add_argument("--all", action="store_true", help="Process all transcripts instead of just one")
    parser.add_argument("--answer_enrichment", action="store_true", help="Answer enrichment questions for transcripts")
    args = parser.parse_args()

    if not (args.section or args.tag or args.context or args.enrichment_question or args.reflective_question or args.answer_enrichment):
        parser.error("At least one of --section, --tag, --context, --enrichment_question, --reflective_question, or --answer_enrichment must be specified")

    transcript_ids = TRANSCRIPT_IDS.copy()
    
    if not args.all:
        transcript_ids = [random.choice(transcript_ids)]
    else:
        print("Shuffling transcript order...")
        random.shuffle(transcript_ids)
    
    for transcript_id in transcript_ids:
        process_transcript(transcript_id, args)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        print(traceback.format_exc())