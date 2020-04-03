import praw
import tweepy
import time
import requests
from bs4 import BeautifulSoup as bs
import csv


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

#tracker info
URL = 'https://www.google.com/covid19-map/'
page = requests.get(URL)

soup = bs(page.content, 'lxml')

tot_confirmed = soup.find_all('td', {"class": "uMsnNd HAChlc"})[0].text
tot_recovered = soup.find_all('td', {"class": "uMsnNd HAChlc"})[2].text
tot_deaths = soup.find_all('td', {"class": "uMsnNd HAChlc"})[3].text

us_confirmed = soup.find_all('td', {"class": "uMsnNd HAChlc"})[4].text
us_recoverd = soup.find_all('td', {"class": "uMsnNd HAChlc"})[6].text
us_deaths = soup.find_all('td', {"class": "uMsnNd HAChlc"})[7].text

#emoji list
am = '\U0001F691'
world = '\U0001F30E'
usa = '\U0001F1FA\U0001F1F8'
heart = '\U0001F493'
skull = '\U0001F480'
mask = '\U0001F637'





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
                    'reddit user:'+
                    str(submission.author) +'\n\n' +
                    "Please practice social distancing, and wash your hands." + '\n'+
                    "repost to spread awareness"+"\n"+
                    "#corona #covid19 #coronavirus #stayhome"
                )

                api.update_status(
                    world+mask + "Total confirmed cases: " + tot_confirmed + '\n'+
                    world+heart+ "Total recovered cases: " + tot_recovered + '\n'+
                    world+skull+ "Total deaths: " + tot_deaths + '\n\n'+
                    usa+mask+ "US confirmed cases: " + us_confirmed +'\n'+
                    usa+heart+ "US Recovered cases: " + us_recoverd + '\n'+ 
                    usa+skull+ "US deaths: "+ us_deaths + '\n'+
                    '\n\n'+
                    "#corona #covid19 #coronavirus #stayhome"
                )
                
                #tweet message to make sure that it is running 
                print('tweeted')
                time.sleep(300) #select the time between posts in seconds
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            pass
     
new_tweet()