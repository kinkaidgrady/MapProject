# MapProject is a project that I completed by myself after finishing the 4th course in my Python Specialization that I completed recenty. 
# This goal of this project is to take a list of data - addresses in this case - and turn them into a static map. To do this I:
  # Built a simple text file of the addresses - livermoresales.data
  # Use geoload.py to pass livermoresales.data through the Google API in order to obtain the geodata(geoload.py) and build a SQL database out of the geodata
  # Use geodump.py to build where.js which is a list of the addresses' geodata and full location names 
  # Use latlongconvert.py to take that list and print it out in the form to use in the url for markers when making the static map
  # Copy the printed data from latlongconvert.py and paste it into mapmakerlivermore.html between marker color and the API key in order to generate all of the markers for the map
    # I created the rest of the URL for the map by referencing the documentation on Google Maps API
  # Open the mapmakerlivermore.html file and you now have a static map showing all of the addresses from the original list - livermoresales.data
  # The code in the files can be minorly tweaked to reference a different set of initial data, and the URL adjusted (simply changing the center to where you want it to be and pasting in the new marker data) in order to generate a new map
