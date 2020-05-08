import praw
import tweepy
import time
import requests
from bs4 import BeautifulSoup as bs
import csv
import datetime

#Authenticate Twitter information
#tweepy.Oauthhandlr(consumer key, consumer scret)
#set_access_token(access_token, access token secret)

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
#api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#You can invoke this object's methods to do any API call.

#try:
#    api.verify_credentials()
#    print("Authentication OK")
#except:
#    print("Error during authentication ")

#tweet_pub = "This is testing tweet number 1"
#makes a new post
#api.update_status(tweet_pub)

#api.update_status("https://www.reddit.com/r/wallpapers/comments/fdceg9/see_you_later_7680x4320/")

#status is a tweet
#friendship is a follow-follower relationship
#favorite is a like

#def retweet():
#    """function to search for puppies tweets and followes and retweets them"""
#    search=('puppies')
#    NumTweets = 100
#    for tweet in tweepy.Cursor(api.search, search).items(NumTweets):
#    error handeling so it doesnt retweet the same thing twice
#        try:
#            tweet.retweet()
#            tweet.favorite()
#            tweet.create_friendship()
#
#            print('retweeted')
#            time.sleep(5)

#        except tweepy.TweepError as e:
#            print(e.reason)
#        except StopIteration:
#            breakpoint or pass

#tracker info
URL = 'https://www.google.com/covid19-map/'
page = requests.get(URL)

soup = bs(page.content, 'lxml')

tot_confirmed = soup.find_all('td', {"class": "l3HOY"})[0].text
tot_recovered = soup.find_all('td', {"class": "l3HOY"})[2].text
tot_deaths = soup.find_all('td', {"class": "l3HOY"})[3].text

us_confirmed = soup.find_all('td', {"class": "l3HOY"})[4].text
us_recoverd = soup.find_all('td', {"class": "l3HOY"})[6].text
us_deaths = soup.find_all('td', {"class": "l3HOY"})[7].text

#ny values
ny_URL = 'https://www.worldometers.info/coronavirus/country/us/'
ny_page = requests.get(ny_URL)

ny_soup = bs(ny_page.content, 'lxml')

ny_tot_confirmed = ny_soup.find_all('td')[12].text.strip()
ny_tot_deaths = ny_soup.find_all('td')[14].text.strip()


#emoji list
am = '\U0001F691'
world = '\U0001F30E'
usa = '\U0001F1FA\U0001F1F8'
heart = '\U0001F493'
skull = '\U0001F480'
mask = '\U0001F637'
statue = '\U0001F5FD'
fever = '\U0001F912'
filename = 'last_seen.txt'

def read_last_seen(filename):
    file_read = open(filename, 'r')
    last_seen_id = int(file_read.read().strip())
    file_read.close()
    return last_seen_id

def store_last_seen(filename, last_seen_id):
    file_write = open(filename, 'w')
    file_write.write(str(last_seen_id))
    file_write.close()
    return
curTime = datetime.datetime.now().strftime("%b %d, %Y %I:%M:%S %p")
#adding the id in here means only only the tweets after id
#this tweets is only looking in my mentions
def reply():
    tweet = api.mentions_timeline(read_last_seen(filename), tweet_mode='extended')
    for tweet in reversed(tweet):
        # lookinf for specific tag in the bots tweets
        # case specific convert tweet.text.lower() to search for all by lowercase
        print('tweet found')
        name = "@" + tweet.user.screen_name
        stat = " As of "+ curTime + "\n"
        stat += usa+mask +"US confirmed cases: " + us_confirmed +'\n'
        stat += usa+heart + "US Recovered cases: " + us_recoverd + '\n'
        stat += usa+skull+ "US deaths: "+ us_deaths
        print('Replied To ID' + '- ' + name + tweet.full_text)


        ny_stat = " As of " + curTime + "\n"
        ny_stat += statue + mask + "NYC confirmed cases: "+ ny_tot_confirmed + '\n'
        ny_stat += statue + skull + "NYC deaths total: " + ny_tot_deaths

        if ('ny' or 'NY' or 'Ny' or 'NYC' or 'nyc' or 'New York') in tweet.full_text:
            api.update_status(status= name + ny_stat, in_reply_to_status_id = tweet.id)
        else:
            api.update_status(status = name + stat , in_reply_to_status_id=tweet.id)
#        tweet.retweet()
#        tweet.favorite()
#        api.create_friendship(tweet.user.screen_name)
        store_last_seen(filename, tweet.id)




while True:
    reply()
    time.sleep(300)