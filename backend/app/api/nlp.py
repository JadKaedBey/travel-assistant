# backend/app/nlp.py
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_info(user_input: str):
    doc = nlp(user_input)
    entities = {ent.label_: ent.text for ent in doc.ents}
    
    # Extract important keywords and entities like location, time, and events
    city = entities.get("GPE", None)  # GPE is geopolitical entity, like city or country
    date = entities.get("DATE", None)
    
    return {
        "city": city,
        "date": date,
        "keywords": [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"] if (
            (city is None or token.text.lower() != city.lower()) and (date is None or token.text.lower() not in date.split(" "))
        )]  # Nouns/Proper Nouns
    }
