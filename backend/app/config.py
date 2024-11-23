from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Access variables
EVENTBRITE_API_KEY = os.getenv('EVENTBRITE_API_KEY')
TICKETMASTER_API_KEY = os.getenv('TICKETMASTER_API_KEY')
OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
OPENTRIPMAP_API_KEY = os.getenv('OPENTRIPMAP_API_KEY')

LMSTUDIO_HOST = os.getenv('LMSTUDIO_HOST', "127.0.0.1:1234")
LMSTUDIO_ENDPOINT = os.getenv('LMSTUDIO_ENDPOINT', "v1/chat/completions")
LMSTUDIO_MODEL = os.getenv('LMSTUDIO_MODEL', "llama-3-8b-lexi-uncensored")
