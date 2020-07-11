import json
import sqlite3
fp = open("state_district.json","r")

conn = sqlite3.connect('covid.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS State
(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
state TEXT UNIQUE)''')

cur.execute('''CREATE TABLE IF NOT EXISTS City
(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
city TEXT UNIQUE,
state_id INTEGER)''')

tree = json.load(fp)

states = tree['states']
print("Loading data to database......")
for state in states:
    state_name = state['name']
    cur.execute('INSERT OR IGNORE INTO State (state) VALUES (?) ',(state_name,))
    cur.execute('SELECT id FROM State WHERE state = ? ', (state_name,))
    state_id = cur.fetchone()[0]
    cities = state['districts']
    for city in cities:
        city_name = city['name']
        cur.execute('INSERT OR IGNORE INTO City (city,state_id) VALUES (?,?)', (city_name,state_id,))
    conn.commit()

print("Data loaded of states and cities in database...")