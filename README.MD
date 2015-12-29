# FlatScrap
Presents on the map apartments and rooms for rent in Wroclaw

## Functions
* Gets recent advertisements from external website
* Lookups street names in contents
* Geocodes address to latitude and longitude
* Puts gathered data onto the map

## Modes
* continuous Flask server
* periodical database updates with cron
  * search for new advertisements
  * kill the worker after finished (burst mode)
