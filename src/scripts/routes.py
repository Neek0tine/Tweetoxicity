from multiprocessing.connection import Client
from flask import render_template, request, redirect, Response
from scripts.preprocess import models_script
from scripts.tweepy_api import tweetox
from scripts.wordcld import WORDCLOUD
from scripts.errors import defaultHandler
from flask.helpers import url_for
from scripts import Clients, Clients_Data, Clients_Input, app
from scripts import db
from sqlalchemy import desc
import pandas as pd
import json



@app.route("/", methods=["POST", "GET"])
@app.route("/home", methods=["POST", "GET"])
def home_page():
    print('[+] Analyzing...')
    if request.method == "POST":
        _username = request.form.get("username")
        db.session.add(Clients(username=_username))
        db.session.commit()

        unique_id = db.session.query(Clients.user_id).order_by(desc(Clients.date_added)).first()

        return redirect(url_for("result_page", var=unique_id[0]))
    else:
        return render_template('home.html')


@app.route("/about")
def about_page():
    return render_template('about.html')


@app.route("/result/<var>", methods=['GET', 'POST'])
def result_page(var):
    usrname = db.session.query(Clients.username).filter(Clients.user_id == int(var)).first()
    _user = usrname[0]
    print(_user)

    print(f'[+] Getting tweets of {_user}')
    if str(_user).startswith('@'):
        _tweetscrap, userent = (tweetox(_user, var).get_user_tweets())

        js1 = _tweetscrap.to_json()

        db.session.add(Clients_Input(
            tweetscrap = js1,
            user_id = var
        ))

        # Query db
        CLIENT_INPUT = db.session.query(Clients_Input).filter(Clients_Input.user_id == int(var)).first()

        if CLIENT_INPUT.tweetscrap is None:
            print('[!] Could not find user timeline')
        else:
            pass

    else:
        _tweetscrap = tweetox(_user, var).get_tweets()

        js1 = _tweetscrap.to_json()

        db.session.add(Clients_Input(
            tweetscrap = js1,
            user_id = var
        ))

        # Query db
        CLIENT_INPUT = db.session.query(Clients_Input).filter(Clients_Input.user_id == int(var)).first()

        if CLIENT_INPUT.tweetscrap is None:
            print('[!] Could not find any tweets related to tag!')
        else:
            pass
    

    CLIENT_INPUT = db.session.query(Clients_Input).filter(Clients_Input.user_id == int(var)).first()
    if CLIENT_INPUT.tweetscrap is None:
        print('[!] User/Tag doesnt have tweets')
        return render_template('tweets_null.html', username=_user)
    else:
        if request.method == 'POST':
            return redirect(url_for("resultdetails_page", var=int(var)))
        else:
            # db
            CLIENT_INPUT = db.session.query(Clients_Input).filter(Clients_Input.user_id == int(var)).first()
            TWEETSCRAP = CLIENT_INPUT.tweetscrap
            _tweetscrap_json = json.loads(TWEETSCRAP)
            _tweetscrap_json_normalize = pd.json_normalize(_tweetscrap_json['Text'])
            
            tweetscrap = _tweetscrap_json_normalize.melt(var_name=['id'])

            tweetscrap = tweetscrap.rename({'value':'Text'},axis=1)

            # Model
            _tweetmodels, _accountsentiment, _sentimentcount = models_script(tweetscrap)


            # db
            POSITIVE = int(_sentimentcount.query("final_sentiment == 'POSITIVE'")["sentiment"])
            NEGATIVE = int(_sentimentcount.query("final_sentiment == 'NEGATIVE'")["sentiment"])

            js = _tweetmodels.to_json(orient='columns')

            CLIENT_INPUT.tweetmodel = js
            CLIENT_INPUT.positive = POSITIVE
            CLIENT_INPUT.negative = NEGATIVE
            CLIENT_INPUT.user_id = var

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


@app.route("/result/<var>/details", methods=['GET', 'POST'])
def resultdetails_page(var):
    CLIENT = db.session.query(Clients).filter(Clients.user_id == int(var)).first()
    CLIENT_INPUT = db.session.query(Clients_Input).filter(Clients_Input.user_id == int(var)).first()
    CLIENT_DATA = db.session.query(Clients_Data).filter(Clients_Data.user_id == int(var)).first()
    if request.method == 'POST':
        return redirect(url_for('download_page', var=int(var)))
    else:
        if not str(CLIENT.username).startswith('@'):
            
            # db
            TWEETMODEL = CLIENT_INPUT.tweetmodel
            tweetmodel_json = json.loads(TWEETMODEL)

            # original Text
            original_text = pd.json_normalize(tweetmodel_json['original text'])
            original_text = original_text.melt(var_name=['id'])

            # clean Text
            clean_text = pd.json_normalize(tweetmodel_json['clean text'])
            clean_text = clean_text.melt(var_name=['id'])

            #  Sentiment
            sentiment = pd.json_normalize(tweetmodel_json['sentiment'])
            sentiment = sentiment.melt(var_name=['id'])

            #  Confidence
            confidence = pd.json_normalize(tweetmodel_json['confidence'])
            confidence = confidence.melt(var_name=['id'])

            Items = [(a, b, c) for a, b, c in zip(original_text['value'], sentiment['value'], confidence['value'])]

            WRDCLOUD = WORDCLOUD(clean_text)

            POSITIVE = CLIENT_INPUT.positive
            NEGATIVE = CLIENT_INPUT.negative

            data = {'Sentiment': 'Count', 'Positive': POSITIVE, 'Negative': NEGATIVE}

            return render_template('result_details.html', items=Items, dashboardPie=data, dashboardWC=WRDCLOUD)

        else:

            _profile_pic = CLIENT_DATA.user_pic
            _screen_name = CLIENT_DATA.screen_name
            _name = CLIENT_DATA.user_name
            _location = CLIENT_DATA.user_location
            _description = CLIENT_DATA.user_bio

            def human_format(num):
                num = float('{:.3g}'.format(num))
                magnitude = 0
                while abs(num) >= 1000:
                    magnitude += 1
                    num /= 1000.0
                return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

            _followers = human_format(CLIENT_DATA.user_followers)
            _friends = human_format(CLIENT_DATA.user_following)
            _birth = CLIENT_DATA.user_birth

            TWEETMODEL = CLIENT_INPUT.tweetmodel
            tweetmodel_json = json.loads(TWEETMODEL)

            # original Text
            original_text = pd.json_normalize(tweetmodel_json['original text'])
            original_text = original_text.melt(var_name=['id'])

            # clean Text
            clean_text = pd.json_normalize(tweetmodel_json['clean text'])
            clean_text = clean_text.melt(var_name=['id'])

            #  Sentiment
            sentiment = pd.json_normalize(tweetmodel_json['sentiment'])
            sentiment = sentiment.melt(var_name=['id'])

            #  Confidence
            confidence = pd.json_normalize(tweetmodel_json['confidence'])
            confidence = confidence.melt(var_name=['id'])


            Items = [(a, b, c) for a, b, c in zip(original_text['value'], sentiment['value'], confidence['value'])]

            WRDCLOUD = WORDCLOUD(clean_text)

            POSITIVE = CLIENT_INPUT.positive
            NEGATIVE = CLIENT_INPUT.negative

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
        


@app.route("/result/<var>/details/download", methods=['GET', 'POST'])
def download_page(var):
    CLIENT_INPUT = db.session.query(Clients_Input).filter(Clients_Input.user_id == int(var)).first()

    # db
    TWEETMODEL = CLIENT_INPUT.tweetmodel
    tweetmodel_json = json.loads(TWEETMODEL)

    # original Text
    original_text = pd.json_normalize(tweetmodel_json['original text'])
    original_text = original_text.melt(var_name=['id'])

    # clean Text
    clean_text = pd.json_normalize(tweetmodel_json['clean text'])
    clean_text = clean_text.melt(var_name=['id'])

    #  Sentiment
    sentiment = pd.json_normalize(tweetmodel_json['sentiment'])
    sentiment = sentiment.melt(var_name=['id'])

    #  Confidence
    confidence = pd.json_normalize(tweetmodel_json['confidence'])
    confidence = confidence.melt(var_name=['id'])

    #merge
    df_final = pd.concat([original_text['value'], clean_text['value'], sentiment['value'], confidence['value']],axis=1)
    columns = ['Original Text', 'Clean Text', 'Sentiment', 'Confidence']
    df_final.columns = columns

    response = Response(df_final.to_csv(), mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=data.csv'

    return response
