import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.history.chat_history import (
    Chat,
    get_all_chats,
    read_entire_chat
)
from app.api.admin import router as admin_router
from app.query import QueryResponse, run_query, QueryRequest
from app.models.event_model import Event
from app.models.location_model import Location

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin_router)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Travel Assistant"}

# endpoint accepts a JSON body via Pydantic model
@app.post("/query/")
def process_query(query: QueryRequest) -> QueryResponse:
    logger.info(f"Query: {query}")
    try:
        return run_query(query)

    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)  # Log the error details
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/get-chat/")
def get_chat(session_id: str) -> Chat | None:
    return read_entire_chat(session_id)

@app.get("/get-chats/")
def get_chats() -> list[str]:
    return get_all_chats()
