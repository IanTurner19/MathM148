# final.csv
This data the fully combined data, including venues capacities, city population, artist popularities, and ticket prices. This was the data that was used for generating EDA graphs and plots, in addition to training and testing our models. 

# map_source.csv
This data was used to generate exact locations for concerts, for the purposes of creating a US map. (See the map sub folder in the EDA folder for the code)

# new_data.csv
This data was generated from the Ticketmaster API and was another batch of scraping the website. 

# output.csv
Our spotify artist dataset included thousands of artists and their respective popularities (from 0-100). However, after merging this with our Ticketmaster data, there were several artistis that did not have matches from the dataset. Because of this, we used Spotify API to fill in the blanks, so this data is the result of Spotify API scraping.

# spotify_artist_data_2023.csv
This was the original spotify popularity dataset, found on Kaggle [Kaggle Spotify Data](https://www.kaggle.com/datasets/tonygordonjr/spotify-dataset-2023). 

# whole_quarter+cities2.csv
This data was generated as a merge between our cities dataset and our ticketmaster data set. It does not include artist popularity or venue capacity. 

# whole_quarter_cities_venues.csv
This data is the data set above combined with several venue capacities. 
