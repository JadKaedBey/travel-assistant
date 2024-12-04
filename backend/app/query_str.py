from datetime import datetime

from app.models.event_model import Event

def generate_ai_style_response(events: list[Event], weather: str) -> str:
  # Sort events by priority and pinned status
  sorted_events = sorted(events, key=lambda x: (-x.pinned, -x.priority, x.date or datetime.max))
  
  # Start the response with the weather
  response = ""
  if weather != "":
    response = f"{weather}\n\n"
  
  # Check if there are any events
  if not sorted_events:
      response += "#### It seems like there are no events scheduled for now. Maybe take the opportunity to relax or explore something spontaneous!"
  else:
      response += "### Here are some events you might enjoy:\n"
      for event in sorted_events:
          
          event_name = event.name  # Name is the minimal requirement for an event!

          event_description = None
          if event.description:
              event_description = f" - {event.description}"

          event_date = None
          if event.date:
              event_date = event.date.strftime('%A, %B %d at %I:%M %p')

          event_location = None
          if event.location:
            event_location = event.location
          
          # formulate event
          response += f"- **{event_name}**"
          if event_location != None:
             response += f" in {event_location}"
          if event_date != None:
             response += f" on {event_date}"
          if event_description != None:
             response += f":\n"
             response += f"> {event_description}\n"
          else:
             response += f"\n"

  return response.strip()