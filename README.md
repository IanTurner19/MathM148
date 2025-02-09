# Ticket Price Prediction

## Update

Google Apps Script cannot update the file if the size is above 50 MB. The limit seems to be 10 MB according to https://developers.google.com/apps-script/reference/drive/file#setcontentcontent but the real limit seems to be 50MB. 

In addition, the Ticketmaster Discovery Feed price column does not update. new_scrape.py uses the Ticketmaster Discovery API instead, which does seem to have price updates. The columns collected are roughly the same, and described in new_data.csv

## Data Collection

### Ticketmaster API
Ticket price history data is very tightly guarded and is not free. We decided to gather current data for a period of 10 days. We used the Ticketmaster API and Google Apps Script to store this information in a csv file in Google Drive. 

The Ticketmaster API has a discovery functionality and a discovery feed functionality. The discovery functionality is limited to 1000 events, but we wanted to collect data on all concerts in the USA starting between Feb. 2 and Feb. 13, and there were more than 1000 of them. Therefore, we decided to use the discovery feed API, which does not have this limit. 

The 77 attributes of each event are listed in columns.txt. We chose the ones listed in the KEEP_COLS variable of scrape.py, to use in our analysis. 

### scrape.py
Calls the Ticketmaster Discovery Feed API https://developer.ticketmaster.com/products-and-docs/apis/discovery-feed/

Filters and adds the time of scraping to data, then sends it to google apps script, and saves a backup copy on the server. 

Running on a Google Cloud free trial server once an hour. Commands used for setup:
1. sudo apt install python3-requests python3-pandas
2. crontab -e, 0 * * * * /usr/bin/python3 /home/wbian(username)/scrape.py

The response from the Ticketmaster API uses too much memory for solutions such as AWS Lambda and Google Apps Script.

### Code.gs
Takes a POST request with the latest snapshot of ticket data and appends it to a google drive file, data.csv. data.csv is initially set up as shown in this repository. 