from flask.helpers import url_for
from scripts import app
from flask import render_template, request, redirect
from scripts.tweepy_api import get_user_tweets
from scripts.preprocess import tweetoxicity

@app.route("/", methods=["POST", "GET"])
@app.route("/home", methods=["POST", "GET"])
def home_page():
    if request.method == "POST":
        username = request.form.get("username")
        return redirect(url_for("result_page", user=username))
    else:
        return render_template('home.html')

username = []
@app.route("/home/result/<user>")
def result_page(user):
    username.append(user)
    return render_template('result.html')

@app.route("/home/result/details")
def resultdetails_page():
    tweetscrap = get_user_tweets(username)
    tweetmodels = tweetoxicity(tweetscrap)
    datas = [(a,b,c) for a,b,c in zip(tweetmodels['original text'], tweetmodels['sentiment'], tweetmodels['confidence'])]
    return render_template('resultdetails.html', items=datas)