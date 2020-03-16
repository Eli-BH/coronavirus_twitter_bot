import praw
import tweepy
import time
import tkinter
import pandas as pd
import datetime as dt
import time
from bs4 import BeautifulSoup as bs
import csv 

client_id = -
client_secret = -
user_agent = -
username = -
password = -

reddit = praw.Reddit(
    client_id = client_id,
    client_secret = client_secret,
    user_agent = user_agent,
    username = -
    password = -
    )


subred = reddit.subreddit("coronavirus")

hot = subred.hot(limit=10)
new = subred.new(limit=2)
controv = subred.controversial(limit=10)
top = subred.top(limit=10)
gilded = subred.top(limit=10)

x = next(new)
posts = {
    'title':[],
    'url':[],
    'author':[],
    'created':[]
}


consumer_key = -
consumer_secret = -
access_token = -
access_token_secret = -

auth = tweepy.OAuthHandler(
    consumer_key,
    consumer_secret,
)

auth.set_access_token(
    access_token,
    access_token_secret,
)
api = tweepy.API(auth)
user = api.me()


def new_tweet():
    while True:
        try:
            for submission in reddit.subreddit('coronavirus').stream.submissions():
                api.update_status(
                    str(submission.title) + '\n' +
                    str(submission.url) + '\n'+
                    'reddit user:'+
                    str(submission.author)
                )
                print('tweeted')
                time.sleep(300)
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            pass
        
new_tweet()