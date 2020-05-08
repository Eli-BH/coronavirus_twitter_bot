import praw
import tweepy
import time
import requests
from bs4 import BeautifulSoup as bs




with open('api_info.csv') as api_info:
    reader = csv.reader(api_info)
    api_data = dict(reader)

#enter your information from the reddit dev dashboard
client_id = api_data['reddit_client_id']
client_secret = api_data['reddit_client_secret']
user_agent = api_data['reddit_user_agent']
username = api_data['reddit_username']
password = api_data['reddit_password']

reddit = praw.Reddit(
    client_id = client_id,
    client_secret = client_secret,
    user_agent = user_agent,
    username = username,
    password = password
    )

# choose your subreddit
subred = reddit.subreddit("coronavirus")

#enter your consumer tokens here from the twitter dev dashboard
consumer_key = api_data['twitter_consumer_key']
consumer_secret = api_data['twitter_consumer_secret']
access_token = api_data['twitter_access_token']
access_token_secret = api_data['twitter_access_token_secret']

#oath info
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
    """function that takes a stream from a subreddit api praw
    and posts it with the tweepy api"""
    while True:
        try:
            for submission in reddit.subreddit('coronavirus').stream.submissions():
                    #updates twitter status with the title of the post and url in the post
                    #credit the poster with submission.author
                    api.update_status(
                        str(submission.title) + '\n' +
                        str(submission.url) + '\n'+
                        "report misinformation to @eli_b_goode by DM"+"\n"+
                        "#covid19 #stayhome"
                    )
                    print("article posted")
                    time.sleep(600)



        except tweepy.TweepError as e:
            print(e.reason)
            time.sleep(30)

        except StopIteration:
            pass


new_tweet()
