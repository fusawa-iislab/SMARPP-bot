from firebase.db import db

collections = db.collections()
for collection in collections:
    print(f"Collection: {collection.id}")
    docs = db.collection(collection.id).get()
    for doc in docs:
        print(f"Document ID: {doc.id}, Data: {doc.to_dict()}")
    print("\n")

# docs = db.collection("smarppbot_chatlog").stream()
# for doc in docs:
#     print(f"Deleting doc: {doc.id}")
#     doc.reference.delete()