from datetime import datetime
from pydantic import BaseModel
from app.api import nlp, events, weather, overpass, localdatasets
from app.api.opentripmap import OpenTripMapModel, query_opentripmap
from app.api.weather import query_weather, WeatherQueryModel
from app.api.lmstudio import lm_studio_request
from app.history.chat_history import (
    UserOrChatbot, 
    InsertMessage,
    add_message,
    create_new_chat
)
from app.answer import Answer
from app.dateparser import parse_date

CITY_NOT_FOUND = "You seem to have not provided the city correctly. Please double check it"

class QueryRequest(BaseModel):
    user_input: str
    session_id: str

class QueryResponse(BaseModel):
    id: str
    message: str

def run_query(query: QueryRequest):
    if query.session_id == "/":
        query.session_id = create_new_chat(query.user_input)
    else:
        add_message(
            InsertMessage(
                session_id          = query.session_id,
                user_or_chatbot     = UserOrChatbot.USER,
                message             = query.user_input
            )
        )

    if False: # DEBUG
        add_message(
            InsertMessage(
                session_id          = query.session_id,
                user_or_chatbot     = UserOrChatbot.CHATBOT,
                message             = "this is test"
            )
        )
        return QueryResponse(id=query.session_id, message="this is test")

    # Step 1: NLP extraction (city, date, keywords)
    info = nlp.extract_info(query.user_input)  # Use query.user_input from the model
    print(f"NLP extraction: {info}")

    # Step 1.5: 
    # --CITY--
    city = info.get('city')

    if city is None:
        add_message(
            InsertMessage(
                session_id          = query.session_id,
                user_or_chatbot     = UserOrChatbot.CHATBOT,
                message             = CITY_NOT_FOUND
            )
        )
        return QueryResponse(id=query.session_id, message=CITY_NOT_FOUND)
    
    # --DATE--
    date = info.get('date')
    try:
        date = parse_date(date)
    except:
        date = datetime.today().date()
    if date is None:
        date = datetime.today().date()
    
    # --KEYWORDS--
    keywords = info.get('keywords')

    # Step 2: Check if any pinned events exist
    pinned_events = events.check_pinned_events(city, date, keywords)

    if pinned_events:
        pinned_answer = lm_studio_request(pinned_events)
        return QueryResponse(id=query.session_id, message=pinned_answer)
    
    # Step 3: Fetch events from OpenTripMap
    event_results = query_opentripmap(OpenTripMapModel(placename=city, kinds=keywords))

    # Step 4: Fetch dynamic events from Ticketmaster and append them to OpenTripMap results
    event_results.extend(events.query_ticketmaster(city, date, keywords))

    # Step 5: Fetch weather from OpenWeatherMap
    weather_info = ""
    if date == datetime.today().date():
        weather_query = WeatherQueryModel(
            city=city,
        )
        weather_info = query_weather(weather_query)

    unesco_sites = localdatasets.get_unesco_sites(city)
    hotels_motels = localdatasets.get_hotels_motels(city)
    historic_places = localdatasets.get_historical_places(city)
    
    # TODO Implement ammenities keywords extraction in nlp
    try:
        amenity = keywords[0] if keywords else "cafe"  # Use first keyword as amenity type or default to "cafe"
        poi_results = overpass.get_poi_data(city, amenity)
    except:
        print("Something went wrong while fetching poi_results! (query.py)")
        poi_results = []
    
    # Step 6: Return the compiled response
    answer: Answer = {
        "events": event_results,
        "weather": weather_info,
        "pois": poi_results,
        "unesco_sites": unesco_sites,
        "hotels_motels": hotels_motels,
        "historic_places": historic_places
    }

    # Step 7: Post-process with LLM to get more human-like response
    ans = lm_studio_request(answer)

    add_message(
        InsertMessage(
            session_id          = query.session_id,
            user_or_chatbot     = UserOrChatbot.CHATBOT,
            message             = ans
        )
    )
    return QueryResponse(id=query.session_id, message=ans)