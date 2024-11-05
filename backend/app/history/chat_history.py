from pymongo import MongoClient
from pymongo import ASCENDING
import datetime
from pydantic import BaseModel
from typing import List
from enum import StrEnum
import secrets
import string

# setup connection
client = MongoClient('mongodb://localhost:27017/')
db = client['chat_db']
chat_collection = db['chat_history']
chat_collection.create_index([("created_at", ASCENDING)], expireAfterSeconds=3600)

# models
class UserOrChatbot(StrEnum):
    USER                = "user"
    CHATBOT             = "chatbot"
class InsertMessage(BaseModel):
    session_id          : str
    user_or_chatbot     : UserOrChatbot
    message             : str
class RetrieveMessage(BaseModel):
    session_id          : str
    user_or_chatbot     : UserOrChatbot
    message             : str
    created_at          : datetime.datetime

# interaction functions
def add_message(message_info: InsertMessage):
    refresh_session(message_info.session_id)
    chat_message = {
        "session_id"        : message_info.session_id,
        "user_or_chatbot"   : message_info.user_or_chatbot,
        "message"           : message_info.message,
        "created_at"        : datetime.datetime.now(datetime.timezone.utc)
    }
    chat_collection.insert_one(chat_message)

def get_chat_history(
    session_id  : str, 
    limit       : int   = 4     # choose even so that user query always comes first
) -> List[RetrieveMessage]:
    refresh_session(session_id)
    items = chat_collection.find({"session_id": session_id}).sort("created_at", ASCENDING).limit(limit)
    return [RetrieveMessage(
        session_id          = item.session_id,
        user_or_chatbot     = item.user_or_chatbot,
        message             = item.message,
        created_at          = item.created_at
    ) for item in items]

def refresh_session(session_id: str):
    chat_collection.update_many(
        {"session_id": session_id},
        {"$set": {"created_at": datetime.datetime.now(datetime.timezone.utc)}}
    )

def find_session_id(session_id: str) -> bool:
    refresh_session(session_id)
    found = chat_collection.find_one({"session_id": session_id})
    return found != None

alphabet = string.ascii_letters + string.digits
def generate_session_id():
    possible_id = None
    while (possible_id == None or find_session_id(possible_id)):
        possible_id = ''.join(secrets.choice(alphabet) for _ in range(32))
    return possible_id
