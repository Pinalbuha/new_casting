import os
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import json
from sqlalchemy import DateTime, ForeignKey, Table
import datetime

database_path = os.environ['DATABASE_URL']
#database_path = "postgres://{}:{}@{}/{}".format('postgres','host123','localhost:5432', 'casting')

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    '''Binds a Flask Application and a SQLAlchemy '''
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_create_all():
    '''drop existing database and create new fresh database'''
    db.drop_all()
    db.create_all()
    create_dumyrecords()
    
# Movies table

class Movie(db.Model):
    __tablename__ = 'Movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.Date(), nullable=False)

    def __repr__(self):
        return f"<Movie {self.id} {self.title} {self.release_date}>"

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
        }

# Actors table
class Actor(db.Model):
    __tablename__ = 'Actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Actor {self.id} {self.name} {self.age} {self.gender}>"

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }

def create_dumyrecords():
    #  movies
    movie_1 = Movie(title='Bell bottom', release_date=datetime.datetime(2021, 9, 1))
    movie_2 = Movie(title='Superman', release_date=datetime.datetime(2025, 1, 5))
    movie_3 = Movie(title='Batman', release_date=datetime.datetime(2035, 5, 11))
    movie_4 = Movie(title='Spiderman', release_date=datetime.datetime(2022, 4, 20))
    movie_5 = Movie(title='Ironman', release_date=datetime.datetime(2020, 4, 20))

    movie_1.insert()
    movie_2.insert()
    movie_3.insert()
    movie_4.insert()
    movie_5.insert()

    # actors
    actor_1 = Actor(name='Raj', gender='Male', age=25)
    actor_2 = Actor(name='Hitu', gender='Female', age=30)
    actor_3 = Actor(name='Katrina kaif', gender='Female', age=40)
    actor_4 = Actor(name='Parth', gender='Male', age=45)
    actor_5 = Actor(name='Rose', gender='Female', age=15)

    actor_1.insert()
    actor_2.insert()
    actor_3.insert()
    actor_4.insert()
    actor_5.insert()

    db.session.commit()
