from flask.helpers import url_for
from scripts import app
from flask import render_template, request, redirect
from scripts.tweepy_api import get_user_tweets
from scripts.preprocess import models_script

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
    tweetscrap = get_user_tweets(user)
    tweetmodels, accountsentiment = models_script(tweetscrap)
    tweets.append(tweetmodels)
    return render_template('result.html', username=user, account_sentiment=accountsentiment)

@app.route("/home/result/details")
def resultdetails_page():
    for tweet in tweets:
        Items = [(a,b,c) for a,b,c in zip(tweet['original text'], tweet['sentiment'], tweet['confidence'])]
    return render_template('resultdetails.html', items=Items)