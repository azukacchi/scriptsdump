import tweepy
import re
import time

## You should already have a Twitter developer account first
## with Read and Write permission
consumer_key = "YOUR KEY HERE"
consumer_secret = "YOUR KEY HERE"
access_token = "YOUR KEY HERE"
access_token_secret = "YOUR KEY HERE"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

twtlink = 'PASTE THE TWEET LINK WHICH RETWEETERS YOU WANT TO BLOCK'

regex = r'(?=twitter\.com\/(\w+)\/status\/(\d+))'
twtid = int(re.search(regex, twtlink).group(2))
user_name = re.search(regex, twtlink).group(1)

rtid = api.retweeters(twtid)

for id in rtid:
    api.create_block(id=id)
    #api.create_mute(id=id) IF YOU WANT TO ONLY MUTE THEM
    time.sleep(3)

api.create_block(screen_name=user_name)

print(f"Number of people who retweeted the tweets that you've blocked: {len(rtid)}")