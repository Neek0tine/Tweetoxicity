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

db.session.execute('CREATE TABLE IF NOT EXISTS clients (id INTEGER NOT NULL,"user_id"	INTEGER, username VARCHAR(100) NOT NULL,	date_added DATETIME, PRIMARY KEY (id))')
db.session.execute('CREATE TABLE IF NOT EXISTS "clients__data" ("id"	INTEGER NOT NULL,"user_id"	INTEGER,"screen_name"	STRING,"user_name"  STRING,"user_location"	STRING,"user_bio"	STRING,"user_followers"	INTEGER,"user_following"	INTEGER,"user_birth"	INTEGER,"user_pic"	STRING,PRIMARY KEY("id"),FOREIGN KEY("user_id") REFERENCES "clients"("user_id"))')
db.session.execute('CREATE TABLE IF NOT EXISTS "clients__input" (id INTEGER NOT NULL,"tweetscrap"	JSON,"tweetmodel"	JSON,"positive"	INTEGER,"negative"	INTEGER,	"user_id"	INTEGER, PRIMARY KEY("id"),FOREIGN KEY("user_id") REFERENCES "clients"("user_id"))')

db.session.close()

class Clients(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, default=random_integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    clients_data = db.relationship('Clients_Data', backref='author', lazy=True)
    clients_input = db.relationship('Clients_Input', backref='author', lazy=True)

    def __repr__(self):
        return f'{self.user_id} - {self.username} - {self.date_added}'


class Clients_Data(db.Model):
    __tablename__ = 'clients__data'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('clients.user_id'), nullable=False)
    screen_name = db.Column(db.String, nullable=True)
    user_name = db.Column(db.String, nullable=True)
    user_location = db.Column(db.String, nullable=True)
    user_bio = db.Column(db.String, nullable=True)
    user_followers = db.Column(db.Integer, nullable=True)
    user_following = db.Column(db.Integer, nullable=True)
    user_birth = db.Column(db.String, nullable=True)
    user_pic = db.Column(db.String(100), nullable=True)

class Clients_Input(db.Model):
    __tablename__ = 'clients__input'
    id = db.Column(db.Integer, primary_key=True)
    tweetscrap = db.Column(db.JSON(), nullable=True)
    tweetmodel = db.Column(db.JSON(), nullable=True)
    positive = db.Column(db.Integer, nullable=True)
    negative = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('clients.user_id'), nullable=False)

    def __repr__(self):
        return f"{self.user_id}"

from scripts import routes

