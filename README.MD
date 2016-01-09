[![Build Status](https://travis-ci.org/dzosz/FlatScrap.svg?branch=master)](https://travis-ci.org/dzosz/FlatScrap)
# FlatScrap
Presents on the map apartments and rooms for rent in Wroclaw

## Functions
* Gets recent advertisements from external website
* Lookups street names in contents
* Geocodes address to latitude and longitude
* Puts gathered data onto the map

## Structure 
* Flask server
* periodical Redis db updates scheduled with cron
  * search for new advertisements
  * run RQ worker and kill after jobs are finished (burst mode)
