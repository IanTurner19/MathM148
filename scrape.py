import requests
from datetime import datetime
import pandas as pd
from io import StringIO
import gzip
import numpy as np

BASE_URL = "https://app.ticketmaster.com/discovery-feed/v2/events.csv"
ONLY_USA = "?countryCode=US"
API_KEY = "&apikey=2zz9VTmXWqWEZhjfuBWmJ3OV90bvVDpk"  # api key is free, doesn't matter if leaked
url = "".join([BASE_URL, ONLY_USA, API_KEY])

# we want concerts that happen before the end of the quarter, march 21st 2025
END_DATE = datetime(2025, 3, 21)
# as described in https://docs.google.com/document/d/1DfaEpcEoRCC792qEEENcZ6HwOGSgjQWveNSDcqEvYkQ/edit?usp=sharing
KEEP_COLS = [
    "EVENT_ID",
    "EVENT_NAME",
    "EVENT_START_DATETIME",
    "EVENT_END_DATETIME",
    "CLASSIFICATION_GENRE",
    "CLASSIFICATION_SUB_GENRE",
    "MIN_PRICE",
    "MAX_PRICE",
    "ATTRACTION_NAME",
    "ATTRACTION_ID",
    "VENUE_NAME",
    "VENUE_ID",
    "VENUE_STREET",
    "VENUE_CITY",
    "VENUE_STATE_CODE",
    "VENUE_TIMEZONE",
    "CLASSIFICATION_TYPE",
    "CLASSIFICATION_SUB_TYPE",
    "ATTRACTION_CLASSIFICATION_SEGMENT",
    "ATTRACTION_CLASSIFICATION_GENRE",
    "ATTRACTION_CLASSIFICATION_SUB_GENRE",
    "ATTRACTION_CLASSIFICATION_TYPE",
    "ATTRACTION_CLASSIFICATION_SUB_TYPE",
    "TRANSACTABLE",
    "HOT_EVENT",
    "scrape_time"
]

resp = requests.get(url)  # returns string of csv file, compressed
decompressed_data = gzip.decompress(resp.content)
csv_str = decompressed_data.decode('utf-8')

df = pd.read_csv(StringIO(csv_str))
df.dropna(subset=["MIN_PRICE", "MAX_PRICE"], how='all', inplace=True)  # rows without prices aren't useful
df["EVENT_START_DATETIME"] = pd.to_datetime(df["EVENT_START_DATETIME"])  # originally str
df["scrape_time"] = pd.Series(datetime.now(), index=df.index)

# apply filters
music_only = df[df["CLASSIFICATION_SEGMENT"] == "Music"]
this_quarter = music_only[
    (music_only["EVENT_START_DATETIME"] > pd.Timestamp(datetime.now()).tz_localize("UTC")) & 
    (music_only["EVENT_START_DATETIME"] <= pd.Timestamp(END_DATE).tz_localize("UTC"))
]  
trimmed_df = this_quarter[KEEP_COLS]  

trimmed_df.to_csv("whole_quarter.csv")
