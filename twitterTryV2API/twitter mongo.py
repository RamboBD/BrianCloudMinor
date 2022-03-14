import pymongo
from pymongo import MongoClient
import tweepy

client = tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAMcEZwEAAAAAAUEgRAIUFieKhK4LftXXK19NvJ4%3DXWU0rt3fkkHZ6fWBuoCslty0bigCv4jrQfXAwGR8saT2FcbzAT")

cluster = MongoClient("mongodb+srv://briandb:admin@cluster0.ahs6b.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["briandb"]
collection = db["briancollection"]
collection.delete_many({})

query = "#Dota OR #Dota2 -is:retweet"

response = client.search_recent_tweets(query=query, max_results=10,
    tweet_fields=['created_at', 'lang', 'public_metrics', 'geo'],
    user_fields=['location', 'created_at'],
    expansions=['author_id'])

users = {u['id']: u for u in response.includes['users']}

print(response)

for tweet in response.data:
    if users[tweet.author_id]:
        user = users[tweet.author_id]
        print(user.username) 
        print(tweet.created_at)
        print(tweet.text)
        print(user.location) 
        print(tweet.public_metrics) 
          
for tweet in response.data:
    post = {"username": user.username, "created_at": tweet.created_at, "tweet": tweet.text, "location": user.location} 
    collection.insert_one(post)

print(post) 