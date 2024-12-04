from typing import Literal
from typing_extensions import TypedDict
import requests
import json

from app.config import LMSTUDIO_HOST, LMSTUDIO_ENDPOINT, LMSTUDIO_MODEL
from app.query_str import generate_ai_style_response
from app.answer import Answer

class Message(TypedDict):
    role: Literal['user', 'assistant', 'system']
    content: str

def lm_studio_request(message: Answer) -> str:
    full_url = f"http://{LMSTUDIO_HOST}/{LMSTUDIO_ENDPOINT}"
    
    messages = [
        { "role": "system", "content": "You are application assistant. Based on given JSON tell what person can visit. Answer in human way like chat assistant talking to a person." },
        { "role": "user", "content": str(message) }
    ]

    payload = {
        "model": LMSTUDIO_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }

    try:
        response = requests.post(
            url=full_url,
            headers={
                "Content-Type": "application/json"
            },
            data=json.dumps(payload)
        )

        if response.status_code == 200:
            json_repsonse = response.json()
            return json_repsonse['choices'][0]['message']['content']
    except:  # noqa: E722
        return generate_ai_style_response(message["events"], message["weather"])
