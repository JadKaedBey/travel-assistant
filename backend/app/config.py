from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Access variables
EVENTBRITE_API_KEY = os.getenv('EVENTBRITE_API_KEY')
OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
OPENTRIPMAP_API_KEY = os.getenv('OPENTRIPMAP_API_KEY')