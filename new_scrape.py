import requests
from datetime import datetime

api_key = "ljmJ6y8jH7XpdY1iJ68nADTczTfPhVDS"
GAS_URL = "https://script.google.com/macros/s/AKfycbxFahQydjQv0yGYURjtsRKz5BHd-Z78786YBQgqKu3MXvoAiOpvEEbroW36jPi0Em9K/exec?fileId={FILE ID HERE}"
start_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
end_date = datetime(year=2025, month=2, day=15).strftime("%Y-%m-%dT%H:%M:%SZ")  # midpoint check in

# API request with U.S. filter, price filter, and 14-day range
BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"
ONLY_USA = "?countryCode=US"
NEXT2WEEKS = f"&startDateTime={start_date}&endDateTime={end_date}"
API_KEY = f"&apikey={api_key}"
SIZE = "&size=200"  # 200 IS MAX PAGE ZIE
POP = "&classificationName=Pop"

# as described in https://docs.google.com/document/d/1DfaEpcEoRCC792qEEENcZ6HwOGSgjQWveNSDcqEvYkQ/edit?usp=sharing
COLS = [
    ["id"],  # event id
    ["name"],  # event name
    ["dates", "start", "dateTime"],  # "EVENT_START_DATETIME",
    # removed because mostly null, ["dates", "end", "dateTime"],  # "EVENT_END_DATETIME",
    ["classifications", 0, "genre", "name"],  # "CLASSIFICATION_GENRE",
    ["classifications", 0, "subGenre", "name"],  # "CLASSIFICATION_SUB_GENRE",
    ["priceRanges", 0, "min"],  # "MIN_PRICE",
    ["priceRanges", 0, "max"],  # "MAX_PRICE",
    ["_embedded", "attractions", 0, "name"],  # "ATTRACTION_NAME",
    ["_embedded", "attractions", 0, "id"],
    ['_embedded', 'venues', 0, 'city', 'name'],  # "venue city",
    ['_embedded', 'venues', 0, 'id'],  # venue id
    ['_embedded', 'venues', 0, 'address', 'line1'],
    ['_embedded', 'venues', 0, 'state', 'stateCode'],
    ['_embedded', 'venues', 0, 'timezone'],  # "VENUE_TIMEZONE",
    ["classifications", 0, "type", "name"],  
    ["classifications", 0, "subType", "name"],  
    ["_embedded", "attractions", 0, "classifications", 0, "segment", "name"],  
    ["_embedded", "attractions", 0, "classifications", 0, "genres", 0, "name"], 
    ["_embedded", "attractions", 0, "classifications", 0, "genres", 0, "subGenres", 0, "name"],  
    ["_embedded", "attractions", 0, "classifications", 0, "type", "name"],  
    ["_embedded", "attractions", 0, "classifications", 0, "type", "subTypes", 0, "name"],  
]

def stringify_row(row):
    '''
    row is a list representing a row in a dataframe
    returns it as a comma separated string
    '''
    as_strs = []
    for val in row:
        if val is None:
            as_strs.append("")  # don't want to turn None into "None"
        elif type(val) == str:
            # leaving commas and newlines messes up csv file
            as_strs.append(val.replace(",", " ").replace("\n", " "))  
        else:
            as_strs.append(str(val))
    return ",".join(as_strs)

output = []  # list of lists
no_page_url = "".join([BASE_URL, ONLY_USA, API_KEY, POP, NEXT2WEEKS, SIZE])
page = 0
more_events = True
while more_events:
    url = "&".join([no_page_url, f"page={page}"])
    response = requests.get(url)
    data = response.json()
    more_events = data["page"]["totalPages"] != data["page"]["number"]  # on last page, pages count from 0
    if "_embedded" not in data:
        continue
    for event in data["_embedded"]["events"]:
        row = []
        if 'priceRanges' not in event:
            continue
        for attrs in COLS:
            curr_val = event
            for attr in attrs:
                if type(curr_val) == list and len(curr_val) == 0:
                    curr_val = None
                    break
                if type(curr_val) == dict and attr not in curr_val:
                    curr_val = None
                    break
                curr_val = curr_val[attr]
            row.append(curr_val)
        row.append(datetime.now())
        output.append(stringify_row(row))
    page += 1

output_str = "\n".join(output)
payload = {
    "snapshot": "".join([output_str, "\n"])  # the google apps script needs the last character to be a newline
}  # format expected by google apps script
#requests.post(GAS_URL, json=payload)  # write to google drive
