from firebase_functions import https_fn
from firebase_admin import initialize_app

from _utils.storage_utils import read_json_from_storage
from _utils.firestore_utils import print_firestore_data

from _prompting.tagging import get_tags
from _prompting.sectioning import get_sections

from _helpers.transcript_helper import create_firestore_transcript, get_transcript_data, update_firestore_with_sections, update_firestore_with_tags

app = initialize_app()

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
    transcript_id = req.args.get("transcript_id")
    if not transcript_id:
        return https_fn.Response("No transcript ID provided", status=400)
    
    try:
        transcript_data = get_transcript_data(transcript_id)
        tags = get_tags(transcript_data)
        update_firestore_with_tags(transcript_id, tags)
        return https_fn.Response(f"Transcript tags created for ID: {transcript_id}")
    except Exception as e:
        import traceback
        error_message = f"Error getting transcript tags: {str(e)}\n{traceback.format_exc()}"
        print(error_message)  # This will log the full error trace
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
        return https_fn.Response(f"Transcript sections generated and updated for ID: {transcript_id}")
    except Exception as e:
        import traceback
        error_message = f"Error generating transcript sections: {str(e)}\n{traceback.format_exc()}"
        print(error_message)  # This will log the full error trace
        return https_fn.Response(error_message, status=500)