#import libraries 
import urllib.request, urllib.parse, urllib.error
import http
import sqlite3
import json
import time
import ssl
import sys

#establish API Key and serviceurl. I removed my API key for security - feel free to add your own and test it out
api_key = True
api_key = 'AIzaSyCjJfXCh-C-NCzQIdl_ETOaG-YIfCy2STk'
serviceurl = "https://maps.googleapis.com/maps/api/geocode/json?"

# Additional detail for urllib
# http.client.HTTPConnection.debuglevel = 1

# Establish connection and cursor
conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()

#create table for SQL
cur.execute('''
CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#Establish handle
fh = open("livermoresales.data")
count = 0

#Guardian to ensure we don't use up all of our credits with the Google Maps API
for line in fh:
    if count > 200 :
        print('Retrieved 200 locations, restart to retrieve more')
        break

    #Clean and encode data to pass into API
    address = line.strip()
    print('')
    cur.execute("SELECT geodata FROM Locations WHERE address= ?",
        (memoryview(address.encode()), ))

    #guardian
    try:
        data = cur.fetchone()[0]
        print("Found in database ",address)
        continue
    except:
        pass

    #create dictionary
    parms = dict()
    parms["address"] = address
    if api_key is not False: parms['key'] = api_key
    url = serviceurl + urllib.parse.urlencode(parms)

    #decode geodata, print statements to ensure code is working
    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' '))
    count = count + 1

    #guardian
    try:
        js = json.loads(data)
    except:
        print(data)  # We print in case unicode causes an error
        continue

    #guardian
    if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS') :
        print('==== Failure To Retrieve ====')
        print(data)
        break

    #insert retrieved data into database
    cur.execute('''INSERT INTO Locations (address, geodata)
            VALUES ( ?, ? )''', (memoryview(address.encode()), memoryview(data.encode()) ) )
    conn.commit()
    if count % 100 == 0 :
        print('Pausing for a bit...')
        time.sleep(5)

print("Run geodump.py to read the data from the database so you can vizualize it on a map.")
