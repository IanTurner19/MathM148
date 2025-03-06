# Artist popularity data from Spotify

Artist popularity would be an important factor to consider when predicting concert ticket prices, but is not in the Ticketmaster data. 

## linking.ipynb
This file takes in the dataset containing Ticketmaster, city population, and venue capacity and the 2 datasets containing spotify artist data (spotify_artist_data_2023.csv and output.csv). It joins them by lowercase Ticketmaster attraction name and lowercase spotify artist name match. Ticketmatser attraction name can contain multiple artists separated by a pipe "|", so if there are multiple matches, the highest artist popularity is chosen. This is then assigned as the popularity of the concert. 

## scrape
For the artists from the Ticketmaster dataset who were not in the spotify dataset, we attempted to obtain their spotify popularity score through the spotify API. 