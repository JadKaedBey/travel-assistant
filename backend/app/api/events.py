import csv
import requests
from dotenv import load_dotenv
from app.config import EVENTBRITE_API_KEY
from fastapi import APIRouter, HTTPException, Depends
from app.models.event_model import Event
from app.models.user_model import User
from typing import List
import json

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

def check_pinned_events(city: str = None, date: str = None, keywords: list[str] = None):
    """Check for pinned events and locations matching the given city, date, and keywords."""
    # Check in pinned events
    with open('data/pinned_events.json', 'r', encoding='utf-8') as events_file:
        pinned_events = json.load(events_file).get('pinned_events', [])
        for event in pinned_events:
            if (
                (city is None or event['city'].lower() == city.lower()) and
                (date is None or event['date'] == date) and
                (keywords is None or any(keyword.lower() in event.get('category', '').lower() for keyword in keywords))
            ):
                return {"type": "event", "data": event}

    # Check in pinned locations
    with open('data/pinned_locations.json', 'r', encoding='utf-8') as locations_file:
        pinned_locations = json.load(locations_file).get('pinned_locations', [])
        for location in pinned_locations:
            if city is None or location['city'].lower() == city.lower():
                return {"type": "location", "data": location}

    return None
