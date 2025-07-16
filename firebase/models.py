from firebase.db import db
from pydantic import BaseModel, ValidationError
import logging

TABLE_NAMES = ["smarppbot_chatlog"]

class Chatlog(BaseModel):
    content: str
    timestamp: str
    is_bot: bool
    agent_id: str
    agent_name: str|None
    channel_id: str


def save_chatlog(chatlog: dict):
    v = Chatlog(**chatlog)
    doc_ref = db.collection("smarppbot_chatlog").add(chatlog)
    logging.info(f"Chatlog created: {doc_ref}")




