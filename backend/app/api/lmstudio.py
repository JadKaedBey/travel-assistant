from typing import TypedDict
import requests
import json

from app.config import LMSTUDIO_HOST, LMSTUDIO_ENDPOINT, LMSTUDIO_MODEL

class Message(TypedDict):
    role: str
    content: str

def lm_studio_request(messages: list[Message]) -> str:
    full_url = f"http://{LMSTUDIO_HOST}/{LMSTUDIO_ENDPOINT}"

    payload = {
        "model": LMSTUDIO_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }

    response = requests.post(
        url=full_url,
        headers={
            "Content-Type": "application/json"
        },
        data=json.dumps(payload)
    )

    if response.status_code == 200:
        json_repsonse = response.json()
        print(json_repsonse)
        return json_repsonse['choices'][0]['message']['content']
    else:
        raise Exception(f"""
            Error {response.status_code} in make_request 
            for url {full_url}
            : {response.text}
        """)
