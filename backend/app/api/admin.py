import csv
from fastapi import APIRouter
from typing import List
from app.models.event_model import Event
from app.models.location_model import Location

router = APIRouter()

# Define file paths for pinned data
PINNED_EVENTS_CSV = '../data/pinned_events.csv'
PINNED_LOCATIONS_CSV = '../data/pinned_locations.csv'

# Helper functions
def save_to_csv(file_path: str, fieldnames: List[str], data: dict):
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

@router.post("/admin/pin_event")
def pin_event(event: Event):
    """Pin an event to prioritize it for suggestions."""
    event_data = event.dict()
    save_to_csv(PINNED_EVENTS_CSV, fieldnames=event_data.keys(), data=event_data)
    return {"message": "Event pinned successfully", "event": event_data}

@router.post("/admin/pin_location")
def pin_location(location: Location):
    """Pin a location to prioritize it for suggestions."""
    location_data = location.dict()
    save_to_csv(PINNED_LOCATIONS_CSV, fieldnames=location_data.keys(), data=location_data)
    return {"message": "Location pinned successfully", "location": location_data}

@router.get("/admin/pinned_events")
def get_pinned_events():
    """Retrieve all pinned events."""
    pinned_events = read_from_csv(PINNED_EVENTS_CSV)
    print(pinned_events)
    return {"pinned_events": pinned_events}

@router.get("/admin/pinned_locations")
def get_pinned_locations():
    """Retrieve all pinned locations."""
    pinned_locations = read_from_csv(PINNED_LOCATIONS_CSV)
    return {"pinned_locations": pinned_locations}

@router.delete("/admin/unpin_event/{event_id}")
def unpin_event(event_id: str):
    """Unpin an event based on its ID."""
    delete_from_csv(PINNED_EVENTS_CSV, key="id", value=event_id)
    return {"message": f"Event with ID {event_id} unpinned successfully"}

@router.delete("/admin/unpin_location/{location_id}")
def unpin_location(location_id: str):
    """Unpin a location based on its ID."""
    delete_from_csv(PINNED_LOCATIONS_CSV, key="id", value=location_id)
    return {"message": f"Location with ID {location_id} unpinned successfully"}
