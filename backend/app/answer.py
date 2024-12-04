from typing import Any
from typing_extensions import TypedDict
from app.models.event_model import Event

class Answer(TypedDict):
  events: list[Event]
  weather: str
  pois: list[dict[str, Any]]
  unesco_sites: list[str]
  hotels_motels: list[str]
  historic_places: list[str]
