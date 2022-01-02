from os import getenv
import pandas as pd
import tweepy
from time import sleep


class tweetox:
    def __init__(self, query):

        self.query = query

        try:
            print('[+] Authenticating ...')
            consumer_key = getenv('tweepy_consumer_key')
            print("[+] Consumer key [OK]")
            consumer_secret = getenv('tweepy_consumer_secret')
            print("[+] Consumer secret [OK]")
            access_token = getenv('tweepy_access_token')
            print("[+] API Access token [OK]")
            access_token_secret = getenv('tweepy_access_secret')
            print("[+] API Secret [OK]")
            print("[+]  -- Authenticated --")

            try:
                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_token, access_token_secret)
                self.api = tweepy.API(auth, wait_on_rate_limit=True)
                return

            except Exception as e:
                print(f"[!] Fail to authenticate bot client. Are you sure the tokens are correct? ({e.args})")

        except Exception as e:
            print(f"[!] Error on acquiring tokens. Are you sure they are set properly? ({e.args})")



    def get_user_tweets(self):
        '''
        This function obtain last 150 tweets of inputted user.

        :returns: DataFrame, tweepy.user or None
        '''

        _query = self.query
        _api = self.api
        _count = 150


        def get_user(query):
            print(f'\n[+] Searching for user:', query)
            _search_result = []
            _user = ''

            try:
                _search_result = _api.search_users(query, count=20)
                _user = _search_result[0]
                print(f'[+] User found! {_user.screen_name}\n')
            except:
                print('[!] Could not find user using batch search. Trying targeted search.')
                _search_result = _api.get_user(user_id=query)
                _user = _search_result[0]

            print("\n" + "-" * 40, f"\nShowing profile of {_user.screen_name}")
            print("Display name :", _user.name)
            print("Location :", _user.location)
            print("Bio :", _user.description)
            print("Followers :", _user.followers_count)
            print("Following :", _user.friends_count)
            print("Account birthdate :", _user.created_at, "\n" + "-" * 40, "\n")

            return _user

        try:
            _user = get_user(_query)
            print(f'[+] Collecting tweets and retweets from {_user.screen_name}\n')
            _tweets = tweepy.Cursor(_api.user_timeline, user_id=_user.id).items(_count)
            _tweets_list = [[_tweet.created_at, _tweet.text] for _tweet in _tweets]
            _tweets_df = pd.DataFrame(_tweets_list, columns=['TimeStamp', 'Text'])
            # _tweets_df.to_csv(f'/scripts/tweets/Tweets_of_{_query}.csv')
            return _tweets_df, _user

        except BaseException as e:
            print('[!] Could not get specified user timeline,', str(e))
            return e




    def get_tweets(self):
        '''
        This bad boy searches all Tweets from all corners of Twitter.

        :return: DataFrame or None
        '''

        _query = self.query
        _api = self.api
        _count = 100

        try:
            _tweets = _api.search_tweets(_query, count=_count)
            _tweets = [[_tweet.created_at, _tweet.text] for _tweet in _tweets]
            _tweets_df = pd.DataFrame(_tweets, columns=['TimeStamp', 'Text'])
            # _tweets_df.to_csv(f'/scripts/tweets/Tweets_of_{_query}.csv')
            return _tweets_df
        except Exception as e:
            print(f'[!] Could not get any result ({e})')
            return None

if __name__== "__main__":
    print("┌" + "─" * 64 + "┐")
    print("""     _____              _                                   
    |_   _| _ _ ___ ___| |_ ___ ___ ___ ___ ___ ___ ___ ___ 
      | || | | | -_| -_|  _|_ -|  _|  _| .'| . | . | -_|  _|
      |_||_____|___|___|_| |___|___|_| |__,|  _|  _|___|_|  
                                           |_| |_|          """)
    print("  Tweetscrapper version 1.2.0")
    print('  Tweepy version', tweepy.__version__)
    print('  Pandas version', pd.__version__)
    print("  https://github.com/Neek0tine/Tweetoxicity")
    print("└" + "─" * 64 + "┘")
    r = tweetox(input('input '))
    r.get_user_tweets()
