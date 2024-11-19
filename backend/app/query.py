from pydantic import BaseModel
from app.api import nlp, events, weather, overpass
from app.api.opentripmap import OpenTripMapModel, query_opentripmap
from app.api.lmstudio import lm_studio_request
from app.history.chat_history import (
    UserOrChatbot, 
    InsertMessage,
    add_message,
)

class QueryRequest(BaseModel):
    user_input: str
    session_id: str

def run_query(query: QueryRequest):
    add_message(
        InsertMessage(
            session_id          = query.session_id,
            user_or_chatbot     = UserOrChatbot.USER,
            message             = query.user_input
        )
    )

    # Step 1: NLP extraction (city, date, keywords)
    info = nlp.extract_info(query.user_input)  # Use query.user_input from the model
    print(f"NLP extraction: {info}")

    # TODO handle cases where city/date are not given
    # Step 2: Check if any pinned events exist
    city = info.get('city')
    date = info.get('date')
    keywords = info.get('keywords')

    pinned_events = events.check_pinned_events(city, date)

    if pinned_events:
        return {"result": f"Prioritized event: {pinned_events}"}

    # Step 3: Fetch events from OpenTripMap
    event_results = query_opentripmap(OpenTripMapModel(placename=city, kinds=keywords))

    # Step 4: Fetch weather from OpenWeatherMap
    weather_info = weather.query_weather(city, date)
    
    # TODO Implement ammenities keywords extraction in nlp
    amenity = keywords[0] if keywords else "cafe"  # Use first keyword as amenity type or default to "cafe"
    poi_results = overpass.get_poi_data(city, amenity)
    
    # Step 5: Return the compiled response
    answer = {
        "events": event_results,
        "weather": weather_info,
        "pois": poi_results
    }

    # Step 6: Post-process with LLM to get more human-like response
    ans = lm_studio_request([
        { "role": "system", "content": "You are application assistant. Based on given JSON tell what person can visit. Answer in human way like chat assistant talking to a person." },
        { "role": "user", "content": str(answer) }
    ])

    add_message(
        InsertMessage(
            session_id          = query.session_id,
            user_or_chatbot     = UserOrChatbot.CHATBOT,
            message             = ans
        )
    )
    return ans