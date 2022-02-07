from multiprocessing.connection import Client
from flask import render_template, request, redirect, Response, Flask, session
from pytest import Session
from scripts.preprocess import models_script
from scripts.tweepy_api import tweetox
from scripts.wordcld import WORDCLOUD
# from scripts.errors import defaultHandler
from flask.helpers import url_for
from scripts import Clients, Clients_Data, app
from scripts import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import pandas as pd

userent = []
tweets = []
tweets_sentiment = []


@app.route("/", methods=["POST", "GET"])
@app.route("/home", methods=["POST", "GET"])
def home_page():
    tweets.clear()
    print('[+] Clean User and Tweets Cache')
    if request.method == "POST":
        _username = request.form.get("username")
        client = Clients(username=_username)
        db.session.add(client)
        db.session.commit()

        ids = db.session.query(Clients.id).order_by(desc(Clients.date_added)).first()

        return redirect(url_for("result_page", var=ids[0]))
    else:
        return render_template('home.html')


@app.route("/about")
def about_page():
    tweets.clear()
    print('[+] Clean User and Tweets Cache')
    return render_template('about.html')


@app.route("/result/<var>", methods=['GET', 'POST'])
def result_page(var):

    usrname = db.session.query(Clients.username).filter(Clients.id == int(var)).first()

    _user = usrname[0]

    print(f'[+] Getting tweets of {_user}')
    _tweetscrap = None

    if str(_user).startswith('@'):
        global userent
        try:
            _tweetscrap, userent = (tweetox(_user).get_user_tweets())
        except Exception:
            raise defaultHandler
        
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

        js = _tweetmodels.to_json(orient='columns')
        
        db.session.add(Clients_Data(tweetmodel=js, user_id=int(var)))
        db.session.commit()

        _color = ''
        _sentiment = ''
        if _accountsentiment == 'POSITIVE':
            _color = 'rgba(22, 160, 133, 0.78)'
            _sentiment = f'Yeah, {_user} is pretty cool'
        else:
            _color = 'rgba(255, 99, 71, 0.78)'
            _sentiment = f'{_user} needs a day off of Twitter. Or a week. Or a month.'

        return render_template('result.html', username=usrname[0], account_sentiment=_sentiment, color=_color)


@app.route("/result/details")
def resultdetails_page():
    Items = []
    WRDCLOUD = []
    if userent is None:

        for tweet in tweets:
            # dataframe
            Items = [(a, b, c) for a, b, c in zip(tweet['original text'], tweet['sentiment'], tweet['confidence'])]

            # Wordcloud
            WRDCLOUD = WORDCLOUD(tweet)

        data = []
        for twt in tweets_sentiment:
            POSITIVE = int(twt.query("final_sentiment == 'POSITIVE'")["sentiment"])
            NEGATIVE = int(twt.query("final_sentiment == 'NEGATIVE'")["sentiment"])
            data = {'Sentiment': 'Count', 'Positive': POSITIVE, 'Negative': NEGATIVE}

        return render_template('result_details.html', items=Items, dashboardPie=data, dashboardWC=WRDCLOUD)

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
        
        # with open('scripts/static/bootstrap/img/pp.jpg', 'wb') as handle:
        #     response = requests.get(_profile_pic, stream=True)
        #     if not response.ok:
        #         print(response)
        #     for block in response.iter_content(1024):
        #         if not block:
        #             break
        #         handle.write(block)
    
        for tweet in tweets:
            # dataframe
            Items = [(a, b, c) for a, b, c in zip(tweet['original text'], tweet['sentiment'], tweet['confidence'])]

            # Wordcloud
            WRDCLOUD = WORDCLOUD(tweet)

        data = []
        for twt in tweets_sentiment:
            POSITIVE = int(twt.query("final_sentiment == 'POSITIVE'")["sentiment"])
            NEGATIVE = int(twt.query("final_sentiment == 'NEGATIVE'")["sentiment"])
            data = {'Sentiment': 'Count', 'Positive': POSITIVE, 'Negative': NEGATIVE}

        return render_template('user_details.html',
                               items=Items,
                               dashboardPie=data,
                               dashboardWC=WRDCLOUD,
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
        return response
