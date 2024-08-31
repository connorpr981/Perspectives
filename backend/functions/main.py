import logging
from firebase_functions import https_fn
from firebase_admin import initialize_app
import traceback

from _utils.storage_utils import read_json_from_storage
from _utils.firestore_utils import print_firestore_data

from _prompting.tagging import get_tags
from _prompting.sectioning import get_sections
from _prompting.researching import generate_tag_relevance
from _prompting.enrichment_questioning import get_enrichment_questions
from _prompting.reflective_questioning import get_reflective_questions
from _prompting.enrichment_answering import simulate_answering_enrichment_questions

from _helpers.transcript_helper import (
    create_firestore_transcript, 
    get_transcript_data, 
    update_firestore_with_sections, 
    update_firestore_with_tags
)
from _helpers.question_helper import verify_transcript_structure
from _helpers.tag_helper import create_tag_index, create_tags_collection, process_transcript_tags

app = initialize_app()

# Configure logging
logging.basicConfig(level=logging.INFO)

@https_fn.on_request()
def read_transcript_from_storage(req: https_fn.Request) -> https_fn.Response:
    filename = req.args.get("filename")
    if not filename:
        return https_fn.Response("No filename provided", status=400)

    try:
        transcript_data = read_json_from_storage("perspectives-f2e80.appspot.com", f"sample/{filename}")
        transcript_id = create_firestore_transcript(transcript_data, filename)
        logging.info(f"Transcript created with ID: {transcript_id}")
        print_firestore_data()
        return https_fn.Response(f"Transcript created with ID: {transcript_id}")
    except Exception as e:
        error_message = f"Error creating transcript: {str(e)}\n{traceback.format_exc()}"
        logging.error(error_message)
        return https_fn.Response(error_message, status=500)

@https_fn.on_request(timeout_sec=540)
def get_turn_tags(req: https_fn.Request) -> https_fn.Response:
    transcript_id = req.args.get("transcript_id")
    if not transcript_id:
        return https_fn.Response("No transcript ID provided", status=400)
    
    try:
        logging.info(f"Starting tag generation for transcript {transcript_id}")
        transcript_data = get_transcript_data(transcript_id)
        tags = get_tags(transcript_data)
        tag_index = create_tag_index(tags, transcript_id)
        update_firestore_with_tags(transcript_id, tags)
        create_tags_collection(tag_index, transcript_id)  # Add transcript_id here
        logging.info(f"Completed tag generation for transcript {transcript_id}")
        return https_fn.Response(f"Transcript tags processed and tags collection updated for ID: {transcript_id}")
    except Exception as e:
        error_message = f"Error processing transcript tags: {str(e)}\n{traceback.format_exc()}"
        logging.error(error_message)
        return https_fn.Response(error_message, status=500)

@https_fn.on_request(timeout_sec=540)
def generate_transcript_sections(req: https_fn.Request) -> https_fn.Response:
    transcript_id = req.args.get("transcript_id")
    if not transcript_id:
        return https_fn.Response("No transcript ID provided", status=400)
    
    try:
        logging.info(f"Starting section generation for transcript {transcript_id}")
        transcript_data = get_transcript_data(transcript_id)
        sections = get_sections(transcript_data)
        update_firestore_with_sections(transcript_id, sections)
        logging.info(f"Completed section generation for transcript {transcript_id}")
        return https_fn.Response(f"Transcript sections generated for ID: {transcript_id}")
    except Exception as e:
        error_message = f"Error generating transcript sections: {str(e)}\n{traceback.format_exc()}"
        logging.error(error_message)
        return https_fn.Response(error_message, status=500)

@https_fn.on_request(timeout_sec=540)
def generate_tag_contexts(req: https_fn.Request) -> https_fn.Response:
    transcript_id = req.args.get("transcript_id")
    if not transcript_id:
        return https_fn.Response("No transcript ID provided", status=400)
    
    try:
        logging.info(f"Starting tag context generation for transcript {transcript_id}")
        
        verify_transcript_structure(transcript_id)
        
        process_transcript_tags(transcript_id, generate_tag_relevance)
        logging.info(f"Completed tag context generation for transcript {transcript_id}")
        return https_fn.Response(f"Tag contexts generated for transcript ID: {transcript_id}")
    except Exception as e:
        error_message = f"Error generating tag contexts: {str(e)}\n{traceback.format_exc()}"
        logging.error(error_message)
        return https_fn.Response(error_message, status=500)

@https_fn.on_request(timeout_sec=540)
def generate_transcript_enrichment_questions(req: https_fn.Request) -> https_fn.Response:
    transcript_id = req.args.get("transcript_id")
    test_mode = req.args.get("test_mode", "false").lower() == "true"
    logging.info(f"Received request to generate enrichment questions for transcript {transcript_id}")
    logging.info(f"Test mode: {test_mode}")
    
    if not transcript_id:
        logging.error("No transcript ID provided")
        return https_fn.Response("No transcript ID provided", status=400)
    
    try:
        enrichment_questions = get_enrichment_questions(transcript_id, test_mode=test_mode)
        return https_fn.Response(f"Transcript enrichment questions generated for ID: {transcript_id}")
    except Exception as e:
        error_message = f"Error generating transcript enrichment questions: {str(e)}\n{traceback.format_exc()}"
        logging.error(error_message)
        return https_fn.Response(error_message, status=500)

@https_fn.on_request(timeout_sec=540)
def generate_transcript_reflective_questions(req: https_fn.Request) -> https_fn.Response:
    transcript_id = req.args.get("transcript_id")
    test_mode = req.args.get("test_mode", "false").lower() == "true"
    logging.info(f"Received request to generate reflective questions for transcript {transcript_id}")
    logging.info(f"Test mode: {test_mode}")
    
    if not transcript_id:
        logging.error("No transcript ID provided")
        return https_fn.Response("No transcript ID provided", status=400)
    
    try:
        reflective_questions = get_reflective_questions(transcript_id, test_mode=test_mode)
        return https_fn.Response(f"Transcript reflective questions generated for ID: {transcript_id}")
    except Exception as e:
        error_message = f"Error generating transcript reflective questions: {str(e)}\n{traceback.format_exc()}"
        logging.error(error_message)
        return https_fn.Response(error_message, status=500)

@https_fn.on_request(timeout_sec=540)
def answer_enrichment_questions(req: https_fn.Request) -> https_fn.Response:
    try:
        transcript_id = req.args.get('transcript_id')
        if not transcript_id:
            return https_fn.Response("Missing transcript_id parameter", status=400)
        
        simulate_answering_enrichment_questions(transcript_id)
        return https_fn.Response("Enrichment questions answered successfully")
    except Exception as e:
        logging.error(f"Error answering enrichment questions: {str(e)}")
        return https_fn.Response(f"Error: {str(e)}", status=500)