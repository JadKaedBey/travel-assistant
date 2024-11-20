import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.history.chat_history import (
    Chat,
    get_all_chats,
    read_entire_chat
)
from app.query import QueryResponse, run_query, QueryRequest

import csv
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



# Define file paths for pinned data
PINNED_EVENTS_CSV = './data/pinned_events.csv'
PINNED_LOCATIONS_CSV = './data/pinned_locations.csv'

# Helper functions
def save_to_csv(file_path: str, fieldnames: list[str], data: dict):
    """Helper function to save a row of data to a CSV file."""
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()  # Write header only if file is empty
        writer.writerow(data)

def read_from_csv(file_path: str):
    """Helper function to read all rows from a CSV file."""
    try:
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)
    except FileNotFoundError:
        return []

def delete_from_csv(file_path: str, key: str, value: str):
    """Helper function to delete a row from a CSV file based on a key-value match."""
    rows = read_from_csv(file_path)
    rows = [row for row in rows if row.get(key) != value]
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

# Admin API Routes

@app.post("/admin/pin_event")
def pin_event(event: Event):
    """Pin an event to prioritize it for suggestions."""
    print("hello there")
    event_data = event.model_dump()
    save_to_csv(PINNED_EVENTS_CSV, fieldnames=list(event_data.keys()), data=event_data)
    return {"message": "Event pinned successfully", "event": event_data}

@app.post("/admin/pin_location")
def pin_location(location: Location):
    """Pin a location to prioritize it for suggestions."""
    print("hello there2")
    location_data = location.model_dump()
    save_to_csv(PINNED_LOCATIONS_CSV, fieldnames=list(location_data.keys()), data=location_data)
    return {"message": "Location pinned successfully", "location": location_data}

@app.get("/admin/pinned_events")
def get_pinned_events():
    """Retrieve all pinned events."""
    print("get pins")
    pinned_events = read_from_csv(PINNED_EVENTS_CSV)
    print(pinned_events)
    return {"pinned_events": pinned_events}

@app.get("/admin/pinned_locations")
def get_pinned_locations():
    """Retrieve all pinned locations."""
    print("get pins loc")
    pinned_locations = read_from_csv(PINNED_LOCATIONS_CSV)
    return {"pinned_locations": pinned_locations}

@app.delete("/admin/unpin_event/{event_id}")
def unpin_event(event_id: str):
    """Unpin an event based on its ID."""
    delete_from_csv(PINNED_EVENTS_CSV, key="id", value=event_id)
    return {"message": f"Event with ID {event_id} unpinned successfully"}

@app.delete("/admin/unpin_location/{location_id}")
def unpin_location(location_id: str):
    """Unpin a location based on its ID."""
    delete_from_csv(PINNED_LOCATIONS_CSV, key="id", value=location_id)
    return {"message": f"Location with ID {location_id} unpinned successfully"}

