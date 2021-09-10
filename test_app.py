import json
import os
import unittest
from app import app, create_app
from models import Movie, Actor, db_drop_create_all
import datetime
import os

database_path = os.environ['TEST_DATABASE_URL']
#database_path='postgres://postgres:host123@localhost:5432/casting_test'
assistant = os.environ['casting_assistant']
director = os.environ['casting_director']
producer = os.environ['executive_producer']


class CastingTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = database_path
        self.app = app.test_client()
        db_drop_create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    # Get movies

    def test_get_movies(self):
        res = self.app.get('/movies', headers={'Authorization': f"Bearer {assistant}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


    def test_401_get_movies_unauthorized(self):
        res = self.app.get('/movies')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

   # post movies

    def test_create_movie(self):
        nmovie = {"title": "Bell bottom 2", "release_date": datetime.datetime(2021, 2, 9),"actor_id": 2}
        resp = self.app.post('/movies', json=nmovie,headers={'Authorization': f"Bearer {producer}"})
        data = json.loads(resp.data)
        
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(data['success'])


    def test_create_movie_unauthorized(self):
        movie1 = {"title": "Bell bottom 2", "release_date":  datetime.datetime(2021, 2, 9),"actor_id": 2}
        resp = self.app.post('/movies', json=movie1,headers={'Authorization': f"Bearer {assistant}"})
        data = json.loads(resp.data)
        
        self.assertEqual(resp.status_code, 401)
        self.assertFalse(data['success'])

    # Patch movie

    def test_update_movie(self):
        update_movie = {"title": "Bell Bottom",'release_date': datetime.datetime(2030, 6, 8),"actor_id": 1}
        
        resp = self.app.patch('/movies/4', headers={'Authorization': f"Bearer {producer}"}, json=update_movie)
        data = json.loads(resp.data)
        
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(data['success'])

    def test_patch_movie_unauthorized(self):
        resp = self.app.patch('/movies/3', headers={'Authorization': f"Bearer {producer}"}, json={"title": "Spiderman"})
        data = json.loads(resp.data)
        
        self.assertEqual(resp.status_code, 422)
        self.assertFalse(data['success'])
        self.assertTrue(data['error'],422)

    def test_401_patch_movie_unauthorized(self):
        resp = self.app.patch('/movies/3', headers={'Authorization': f"Bearer {assistant}"}, json={"title": "Spiderman"})
        data = json.loads(resp.data)
       
        self.assertEqual(resp.status_code, 401)
        self.assertFalse(data['success'])
       

     # delete movies
    def test_delete_movies(self):
        resp = self.app.delete('/movies/2', headers={'Authorization': f"Bearer {producer}"})
        data = json.loads(resp.data)
        
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(data['success'])

   
    def test_delete_unauthorized(self):
        resp = self.app.delete(
            '/movies/3', headers={'Authorization': f"Bearer {assistant}"})
        data = json.loads(resp.data)
        
        self.assertEqual(resp.status_code, 401)
        self.assertFalse(data['success'])


 # Get actors

    def test_get_actors(self):
        resp = self.app.get('/actors', headers={'Authorization': f"Bearer {director}"})
        data = json.loads(resp.data)
        
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(data['success'])

    
    def test_401_get_actors_unauthorized(self):
        resp = self.app.get('/actors')
        data = json.loads(resp.data)
        
        self.assertEqual(resp.status_code, 401)
        self.assertFalse(data['success'])

    # Post actors

    def test_create_actors(self):
        actor_data = {"name": "Arjun", "age": 45, "gender": "male"}
        resp = self.app.post('/actors', json=actor_data,headers={'Authorization': f"Bearer {director}"})
        data = json.loads(resp.data)
        
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(data['success'])


    def test_401_create_actor_unauthorized(self):
        actor_data = {"name": "Arjun", "age": 45, "gender": "male"}
        resp = self.app.post('/actors', json=actor_data,headers={'Authorization': f"Bearer {assistant}"})
        data = json.loads(resp.data)
        
        self.assertEqual(resp.status_code, 401)
        self.assertFalse(data['success'])

    #patch actors

    def test_update_actors(self):
        update_actor = {"name":"Prags", "age": 29, "gender": "male"}
        res = self.app.patch('/actors/1', json=update_actor,headers={"Authorization": f"Bearer {producer}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))


    def test_401_update_actors(self):
        update_actor = {"name":"Prags", "age": 29, "gender": "male"}
        res = self.app.patch('/actors/1000', json=update_actor,headers={"Authorization": f"Bearer {assistant}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # Delete actors

    def test_delete_actors(self):
        resp = self.app.delete('/actors/1', headers={'Authorization': f"Bearer {producer}"})
        data = json.loads(resp.data)
        
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(data['success'])

    def test_404_delete_actors(self):
        resp = self.app.delete('/actors/1', headers={'Authorization': f"Bearer {assistant}"})
        data = json.loads(resp.data)
        
        self.assertEqual(resp.status_code, 401)
        self.assertFalse(data['success'])


if __name__ == '__main__':
    unittest.main()
