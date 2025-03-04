import requests
import json
import time
import traceback

API_KEY_FILENAME = "spotify_credentials.json"  # array of objects with attributes id and secret
ARTISTS_FILENAME = "artists.txt"  # list of artists separated by newline
OUTPUT_FILENAME =  "output.csv"  # will have 3 columns, artist, spotify id, and popularity
ERR_LOG_FILENAME = "errors.txt"  # index of artists, separated by newline

ACCESS_TOKEN_URL = "https://accounts.spotify.com/api/token"
ACCESS_TOKEN_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded"
}
# spotify returns artists in order of relevance, so if 1st one isn't correct, no need to check the next ones
SEARCH_URL = "https://api.spotify.com/v1/search?type=artist&limit=1"  

api_keys = []
with open(API_KEY_FILENAME, "r") as api_key_file:
    api_keys = json.loads(api_key_file.read())

artists = []
with open(ARTISTS_FILENAME, "r") as artists_file:
    for line in artists_file.readlines():
        if line[-1] == "\n":
            # get rid of newline
            artists.append(line[:-1])
        else:
            artists.append(line)

# make 2 calls a minute to stay under 25 calls/hr/api key limit 
# (there will probably be 5 api keys)
# need to refresh access token every hour, or 120 calls
access_tokens = []
curr_call = 120  # bug caused issues after 120, so restarting from 120
while curr_call < len(artists):
    artist = artists[curr_call]
    print("currently looking for", artist)
    try:
        if curr_call % 120 == 0:
            access_tokens = []
            print("getting access tokens")
            for api_key in api_keys:
                data_str = f"grant_type=client_credentials&client_id={api_key['id']}&client_secret={api_key['secret']}"
                access_token_resp = requests.post(ACCESS_TOKEN_URL, data=data_str, headers=ACCESS_TOKEN_HEADERS)
                access_tokens.append(access_token_resp.json()["access_token"])
        # alternate between api keys each call
        access_token = access_tokens[curr_call % len(access_tokens)]
        curr_url = f"{SEARCH_URL}&q={artist}" 
        curr_header = {
            "Authorization": f"Bearer  {access_token}"
        }
        curr_resp = requests.get(curr_url, headers=curr_header).json()
        popularity = -1  # default for artists who aren't found
        spotify_id = ""
        num_artists = curr_resp["artists"]["total"]
        if num_artists > 0:
            spotify_artist_info = curr_resp["artists"]["items"][0]
            if spotify_artist_info["name"].lower() == artist.lower():
                popularity = spotify_artist_info["popularity"] 
                spotify_id = spotify_artist_info["id"]
        with open(OUTPUT_FILENAME, "a") as outfile:
            outfile.write(f"{artist.replace(',', '')},{spotify_id},{popularity}\n")
    
    except Exception as err:
        print(traceback.format_exc())
        # write calls_made to output file
        with open(ERR_LOG_FILENAME, "a") as err_file:
            err_file.write(str(curr_call) + "\n")
    
    curr_call += 1        
    time.sleep(30)