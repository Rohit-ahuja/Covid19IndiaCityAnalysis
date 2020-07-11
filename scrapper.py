import urllib.request, urllib.parse, urllib.error
import json
import ssl
import pymongo
import sqlite3


conn = sqlite3.connect('covid.sqlite')
cur = conn.cursor()

cur.execute('''SELECT City.city,State.state
FROM City JOIN State ON City.state_id=State.id''')



# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://api.covid19india.org/districts_daily.json'
print('Retrieving', url)
uh = urllib.request.urlopen(url, context=ctx)
data = uh.read()

myclient = pymongo.MongoClient("mongodb://localhost:27017")

mydb = myclient["coviddb"]
mycol = mydb["coviddata"]
mycol.drop()

print('Retrieved', len(data), 'characters')
print("Loading data into database...")
tree = json.loads(data)
count = 0

for row in cur:
    (city,state) = row
    try:
        data = tree['districtsDaily'][state][city]
    except:
        print("No data found for: ",city,state)
    json_to_put = '''
    {
        "id" : "",
        "state" : "",
        "data" : []
    }
    '''
    parsed = json.loads(json_to_put)

    parsed['id'] = city
    parsed['state'] = state
    parsed['data'] = data
    x = mycol.insert_one(parsed)
    count = count + 1
    #myquery = {"id": "Kanpur" }

    #mydoc = mycol.find(myquery)

    #for x1 in mydoc:
        #print(x1)

print("Total rows added:",count)
