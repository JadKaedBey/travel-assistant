import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.api import nlp, events, weather, overpass
from app.api.opentripmap import OpenTripMapModel, query_opentripmap
from app.api.lmstudio import lm_studio_request
from app.history.chat_history import (
    UserOrChatbot, 
    InsertMessage, 
    RetrieveMessage, 
    add_message, 
    find_session_id,
    generate_session_id
)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the request body model
class QueryRequest(BaseModel):
    user_input: str
    session_id: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Travel Assistant"}

# endpoint accepts a JSON body via Pydantic model
@app.post("/query/")
def process_query(query: QueryRequest):
    print(f"Query: {query}")
    try:
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

    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)  # Log the error details
        raise HTTPException(status_code=500, detail="Internal Server Error")


# session id logic
@app.get("/check-session-id/")
def check_session_id(session_id: str):
    return {"found": find_session_id(session_id)}

@app.post("/fresh-session-id/")
def fresh_session_id():
    return {"session_id": generate_session_id()}
