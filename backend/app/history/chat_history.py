"""
This file contains all the logic for communicating with the database with regard to chat history messages.
Chat messages are managed using a session key and set to expire after some time if not used.
Author: Ruben Vandamme
Date: 05 November 2024
Usage:
    - add_message           : save a message
    - get_chat_history      : get messages using a session key
    - (refresh_session)     : refresh messages TTL of a session
    - find_session_id       : check if a session id is present
    - generate_session_id   : generate an unique session id
"""

from typing_extensions import TypedDict
from pymongo import MongoClient
from pymongo import DESCENDING
import datetime
from bson.objectid import ObjectId
from pydantic import BaseModel
from enum import Enum
import os

# setup connection
client: MongoClient = MongoClient(os.getenv('MONGODB_URI', 'mongodb://127.0.0.1:27017/'))
db = client['chat_db']
chats_collection = db['chat_history']
chats_collection.create_index([("last_updated", DESCENDING)])

# models
class UserOrChatbot(Enum):
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

class ChatMessage(TypedDict):
    user_or_chatbot     : UserOrChatbot
    message             : str

class Chat(TypedDict):
    id: str
    last_updated: datetime.datetime
    messages: list[ChatMessage]

# Function to get all chat IDs
def get_all_chats():
    chats = chats_collection.find().sort("last_updated", DESCENDING)
    return [str(chat["_id"]) for chat in chats]

# Function to read an entire chat by ID
def read_entire_chat(chat_id: str) -> Chat | None:
    chat = chats_collection.find_one({"_id": ObjectId(chat_id)})
    if chat:
        return {"id": str(chat["_id"]), "messages": chat["messages"], "last_updated": chat["last_updated"]}
    else:
        return None


# Function to create a new chat and send the first message
def create_new_chat(message: str):
    chat = {
        "messages": [{"user_or_chatbot": "user", "message": message}],
        "last_updated": datetime.datetime.now(datetime.timezone.utc)
    }
    result = chats_collection.insert_one(chat)
    return str(result.inserted_id)

def add_message(message_info: InsertMessage):
    chat = chats_collection.find_one({"_id": ObjectId(message_info.session_id)})
    if chat:
        chats_collection.update_one(
            {"_id": ObjectId(message_info.session_id)},
            {
                "$push": {"messages": {"user_or_chatbot": message_info.user_or_chatbot, "message": message_info.message}},
                "$set": {"last_updated": datetime.datetime.now(datetime.timezone.utc)}
            }
        )
        return True
    else:
        return False
