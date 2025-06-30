import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv


load_dotenv()
# print(os.getenv("GRPC_DNS_RESOLVER")) 


cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()