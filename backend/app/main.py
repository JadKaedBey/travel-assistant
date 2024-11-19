import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.history.chat_history import (
    find_session_id,
    generate_session_id
)
from app.query import run_query, QueryRequest

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Travel Assistant"}

# endpoint accepts a JSON body via Pydantic model
@app.post("/query/")
def process_query(query: QueryRequest):
    logger.info(f"Query: {query}")
    try:
        return run_query(query)

    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)  # Log the error details
        raise HTTPException(status_code=500, detail="Internal Server Error")


# session id logic
@app.get("/check-session-id/")
def check_session_id(session_id: str):
    return {"found": find_session_id(session_id)}

@app.post("/fresh-session-id/")
def fresh_session_id():
    return {"session_id": generate_session_id()}
