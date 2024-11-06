# Preliminary model
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Event(BaseModel):
    id: str                      # Unique identifier for the event (could be from Eventbrite or your system)
    name: str                    # Event name
    description: Optional[str]    # A brief description of the event
    location: str                # Location (could be a city or venue)
    date: Optional[datetime]      # Date and time of the event
    category: Optional[str]       # Category of the event (e.g., concert, exhibition, conference)
    url: Optional[str]            # Link to the event (e.g., on Eventbrite)
    priority: Optional[int] = 0   # Priority level (for pinned events, this could be set by an admin)
    pinned: Optional[bool] = False  # Whether the event has been pinned by an admin
