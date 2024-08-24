import logging
from firebase_functions import https_fn
from firebase_admin import initialize_app

from _utils.storage_utils import read_json_from_storage
from _utils.firestore_utils import print_firestore_data

from _prompting.tagging import get_tags
from _prompting.sectioning import get_sections

from _helpers.transcript_helper import create_firestore_transcript, get_transcript_data, update_firestore_with_sections, update_firestore_with_tags
from _helpers.tag_helper import create_tag_index, create_tags_collection, update_tags_after_sectioning

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
        print("Firestore data after creation:")
        print_firestore_data()
        return https_fn.Response(f"Transcript created with ID: {transcript_id}")
    except Exception as e:
        return https_fn.Response(f"Error creating transcript: {str(e)}", status=500)

@https_fn.on_request(
    timeout_sec=540
)
def get_turn_tags(req: https_fn.Request) -> https_fn.Response:
    """
    Generate tags for each turn in the transcript, update Firestore, and create/update the tags collection.
    """
    transcript_id = req.args.get("transcript_id")
    if not transcript_id:
        return https_fn.Response("No transcript ID provided", status=400)
    
    try:
        logging.info(f"Starting tag generation for transcript {transcript_id}")
        transcript_data = get_transcript_data(transcript_id)
        logging.info(f"Retrieved transcript data for {transcript_id}")
        
        tags = get_tags(transcript_data)
        logging.info(f"Generated {len(tags)} tags for transcript {transcript_id}")
        
        # Create tag index (now includes links and titles)
        tag_index = create_tag_index(tags, transcript_id)
        logging.info(f"Created tag index for transcript {transcript_id}")
        
        # Update Firestore with tags
        update_firestore_with_tags(transcript_id, tags)
        logging.info(f"Updated Firestore with tags for transcript {transcript_id}")
        
        # Create/update tags collection
        create_tags_collection(tag_index)
        logging.info(f"Updated tags collection for transcript {transcript_id}")
        
        return https_fn.Response(f"Transcript tags processed and tags collection updated for ID: {transcript_id}")
    except Exception as e:
        import traceback
        error_message = f"Error processing transcript tags: {str(e)}\n{traceback.format_exc()}"
        logging.error(error_message)
        return https_fn.Response(error_message, status=500)

@https_fn.on_request(
    timeout_sec=540
)
def generate_transcript_sections(req: https_fn.Request) -> https_fn.Response:
    transcript_id = req.args.get("transcript_id")
    if not transcript_id:
        return https_fn.Response("No transcript ID provided", status=400)
    
    try:
        transcript_data = get_transcript_data(transcript_id)
        sections = get_sections(transcript_data)
        update_firestore_with_sections(transcript_id, sections)
        
        # Update tags after sectioning
        update_tags_after_sectioning(transcript_id, sections)
        
        return https_fn.Response(f"Transcript sections generated and tags updated for ID: {transcript_id}")
    except Exception as e:
        import traceback
        error_message = f"Error generating transcript sections: {str(e)}\n{traceback.format_exc()}"
        print(error_message)
        return https_fn.Response(error_message, status=500)