import logging
from firebase_functions import https_fn
from firebase_admin import initialize_app
import traceback

from _utils.storage_utils import read_json_from_storage
from _utils.firestore_utils import print_firestore_data, print_all_tags

from _prompting.tagging import get_tags
from _prompting.sectioning import get_sections
from _prompting.researching import generate_tag_relevance

from _helpers.transcript_helper import (
    create_firestore_transcript, 
    get_transcript_data, 
    update_firestore_with_sections, 
    update_firestore_with_tags,
    verify_transcript_structure
)
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