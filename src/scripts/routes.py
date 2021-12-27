from flask import render_template, request, redirect, send_file
from scripts.preprocess import models_script
from scripts.tweepy_api import tweetox
# from .errors import defaultHandler
from flask.helpers import send_from_directory, url_for
from scripts import app
import os


user = []


@app.route("/", methods=["POST", "GET"])
@app.route("/home", methods=["POST", "GET"])
def home_page():
    if request.method == "POST":
        username = request.form.get("username")
        user.append(str(username))
        return redirect(url_for("result_page", user=username))
    else:
        return render_template('home.html')


@app.route("/about")
def about_page():
    return render_template('about.html')


tweets = []


@app.route("/home/result/<user>")
def result_page(user):
    print(f'[+] Getting tweets of {user}')
    _tweetscrap = ''

    if str(user).startswith('@'):

        _tweetscrap = (tweetox(user).get_user_tweets())[0]

        # try:
        #     _tweetscrap = (tweetox(user).get_user_tweets())[0]
        # except Exception:
        #     raise defaultHandler

        if _tweetscrap is None:
            print('[!] Could not find user timeline')
            _tweetscrap = None
        else:
            pass

    else:
        _tweetscrap = tweetox(user).get_tweets()
        if _tweetscrap is None:
            print('[!] Could not find any tweets related to tag!')
            _tweetscrap = None
        else:
            pass

    if _tweetscrap.empty:
        print('[!] User/Tag doesnt have tweets')
        return render_template('tweets_null.html', username=user)
    else:
        _tweetmodels, _accountsentiment = models_script(_tweetscrap)
        tweets.append(_tweetmodels)

        _color = ''
        if _accountsentiment == 'POSITIVE':
            _color = 'rgba(22, 160, 133, 0.78)'
        else:
            _color = 'rgba(255, 99, 71, 0.78)'

        return render_template('result.html', username=user, account_sentiment=_accountsentiment, color=_color)


@app.route("/home/result/details")
def resultdetails_page():
    Items = []
    for tweet in tweets:
        _username = "".join([usr for usr in user])
        _filename = fr"scripts\tweets\Tweets_of_{_username}.csv"
        _tocsv = tweet.to_csv(_filename)
        Items = [(a, b, c) for a, b, c in zip(tweet['original text'], tweet['sentiment'], tweet['confidence'])]

    return render_template('resultdetails.html', items=Items)


@app.route("/download")
def download():
    users = "".join([i for i in user])
    _filenames = fr"tweets\Tweets_of_{users}.csv"
    
    return send_file(_filenames, as_attachment=True)