from scripts import app
from flask import request, render_template
from .tweepy_api import get_user_tweets


@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == "POST":
        username = request.form.get("uname")
        result = get_user_tweets(username)
        result = result.to_html()
        return result

    return render_template('base.html')



