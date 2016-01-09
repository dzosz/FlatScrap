[![Build Status](https://travis-ci.org/dzosz/FlatScrap.svg?branch=master)](https://travis-ci.org/dzosz/FlatScrap)
# FlatScrap
Presents on the map apartments and rooms for rent in Wroclaw from last 14 days

## Structure
* Flask server with Redis integration
* Periodical cron job updates the addresses
* RQ worker and Geopy, geocoding street to latitude ang longitude

