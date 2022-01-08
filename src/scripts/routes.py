import pandas as pd
from flask import render_template, request, redirect, Response
from scripts.preprocess import models_script
from scripts.tweepy_api import tweetox
from scripts.wordcld import WORDCLOUD
import requests
# from .errors import defaultHandler
from flask.helpers import send_from_directory, url_for
from scripts import app
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image


user = []
userent = []
tweets = []
tweets_sentiment = []


@app.route("/", methods=["POST", "GET"])
@app.route("/home", methods=["POST", "GET"])
def home_page():
    if request.method == "POST":
        _username = request.form.get("username")
        user.append(str(_username))
        return redirect(url_for("result_page"))
    else:
        user.clear()
        return render_template('home.html')


@app.route("/about")
def about_page():
    return render_template('about.html')


@app.route("/result")
def result_page():
    _user = "".join(user)
    print(f'[+] Getting tweets of {_user}')
    _tweetscrap = None

    if str(_user).startswith('@'):
        global userent
        _tweetscrap, userent = (tweetox(_user).get_user_tweets())


        # # try:
        # #     _tweetscrap = (tweetox(user).get_user_tweets())[0]
        # # except Exception as e:
        # #     raise defaultHandler

        if _tweetscrap is None:
            print('[!] Could not find user timeline')
            _tweetscrap = None
        else:
            pass

    else:
        userent = None
        _tweetscrap = tweetox(_user).get_tweets()
        if _tweetscrap is None:
            print('[!] Could not find any tweets related to tag!')
            _tweetscrap = None
        else:
            pass

    if _tweetscrap.empty:
        print('[!] User/Tag doesnt have tweets')
        return render_template('tweets_null.html', username=_user)
    else:
        _tweetmodels, _accountsentiment, _sentimentcount = models_script(_tweetscrap)
        tweets.append(_tweetmodels)
        tweets_sentiment.append(_sentimentcount)

        _color = ''
        if _accountsentiment == 'POSITIVE':
            _color = 'rgba(22, 160, 133, 0.78)'
        else:
            _color = 'rgba(255, 99, 71, 0.78)'

        return render_template('result.html', username=_user, account_sentiment=_accountsentiment, color=_color)


@app.route("/result/details")
def resultdetails_page():
    Items = []
    if userent is None:

        for tweet in tweets:
            # dataframe
            Items = [(a, b, c) for a, b, c in zip(tweet['original text'], tweet['sentiment'], tweet['confidence'])]

            # Wordcloud
            WORDCLOUD(tweet)

        data = []
        for twt in tweets_sentiment:
            POSITIVE = int(twt.query("final_sentiment == 'POSITIVE'")["sentiment"])
            NEGATIVE = int(twt.query("final_sentiment == 'NEGATIVE'")["sentiment"])
            data = {'Sentiment': 'Count', 'Positive': POSITIVE, 'Negative': NEGATIVE}

        return render_template('result_details.html', items=Items, dashboardPie=data)

    else:
        _profile_pic = str(userent.profile_image_url)
        _screen_name = userent.screen_name
        _name = userent.name
        _location = userent.location
        _description = userent.description

        def human_format(num):
            num = float('{:.3g}'.format(num))
            magnitude = 0
            while abs(num) >= 1000:
                magnitude += 1
                num /= 1000.0
            return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

        _followers = human_format(userent.followers_count)
        _friends = human_format(userent.friends_count)
        _birth = userent.created_at

        with open('scripts/static/bootstrap/img/pp.jpg', 'wb') as handle:
            response = requests.get(_profile_pic, stream=True)
            if not response.ok:
                print(response)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)

        for tweet in tweets:
            # dataframe
            Items = [(a, b, c) for a, b, c in zip(tweet['original text'], tweet['sentiment'], tweet['confidence'])]

            # Wordcloud
            WORDCLOUD(tweet)

        data = []
        for twt in tweets_sentiment:
            POSITIVE = int(twt.query("final_sentiment == 'POSITIVE'")["sentiment"])
            NEGATIVE = int(twt.query("final_sentiment == 'NEGATIVE'")["sentiment"])
            data = {'Sentiment': 'Count', 'Positive': POSITIVE, 'Negative': NEGATIVE}

        return render_template('user_details.html',
                               items=Items,
                               dashboardPie=data,
                               _profile_pic=_profile_pic,
                               _screen_name=_screen_name,
                               _name=_name,
                               _location=_location,
                               _description=_description,
                               _followers=_followers,
                               _friends=_friends,
                               _birth=_birth)


@app.route("/download")
def download():
    for tweet in tweets:
        response = Response(tweet.to_csv(), mimetype='text/csv')
        response.headers['Content-Disposition'] = 'attachment; filename=data.csv'
        user.clear()
        return response
