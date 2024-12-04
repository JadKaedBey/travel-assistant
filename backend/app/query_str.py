from datetime import datetime

from app.models.event_model import Event

def generate_ai_style_response(events: list[Event], weather: str) -> str:
  # Sort events by priority and pinned status
  sorted_events = sorted(events, key=lambda x: (-x.pinned, -x.priority, x.date or datetime.max))
  
  # Start the response with the weather
  response = f"The weather for the day is expected to be: {weather}.\n\n"
  
  # Check if there are any events
  if not sorted_events:
    response += "It seems like there are no events scheduled for now. Maybe take the opportunity to relax or explore something spontaneous!"
  else:
    response += "Here are some events you might enjoy:\n"
    for event in sorted_events:
      event_date = (
        f" on {event.date.strftime('%A, %B %d at %I:%M %p')}" if event.date else ""
      )
      description = ""
      
      if event.description:
        description = f" - {description}"
      
      response += f"- **{event.name}** at {event.location}{event_date}{description}\n"
  return response.strip()