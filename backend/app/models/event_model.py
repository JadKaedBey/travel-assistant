# Preliminary model
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Event(BaseModel):
    id: str                           # Unique identifier for the event 
    name: str                         # Event name
    location: str                     # Location (could be a city or venue)
    description: Optional[str] = None # A brief description of the event
    date: Optional[datetime] = None   # Date and time of the event
    category: Optional[str] = None    # Category of the event (e.g., concert, exhibition, conference)
    url: Optional[str] = None         # Link to the event (e.g., on Eventbrite)
    priority: Optional[int] = 0       # Priority level (for pinned events, this could be set by an admin)
    pinned: Optional[bool] = False    # Whether the event has been pinned by an admin
