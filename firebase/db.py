import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from dotenv import load_dotenv

load_dotenv()

firebase_json = os.environ.get("FIREBASE_CREDENTIALS_JSON")
if not firebase_json:
    raise ValueError("FIREBASE_CREDENTIALS_JSON is not set in environment variables")

firebase_json = json.loads(firebase_json)
print(firebase_json)
cred = credentials.Certificate(firebase_json)
firebase_admin.initialize_app(cred)

db = firestore.client()

if __name__ == "__main__":
    print(db)