import os
import json
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth, firestore

from dotenv import load_dotenv

load_dotenv()

sa_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT_JSON")
if not sa_json:
    raise RuntimeError("Please set FIREBASE_SERVICE_ACCOUNT_JSON env var")

# Allow FIREBASE_SERVICE_ACCOUNT_JSON to be either:
# - the full service account JSON text, or
# - a filesystem path to a JSON file (e.g. ./firebase.json or C:\path\to\firebase.json)
try:
    # If the value points to an existing file, read from it.
    if os.path.exists(sa_json):
        with open(sa_json, "r", encoding="utf-8") as f:
            sa_data = json.load(f)
    else:
        # Otherwise assume it's the JSON string itself
        sa_data = json.loads(sa_json)
except (json.JSONDecodeError, OSError) as e:
    raise RuntimeError(
        "FIREBASE_SERVICE_ACCOUNT_JSON is set but is not valid JSON and not a path to a readable file: "
        + str(e)
    )

cred = credentials.Certificate(sa_data)
firebase_admin.initialize_app(cred)
db = firestore.client()

# You can re-export firebase_auth if needed
auth = firebase_auth
