# Scraping with the Spotify API

There are artists in Ticketmaster that do not show up in the spotify dataset. To obtain their popularity scores, we created a script to obtain this information from the Spotify API. 

## find.ipynb
This notebook writes all of the artists who show up in Ticketmaster data but not in the spotify dataset to a file called artists.txt.

## scrape.py
This file uses artists.txt to call the Spotify API search endpoint for their popularity score. If no exact lowercase match is found, this artist is assumed to not be on Spotify. Close matches cannot be counted, for example CAIN and Caine are 2 very different artists. Only the first response from Spotify is considered because the Spotify API orders everything by relevance. scrape.py is set up to work within the rate limits of the Spotify API and runs on a free Google Cloud server. The collected data is written to output.csv, which contains columns of artist name, spotify id if found, and popularity score (-1 if not found). scrape.py also relies on spotify_credentials.json, which isn't included in this repository for security reasons, but contains an array of objects containing spotify API client ID and secret. 