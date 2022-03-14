from re import A
import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://briandb:admin@cluster0.ahs6b.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["briandb"]
collection = db["briancollection"]

tweet = []

table = "<tr><td>username</td><td>created_at</td><td>tweet</td><td>location</td>"
tweet.append(table)

for tweets in collection.find():
    a = "<tr><td>%s</td>" %tweets['username']
    tweet.append(a)
    b = "<tr><td>%s</td>" %tweets['created_at']
    tweet.append(b)
    c = "<tr><td>%s</td>" %tweets['tweet']
    tweet.append(c)
    d = "<tr><td>%s</td>" %tweets['location']
    tweet.append(d)
    

print(tweet)