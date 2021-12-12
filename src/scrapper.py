import os
import time
import tweepy
import pandas as pd
from os import getenv


consumer_key = getenv('tweepy_consumer_key')
consumer_secret = getenv('tweepy_consumer_secret')
access_token = getenv('tweepy_access_token')
access_token_secret = getenv('tweepy_access_secret')
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
print(tweepy.__version__)

def search():
    user = ''
    search_user = api.search_users(input("Username: "), count=10)

    if len(search_user) > 1:
        for index, users in enumerate(search_user, start=1):
            print(index, users.screen_name)
        search()

    else:
        for users in search_user:
            print("Username :", users.name)
            print("Display name :", users.screen_name)
            print("Location :", users.location)
            print("Bio :", users.description)
            print("Followers :", users.followers_count)
            print("Following :", users.friends_count)
            print("Account birthdate :", users.created_at)
            print()
            user = users
    return user

_count = 150
try:
    user = search()
    tweets = tweepy.Cursor(api.user_timeline, user_id=user.id).items(_count)
    tweets_list = [[tweet.created_at, tweet.text] for tweet in tweets]
    tweets_df = pd.DataFrame(tweets_list)
    print(tweets_df)

except BaseException as e:
    print('failed on_status,', str(e))
    time.sleep(3)