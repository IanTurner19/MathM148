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

# we want concerts that happen before feb 13 2025 utc
END_DATE = datetime(2025, 2, 13)
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
    "MIN_PRICE_WITH_FEES",
    "MAX_PRICE_WITH_FEES",
    "TRANSACTABLE",
    "HOT_EVENT",
    "scrape_time"
]

GAS_URL = "https://script.google.com/macros/s/AKfycby9gHsXvg3D-fJkZnWUQKXAGf9xrZ38k_cL6Fv3MbCVT0aareweZIgAXmSgcvecODrP/exec"

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


resp = requests.get(url)  # returns string of csv file, compressed
decompressed_data = gzip.decompress(resp.content)
csv_str = decompressed_data.decode('utf-8')

df = pd.read_csv(StringIO(csv_str))
df = df.replace({np.nan: None})  # NaN is not json serializable, needed for POST call to google drive
df.dropna(subset=["MIN_PRICE", "MAX_PRICE"], how='all', inplace=True)  # rows without prices aren't useful
df["EVENT_START_DATETIME"] = pd.to_datetime(df["EVENT_START_DATETIME"])  # originally str
df["scrape_time"] = pd.Series(datetime.now(), index=df.index)

# apply filters
music_only = df[df["CLASSIFICATION_SEGMENT"] == "Music"]
week5 = music_only[
    (music_only["EVENT_START_DATETIME"] > pd.Timestamp(datetime.now()).tz_localize("UTC")) & 
    (music_only["EVENT_START_DATETIME"] <= pd.Timestamp(END_DATE).tz_localize("UTC"))
]  
trimmed_df = week5[KEEP_COLS]  

payload_list = trimmed_df.values.tolist()  # list of lists, where each inner list is a row
row_strs = [stringify_row(row) for row in payload_list]  # list of strs
snapshot_str = "\n".join(row_strs)
payload = {
    "snapshot": "".join([snapshot_str, "\n"])  # the google apps script needs the last character to be a newline
}  # format expected by google apps script
requests.post(GAS_URL, json=payload)  # write to google drive

trimmed_df.to_csv(f"{datetime.now()}_scrape.csv")
