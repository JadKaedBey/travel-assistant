import csv
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv
from app.config import EVENTBRITE_API_KEY, TICKETMASTER_API_KEY
from fastapi import APIRouter, HTTPException, Depends
from app.models.event_model import Event
from app.models.user_model import User
import json
from app.dateparser import parse_date, get_start_end_date

load_dotenv()

router = APIRouter()

# Base URL for Eventbrite API
EVENTBRITE_API_URL = "https://www.eventbriteapi.com/v3/events/search/"
TICKETMASTER_API_URL = "https://app.ticketmaster.com/discovery/v2/events"
PINNED_EVENTS_PATH = 'app/data/pinned_events.json'
PINNED_LOCATIONS_PATH = 'app/data/pinned_locations.json'

def query_eventbrite(city: str, date: str, keywords: list[str]) -> list[Event]:
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
            
def query_ticketmaster(city: str, date: datetime.date, keywords: list[str]) -> list[Event]:
    """Fetch events from Ticketmaster API."""

    date, end_date = get_start_end_date(datetime.combine(date, datetime.min.time()))
    print(f"Querying Ticketmaster: city={city}, date={date}, endDate={end_date}, keywords={keywords}")

    params = {
        "keyword": " ".join(keywords),
        "city": f"{city}",
        "sort": "date,asc",
        "startDateTime": date + "+00:00",
        "endDateTime": end_date + "+00:00",
        "apikey": TICKETMASTER_API_KEY,
        "size": 5 #page size of the response
        }
    response = requests.get(TICKETMASTER_API_URL, params=params)
    if response.status_code != 200:
        print(f"TicketMaster API Error: {response.status_code} {response.text}")
        return []
    
    # Parse event data
    events_data = response.json().get("_embedded", {}).get("events", [])
    events = []
    
    for event_data in events_data:
        event = Event(
            id=event_data.get("id"),
            name=event_data.get("name"),
            location=city,  # Event location set to the input city
            url=event_data.get("url"),
            date=event_data["dates"]["start"]["localDate"],
            category = event_data.get("classifications", [])[0].get("segment", {}).get("name", "Unknown Category")
        )
        events.append(event)

    return events

def check_pinned_events(city: str = None, date: datetime.date = None, keywords: list[str] = None):
    """Check for pinned events and locations matching the given city, date, and keywords."""
    # Check in pinned events
    with open(PINNED_EVENTS_PATH, 'r', encoding='utf-8') as events_file:
        pinned_events = json.load(events_file).get('pinned_events', [])
        for event in pinned_events:
            if (
                (city is None or event['location'].lower() == city.lower()) and
                (date is None or parse_date(event['date']) == date) and
                (keywords is None or any(keyword.lower() in event.get('category', '').lower() for keyword in keywords))
            ):
                return {"type": "event", "data": event}

    # Check in pinned locations
    with open(PINNED_LOCATIONS_PATH, 'r', encoding='utf-8') as locations_file:
        pinned_locations = json.load(locations_file).get('pinned_locations', [])
        for location in pinned_locations:
            if city is None or location['city'].lower() == city.lower():
                return {"type": "location", "data": location}

    return None
