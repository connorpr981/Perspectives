from firebase_functions import https_fn
from firebase_admin import initialize_app

from _prompting.sectioning import get_sections
from _scripts.transcript_processing import (
    create_firestore_transcript, 
    get_transcript_data, 
    update_firestore_with_sections
)
from _utils.storage_utils import read_json_from_storage

app = initialize_app()

@https_fn.on_request()
def read_transcript_from_storage(req: https_fn.Request) -> https_fn.Response:
    filename = req.args.get("filename")
    if not filename:
        return https_fn.Response("No filename provided", status=400)

    try:
        transcript_data = read_json_from_storage("perspectives-f2e80.appspot.com", f"sample/{filename}")
        transcript_id = create_firestore_transcript(transcript_data, filename)
        return https_fn.Response(f"Transcript created with ID: {transcript_id}")
    except Exception as e:
        return https_fn.Response(f"Error creating transcript: {str(e)}", status=500)

@https_fn.on_request()
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
        return https_fn.Response(f"Error generating transcript sections: {str(e)}", status=500)