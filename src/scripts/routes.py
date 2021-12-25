from flask import render_template, request, redirect
from scripts.preprocess import models_script
from flask.helpers import url_for
from scripts.tweepy_api import tweetox
from scripts import app


@app.route("/", methods=["POST", "GET"])
@app.route("/home", methods=["POST", "GET"])
def home_page():
    if request.method == "POST":
        username = request.form.get("username")
        return redirect(url_for("result_page", user=username))
    else:
        return render_template('home.html')


tweets = []


@app.route("/home/result/<user>")
def result_page(user):
    print(f'[+] Getting tweets of {user}')
    _tweetscrap = ''

    if str(user).startswith('@'):
        _tweetscrap = (tweetox(user).get_user_tweets())[0]
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
        Items = [(a, b, c) for a, b, c in zip(tweet['original text'], tweet['sentiment'], tweet['confidence'])]

    return render_template('resultdetails.html', items=Items)
