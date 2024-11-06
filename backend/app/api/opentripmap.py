"""
This script contains the logic for interacting with the OpenTripMap API using FastAPI.
(https://rapidapi.com/opentripmap/api/places1/playground/apiendpoint_c92ce138-db30-4713-9058-752835430bc7)
It can be seen as an extension of the events.py file.

Author: Ruben Vandamme
Date: 04 November 2024
Usage:
    - Call the query_opentripmap function with a name of a city to get a list of relevant Events.
"""

import requests
from typing import List
from app.models.event_model import Event
from pathlib import Path
from app.config import OPENTRIPMAP_API_KEY
from pydantic import validate_call

HOST = "opentripmap-places-v1.p.rapidapi.com"
VALID_KINDS_FILE_PATH = Path(__file__).resolve().parents[2] / 'app' / 'api' / 'opentripmap_valid_kinds.txt'

def make_request(endpoint: str, query_params: dict) -> dict:
    """General request function for OpenTripMap API"""

    # variables
    headers = {
        "X-RapidAPI-Key": OPENTRIPMAP_API_KEY,
        "X-RapidAPI-Host": HOST
    }
    full_url = f"https://{HOST}/{endpoint}"

    # make request
    response = requests.get(
        url=full_url, 
        headers=headers, 
        params=query_params
    )

    # parse request if valid
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"""
            Error {response.status_code} in make_request 
            for url {full_url} 
            with headers {headers} 
            and params {query_params}
            : {response.text}
        """)

@validate_call
def query_opentripmap(
    placename:      str,     
    radius:         int | None  = None,
    walking_time:   int | None  = 5,
    kinds:          List[str]   = [],
    limit:          int | None  = 10,
    filter:         str | None  = None
):
    """Fetch events from OpenTripMap API.
    https://dev.opentripmap.org/docs#/Objects%20list/getListOfPlacesBySuggestions.

    Attributes:
        placename:      eg. Paris
        radius:         in meters (ór radius ór walking_time is mandatory)
        walking_time:   in minutes (ór radius ór walking_time is mandatory)
        kinds:          eg. ['foods', 'fountains'] (empty list means all kinds)
        limit:          Maximum number of returned objects.
        filter:         String to filter on (eg. 'don' for McDonalds) (at least 3 chars)

    >>> type(query_opentripmap('Paris', limit=1, kinds=['foods']))
    <class 'list'>
    """

    print(f"""Querying OpenTripMap for: 
    placename={placename}, 
    radius={radius}, 
    walking_time={walking_time},
    kinds={kinds},
    limit={limit},
    filter={filter}""")

    # check params
    if radius != None and walking_time != None:
        raise Exception(f"""
        ParamError in query_opentripmap.
        Please specify a radius or walking_time, but not both.
        Radius was {radius} and walking_time was {walking_time}.
        """)
    if radius == None and walking_time == None:
        raise Exception(f"""
        ParamError in query_opentripmap.
        Please specify a radius or walking_time.
        """)
    if walking_time != None:
        radius = (walking_time * 60) * 3   # assume 3m/s in bird flight distance
    
    with open(VALID_KINDS_FILE_PATH, 'r') as file:
        valid_set = set(line.strip() for line in file)
    kinds = [kind.lower().replace(" ", "_") for kind in kinds]
    valid_kinds = []
    for kind in kinds:
        if kind in valid_set:
            valid_kinds.append(kind)
        else:
            print(f"{kind} is not a valid kind. It will be ignored.")
    if limit <= 0:
        raise Exception(f"""
        ParamError in query_opentripmap.
        Please specify a positive integer for limit instead of {limit}. 
        """)
    if filter != None and len(filter) < 3:
        print(f"Filter was {filter}, but it has to be at least 3 characters. It will be ignored.")
        filter = None

    # first get location coordinates
    result = make_request(
        endpoint="en/places/geoname",
        query_params={"name": placename.capitalize()}
    )
    try:
        lat = result['lat']
        lon = result['lon']
        if result['status'] != 'OK':
            raise Exception(f"""
                Error status not OK in query_opentripmap
                for placename {placename}.
                Full result: {result}
            """)
    except KeyError as e:
        raise Exception(f"""
            KeyError in make_request response in query_opentripmap
            for placename {placename}.
            Latitude, longitude or status was not found.
            Full result: {result}
            Full error: {e}
        """)
    
    # next, get the POI
    if filter != None:
        result = make_request(
            endpoint="en/places/autosuggest",
            query_params={
                "lon":      str(lon),
                "lat":      str(lat),
                "radius":   str(radius),
                "limit":    str(limit),
                "kinds":    ','.join(valid_kinds),
                "name":     filter,
                "format":   'json'
            }
        )
    else:
        result = make_request(
            endpoint="en/places/radius",
            query_params={
                "lon":      str(lon),
                "lat":      str(lat),
                "radius":   str(radius),
                "limit":    str(limit),
                "kinds":    ','.join(valid_kinds),
                "format":   'json'
            }
        )

    # and transform it to Events
    try:
        events = []
        for obj in result:
            events.append(Event(
                id          = obj['xid'],
                name        = obj['name'],
                location    = placename,        # opentripmap returns the exact coordinates as well
                #category    = obj['kinds'],    # opentripmap returns a list of relevant categories
                category=None,
                description=None,
                date=None,
                url=None
            ))
        return events
    except KeyError as e:
        raise Exception(f"""
            KeyError in make_request response in query_opentripmap
            for placename {placename}.
            xid or name was not found.
            Full result: {result}
            Full error: {e}
        """)
    
        
if __name__ == "__main__":
    import doctest
    doctest.testmod()