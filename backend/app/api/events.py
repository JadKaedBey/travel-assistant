import csv
import requests
from dotenv import load_dotenv
from app.config import EVENTBRITE_API_KEY
from fastapi import APIRouter, HTTPException, Depends
from app.models.event_model import Event
from app.models.user_model import User
from typing import List

load_dotenv()

router = APIRouter()

# Base URL for Eventbrite API
EVENTBRITE_API_URL = "https://www.eventbriteapi.com/v3/events/search/"
PINNED_EVENTS_CSV = 'data/pinned_events.csv'

def query_eventbrite(city: str, date: str, keywords: List[str]) -> List[Event]:
    """Fetch events from Eventbrite API."""
    
    print(f"Querying Eventbrite: city={city}, date={date}, keywords={keywords}")
    
    params = {
        "location.address": city,
        "start_date.range_start": date,
        "start_date.range_end": date,  # If you want to limit it to a single day
        "q": " ".join(keywords),       # Concatenate keywords into a search query
        "sort_by": "date"              # Sort events by date (optional)
    }
    
    headers = {
        "Authorization": f"Bearer {EVENTBRITE_API_KEY}"
    }
    
    response = requests.get(EVENTBRITE_API_URL, params=params, headers=headers)
    
    if response.status_code != 200:
        print(f"Eventbrite API Error: {response.status_code}")
        return []
    
    # Parse event data
    events_data = response.json().get("events", [])
    events = []
    
    for event_data in events_data:
        event = Event(
            id=event_data.get("id"),
            name=event_data["name"]["text"],
            location=city,  # Event location set to the input city
            date=event_data["start"]["local"]
        )
        events.append(event)
    
    return events

# TODO: fix if city or date is None
def check_pinned_events(city, date):
    # Read from the pinned events CSV
    with open('app/data/events.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['city'].lower() == city.lower() and row['date'] == date:
                return row['event']
    return None

def get_events_with_priority(city: str, date: str) -> List[Event]:
    """Get events with pinned events prioritized."""
    # Load pinned events
    pinned_events = load_pinned_events()
    
    # Fetch events from Eventbrite (or other APIs)
    fetched_events = query_eventbrite(city, date, keywords=[])
    
    # Prioritize pinned events by adding them to the front
    all_events = pinned_events + [event for event in fetched_events if event.id not in [e.id for e in pinned_events]]
    
    return all_events

# Admin Functions:

def load_pinned_events() -> List[Event]:
    """Load pinned events from CSV."""
    pinned_events = []
    try:
        with open(PINNED_EVENTS_CSV, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                pinned_events.append(Event(**row))
    except FileNotFoundError:
        # If file not found, return an empty list
        pass
    return pinned_events

def save_pinned_event(event: Event):
    """Save a pinned event to CSV."""
    with open(PINNED_EVENTS_CSV, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=event.dict().keys())
        if csvfile.tell() == 0:
            writer.writeheader()  # Write header if file is empty
        writer.writerow(event.dict())
        
@router.post("/pin_event/")
def pin_event(event: Event, current_user: User = Depends()):
    """Allow admin users to pin an event."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You are not authorized to pin events.")
    
    # Check if the event is already pinned
    pinned_events = load_pinned_events()
    if any(e.id == event.id for e in pinned_events):
        raise HTTPException(status_code=400, detail="Event is already pinned.")
    
    # Save the pinned event
    save_pinned_event(event)
    return {"message": "Event pinned successfully", "event": event}