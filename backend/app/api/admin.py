# admin_routes.py
import os
import json
from datetime import datetime
from fastapi import APIRouter
from app.models.event_model import Event
from app.models.location_model import Location

# Create a router for admin endpoints
router = APIRouter(prefix="/admin", tags=["Admin"])

# file paths for pinned data
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # Go up one directory from the current file's location
PINNED_EVENTS_JSON = os.path.join(BASE_DIR, 'data', 'pinned_events.json')
PINNED_LOCATIONS_JSON = os.path.join(BASE_DIR, 'data', 'pinned_locations.json')


# Helper functions
def save_to_json(file_path: str, data: dict):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as jsonfile:
            file_data = json.load(jsonfile)
    else:
        file_data = {"pinned_events": []} if "events" in file_path else {"pinned_locations": []}

    key = "pinned_events" if "events" in file_path else "pinned_locations"
    file_data[key].append(data)

    with open(file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(file_data, jsonfile, indent=4, default=_datetime_handler)

def _datetime_handler(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def read_events_from_json(file_path: str):
    try:
        with open(file_path, 'r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)
            return data['pinned_events']
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def read_locations_from_json(file_path: str):
    try:
        with open(file_path, 'r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)
            return data['pinned_locations']
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def delete_from_json(file_path: str, key: str, value: str):
    if not os.path.exists(file_path):
        return

    with open(file_path, 'r', encoding='utf-8') as jsonfile:
        file_data = json.load(jsonfile)

    data_key = "pinned_events" if "events" in file_path else "pinned_locations"
    file_data[data_key] = [item for item in file_data[data_key] if item.get(key) != value]

    with open(file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(file_data, jsonfile, indent=4)

# Admin API Routes
@router.post("/pin_event")
def pin_event(event: Event):
    event_data = event.model_dump()
    save_to_json(PINNED_EVENTS_JSON, data=event_data)
    return {"message": "Event pinned successfully", "event": event_data}

@router.post("/pin_location")
def pin_location(location: Location):
    location_data = location.model_dump()
    save_to_json(PINNED_LOCATIONS_JSON, data=location_data)
    return {"message": "Location pinned successfully", "location": location_data}

@router.get("/pinned_events")
def get_pinned_events():
    pinned_events = read_events_from_json(PINNED_EVENTS_JSON)
    return {"pinned_events": pinned_events}

@router.get("/pinned_locations")
def get_pinned_locations():
    pinned_locations = read_locations_from_json(PINNED_LOCATIONS_JSON)
    return {"pinned_locations": pinned_locations}

@router.delete("/unpin_event/{event_id}")
def unpin_event(event_id: str):
    delete_from_json(PINNED_EVENTS_JSON, key="id", value=event_id)
    return {"message": f"Event with ID {event_id} unpinned successfully"}

@router.delete("/unpin_location/{location_id}")
def unpin_location(location_id: str):
    delete_from_json(PINNED_LOCATIONS_JSON, key="id", value=location_id)
    return {"message": f"Location with ID {location_id} unpinned successfully"}
