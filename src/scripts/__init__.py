from lib2to3.pytree import Base
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from random import randint
from datetime import datetime
from sqlalchemy import JSON

def random_integer():
    min_ = 100
    max_ = 1000000
    rand = randint(min_, max_)

    return int(rand)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///client.db'
db = SQLAlchemy(app)

class Clients(db.Model):
    id = db.Column(db.Integer,default=random_integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    post = db.relationship('Clients_Data', backref='author', lazy=True)

    def __repr__(self):
        return f'{self.id} - {self.username} - {self.date_added}'

class Clients_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tweetmodel = db.Column(db.JSON())
    user_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)

    def __repr__(self):
        return f"{id}"

from scripts import routes

