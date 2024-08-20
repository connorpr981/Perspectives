from google.cloud import storage
import json
from typing import Any, Dict, List

def get_storage_client():
    return storage.Client()

def read_json_from_storage(bucket_name: str, filename: str) -> List[Dict[str, Any]]:
    storage_client = get_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)
    json_string = blob.download_as_text()
    return json.loads(json_string)