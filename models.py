import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate
from datetime import datetime


#database_filename = "database.db"
#project_dir = os.path.dirname(os.path.abspath(__file__))
#database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))
#database_path = os.environ['DATABASE_URL']
database_name = "casting"
database_path = "postgresql://{}:{}@{}/{}".format('postgres', 'host123', 'localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    db.create_all()



"""
Movie
"""
class Movie(db.Model):
    __tablename__ = "Movies"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(db.Date(), nullable=False)

    def __repr__(self):
        return f"<Movie {self.title} {self.release_date}>"

    def __init__(self, id, title, release_date):
        self.id = id
        self.title = title
        self.release_date = release_date

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
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date.isoformat()
        }
    #Actor

class Actor(db.Model):
    __tablename__ = "Actors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)

    def __repr__(self):
        return f"<Actor {self.name} {self.age} {self.gender}>"

    def __init__(self, id, first_name, age, gender):
        self.id = id
        self.first_name = first_name
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
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,

        }

    




    
