from scripts import app
from flask import render_template
import pandas as pd

@app.route('/')
def home_page():
    return render_template('base.html')

@app.route('/table')
def table_page():
    textfile = pd.read_csv('./models/data/elonmusk_tweets.csv')
    items = [(a,b,c) for a,b,c in zip(textfile['original text'], textfile['sentiment'], textfile['confidence'])]
    
    return render_template('table.html', items=items)