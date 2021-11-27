import steamspypi
import json
import psycopg2
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import re
import time

def insert_game(appid):
    #create data to insert
    data_request = dict()
    data_request['request'] = 'appdetails'
    data_request['appid'] = appid

    data = steamspypi.download(data_request)

    #appid
    appid = int(data['appid'])
    #name
    name = data['name']
    #developer
    developer = data['developer']
    developer = re.split(', ', developer)
    #publisher
    publisher = data['publisher']
    publisher = re.split(', ', publisher)
    #price
    price = int(data['price']) / 100
    #discount
    discount = data['discount']
    #positive
    positive = data['positive']
    #negative
    negative = data['negative']
    #genre
    genre = data['genre']
    genre = re.split(', ', genre)
    #tags
    tags = list(data['tags'].keys())

    # # print game details
    # print("%s\n" % appid)
    # print("%s\n" % name)
    # print("%s\n" % developer)
    # print("%s\n" % publisher)
    # print("%s\n" % price)
    # print("%s\n" % discount)
    # print("%s\n" % positive)
    # print("%s\n" % negative)
    # print("%s\n" % genre)
    # print("%s\n" % tags)

    #do query
    cur.execute("INSERT INTO product (product_id, name, developer, publisher, price, current_discount, positive_ratings, negative_ratings, genres, tags) \
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) \
        ON CONFLICT (product_id) \
        DO \
            UPDATE SET developer = EXCLUDED.developer, \
                    publisher = EXCLUDED.publisher, \
                    price = EXCLUDED.price, \
                    current_discount = EXCLUDED.current_discount, \
                    positive_ratings = EXCLUDED.positive_ratings, \
                    negative_ratings = EXCLUDED.negative_ratings, \
                    genres = EXCLUDED.genres, \
                    tags = EXCLUDED.tags;", (appid, name, developer, publisher, price, discount, positive, negative, genre, tags) )

con = psycopg2.connect(
        host="localhost", 
        database="steam",
        user="postgres",
        password="PNorthern1",
        port=5432
    )

cur = con.cursor()
#cursor

#grab appids of top 100 games
data_request = dict()
data_request['request'] = 'top100in2weeks'
data = steamspypi.download(data_request)

gappid = list(data.keys())
print(gappid)

#insert game details one by one into products table
for appid in gappid:
    print("inserting %s", appid)
    insert_game(appid)
    time.sleep(1)
    

con.commit()
#close cursor
cur.close()

#close connection
con.close()

# data_request = dict()
# data_request['request'] = 'appdetails'
# data_request['appid'] = '1088850'

# data = steamspypi.download(data_request)

# hello = data['tags'].keys()
# bye = list(hello)
# print(bye[1])