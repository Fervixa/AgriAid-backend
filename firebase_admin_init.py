import os
import json
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth, firestore

from dotenv import load_dotenv

load_dotenv()

sa_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT_JSON")
if not sa_json:
    raise RuntimeError("Please set FIREBASE_SERVICE_ACCOUNT_JSON env var")

cred = credentials.Certificate(json.loads(sa_json))
firebase_admin.initialize_app(cred)
db = firestore.client()

# You can re-export firebase_auth if needed
auth = firebase_auth
