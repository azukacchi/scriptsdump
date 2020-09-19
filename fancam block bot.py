import tweepy
import re
import time

## You should already have a Twitter developer account first

consumer_key = "YOUR KEY HERE"
consumer_secret = "YOUR KEY HERE"
access_token = "YOUR KEY HERE"
access_token_secret = "YOUR KEY HERE"



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

twtlink = '' # the link of the tweet which you want to block all the fancams, place inside the ' '
regex = r'(?=twitter\.com\/(\w+)\/status\/(\d+))'
twtid = int(re.search(regex, twtlink).group(2))
user_name = re.search(regex, twtlink).group(1)

tweets = tweepy.Cursor(api.search, q='to:{} filter:replies'.format(user_name), tweet_mode='extended', since_id=twtid).items()

### OPTIONAL
items = [] 
fancamreply = []
reply = set()
blocklist = set()
############

for tweet in tweets:
    if not hasattr(tweet,'in_reply_to_status_id'):
        continue
    if tweet.in_reply_to_status_id == twtid:
        items.append(tweet.id)
        reply.add(tweet.user.id)
        if not hasattr(tweet, 'extended_entities'):
            continue
        elif tweet.extended_entities['media'][0]['type'] == 'video':
            api.create_block(id=tweet.user.id)
            time.sleep(3)
            blocklist.add(tweet.user.screen_name)
            fancamreply.append(tweet.id)
            
            
### OPTIONAL            
print(f'Number of all public replies under the status: {len(items)}')
print(f'Number of people replying under the status: {len(reply)}')
print(f'Number of reply under the status with fancam: {len(fancamreply)}')
print(f'Number of people replying with fancams: {len(blocklist)}')
print(f'{blocklist}')
#############



