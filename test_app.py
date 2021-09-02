import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor

import datetime

class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        self.assistant = os.environ['casting_assistant']
        self.director = os.environ['casting_director']
        self.producer = os.environ['executive_producer']
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', 'host123', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

            self.new_movie = {
            'title': 'Bell Bottom2',
            'release_date': datetime.date(2021, 2, 9),
        }

        self.update_movie = {
            'title': 'Bell Bottom3',
            'release_date': datetime.date(2030, 6, 8),
        }

        self.new_actor = {
            'name': 'Katrina kaif',
            'age': 35,
            'gender': 'female',
        }

        self.update_actor = {
            'name': 'Katrina kaif',
            'age': 40,
            'gender': 'female',
        }




    def tearDown(self):
        """Executed after reach test"""
        pass


# Get movies

    def test_get_movies(self):
        res = self.client().get('/movies', headers={"Authorization": "Bearer {}".format(self.assistant)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        

    def test_401_get_movies_unauthorized(self):
        res = self.client().get('/movies', headers={"Authorization": "Bearer {}".format(self.assistant)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        

#Post moive

    def test_create_movie(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers={"Authorization": "Bearer {}".format(self.director)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movie']))

    def test_401_create_movie_unauthorized(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers={"Authorization": "Bearer {}".format(self.director)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

   
#patch movie

    def test_update_movie(self):
        res = self.client().patch('/movies/1', json=self.update_movie, headers={"Authorization": "Bearer {}".format(self.producer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movie']))

    def test_400_update_movie_with_no_body(self):
        res = self.client().patch('/movies/1000', json='',headers={"Authorization": "Bearer {}".format(self.producer)})
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    

# delete movie

    def test_delete_movie(self):
        res=self.client().delete('/movies/1',headers={"Authorization": "Bearer {}".format(self.producer)})
        data=json.loads(res.data)
        quest=Movie.query.filter(Movie.id == 20).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    def test_404_delete_movie(self):
        res=self.client().delete('/movies/1000', headers={"Authorization": "Bearer {}".format(self.producer)})
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_401_delete_movie_unauthorized(self):
        res=self.client().delete('/movies/1', headers='')
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)


# Get Actors


    def test_get_actors(self):
        res = self.client().get(
            '/movies', headers={"Authorization": "Bearer {}".format(self.assistant)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_get_actors_unauthorized(self):
        res = self.client().get(
            '/movies', headers={"Authorization": "Bearer {}".format(self.assistant)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

#Post actors

    def test_create_actors(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers={"Authorization": "Bearer {}".format(self.director)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_401_create_actors_unauthorized(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers={"Authorization": "Bearer {}".format(self.director)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)


#patch movie


    def test_update_actors(self):
        res = self.client().patch('/actors/1', json=self.update_actor,
                                  headers={"Authorization": "Bearer {}".format(self.producer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_400_update_actors_with_no_body(self):
        res = self.client().patch('/actors/1000', json='',
                                  headers={"Authorization": "Bearer {}".format(self.producer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)


# delete movie


    def test_delete_actors(self):
        res = self.client().delete(
            '/actors/1', headers={"Authorization": "Bearer {}".format(self.producer)})
        data = json.loads(res.data)
        quest = Movie.query.filter(Actor.id == 20).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    def test_404_delete_actors(self):
        res = self.client().delete(
            '/movies/1000', headers={"Authorization": "Bearer {}".format(self.producer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)



if __name__ == "__main__":
    unittest.main()


