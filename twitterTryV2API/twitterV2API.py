import mysql.connector
from mysql.connector import Error
import tweepy

client = tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAMcEZwEAAAAAAUEgRAIUFieKhK4LftXXK19NvJ4%3DXWU0rt3fkkHZ6fWBuoCslty0bigCv4jrQfXAwGR8saT2FcbzAT")


def connect(username, created_at, tweet, location):
    try:
        connection = mysql.connector.connect(host='localhost',
                                         database='twitterdb',
                                         user='root',
                                         password='admin')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

            #This is so we can check if out databse has 10 tweets storted
            query2 =  "SELECT COUNT(*) FROM twitterdb.tweet"
            cursor.execute(query2)
            rowcount = cursor.fetchone()[0]

            #if 10 tweets are stored delete the oldest one.
            if rowcount >= 10:
                query3 = "Select min(idtweet) from tweet"
                cursor.execute(query3)
                smallestID = cursor.fetchone()
                query4 = "delete from twitterdb.tweet where idtweet = %s"
                cursor.executemany(query4, (smallestID, ))
            #insert new tweet into database
            query = """INSERT INTO tweet (username, created_at, tweet, location) VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, (username, created_at, tweet, location))
            connection.commit()

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


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
        connect(user.username, tweet.created_at, tweet.text, user.location)



