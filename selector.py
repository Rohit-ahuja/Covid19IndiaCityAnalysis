import sqlite3
import pymongo
import matplotlib.pyplot as plt

conn = sqlite3.connect('covid.sqlite')
cur = conn.cursor()

cur.execute('''SELECT id,state FROM STATE''')

myclient = pymongo.MongoClient("mongodb://localhost:27017")

mydb = myclient["coviddb"]
mycol = mydb["coviddata"]
lst = []
for row in cur:
    (id, state) = row
    print(id,state)
    lst.append(row)

state_id = int(input('Enter state_id:'))

for row in lst:
    (id, state) = row
    if id == state_id:
        state_to_search = state
        break

cur.execute('SELECT id,city FROM CITY WHERE state_id=?',(state_id,))

lst = []
for row in cur:
    (id, city) = row
    print(id,city)
    lst.append(row)

city_id = int(input('Enter city_id:'))

for row in lst:
    (id, city) = row
    if id == city_id:
        city_to_search = city
        break

print(city_to_search)
myquery = {"id": city_to_search,"state": state_to_search }

mydoc = mycol.find(myquery)

for x1 in mydoc:
    data = x1['data']

active_y = []
date_x = []
recovered_y = []
confirmed_y = []
for row in data:
    active_y.append(row['active'])
    date_x.append(row['date'])
    recovered_y.append(row['recovered'])
    confirmed_y.append(row['confirmed'])
# plotting the points
plt.plot(date_x, active_y,label = "active")
plt.plot(date_x,recovered_y,label = "recovered")
plt.plot(date_x,confirmed_y,label = "confirmed")
# naming the x axis
plt.xlabel('Date')
# naming the y axis
plt.ylabel('Cases')

# show a legend on the plot
plt.legend()

# giving a title to my graph
plt.title('Data of '+city_to_search+','+state_to_search)

# function to show the plot
plt.show()

