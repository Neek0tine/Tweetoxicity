from os import getenv
import pandas as pd
import tweepy
from time import sleep


def _init():
    try:
        print('Authenticating ...')
        consumer_key = getenv('tweepy_consumer_key')
        print("Consumer key [OK]")
        consumer_secret = getenv('tweepy_consumer_secret')
        print("Consumer secret [OK]")
        access_token = getenv('tweepy_access_token')
        print("API Access token [OK]")
        access_token_secret = getenv('tweepy_access_secret')
        print("API Secret [OK]")
        print(" -- Authenticated --")
    except Exception as e:
        print(f"API Access tokens are not inside systen environment variables. Please contact developer! ({e.args}")

    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        _api = tweepy.API(auth, wait_on_rate_limit=True)
        api = _api
    except Exception as e:
        print(f"Fail to authenticate user. Please try again later or contact developers! ({e.args})")

    return api


def get_user_stats(query=None):
    _user = None
    api = _init()
    if query is None:
        _query = input("Search : ")
    else:
        _query = query

    _search_result = api.search_users(_query, count=1)

    _user = _search_result[0]
    print("\n"+"-"*40,f"\nShowing profile of {_user.screen_name}")
    print("Display name :", _user.name)
    print("Location :", _user.location)
    print("Bio :", _user.description)
    print("Followers :", _user.followers_count)
    print("Following :", _user.friends_count)
    print("Account birthdate :", _user.created_at, "\n"+"-"*40, "\n")
    user = _user
    return user, api

def get_user_tweets(user=None):
    _user, api = get_user_stats(user)
    _count = 50

    try:
        tweets = tweepy.Cursor(api.user_timeline, user_id=_user.id).items(_count)
        tweets_list = [[tweet.created_at, tweet.text] for tweet in tweets]
        tweets_df = pd.DataFrame(tweets_list, columns=['TimeStamp', 'Text'])
        return tweets_df
        # tweets_df.to_csv(f'Tweets of {_user.screen_name}.csv', index=False)

    except BaseException as e:
        print('failed on_status,', str(e))
        sleep(3)
        get_user_tweets()


if __name__== "__main__":
    api = _init()
    print("┌" + "─" * 56 + "┐")
    print("""  _____              _                                   
    |_   _| _ _ ___ ___| |_ ___ ___ ___ ___ ___ ___ ___ ___ 
      | || | | | -_| -_|  _|_ -|  _|  _| .'| . | . | -_|  _|
      |_||_____|___|___|_| |___|___|_| |__,|  _|  _|___|_|  
                                           |_| |_|          """)
    print("  Tweetscrapper version 1.1")
    print('  Tweepy version', tweepy.__version__)
    print("  https://github.com/Neek0tine/Tweetoxicity")
    print("└" + "─" * 56 + "┘")