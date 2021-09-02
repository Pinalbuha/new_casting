import os, sys

from flask_migrate import Migrate, migrate; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import *
from models import setup_db, Actor, Movie
import sys
import json
from flask_migrate import Migrate



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
 
  # CORS Headers 


  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  @app.route('/')
  def welcome():
    message = 'Welcome to the Casting Agency'
    return jsonify(message)

  # Get movies
  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies(payload):
    all_movies = Movie.query.all()
    movies = [movie.format() for movie in all_movies]
    if movies is None:
      abort(404)
   
    return jsonify({
          'success': True,
          'all_movies': movies
      }),200
    

  # Post movies
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def add_movie(payload):
    body = request.get_json()
    new_title = body.get('title')
    new_release_date = body.get('release_date')

    if new_title is None or new_release_date is None:
      abort(422)
  
    try:
      new_movie = Movie(title=new_title, release_date=new_release_date)
      new_movie.insert()
    
      return jsonify({
        'success': True,
        "new_movies": new_movie.format()
      }), 200
    except Exception as e:
        print(e)
        abort(422)
        
    

  # Patch movies
  @app.route('/movies/<int:id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movies(payload, id):
    movie = Movie.query.get(id)
    if not movie:
      abort(404)
    body = request.get_json()
    title = body.get("title")
    release_date = body.get("release_date")

    if (title is None) or (release_date is None):
        abort(422)

    try:
      if title is not None:
        movie.title = title

        if release_date is not None:
          movie.relaese_date = release_date

        movie.update()
        return jsonify({
            'success': True,
            'movie': movie.format(),
        }), 200

    except Exception:
            abort(422)
    

  # Delete moives
  @app.route('/movies/<int:id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movies(payload, id):
    try:
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if movie:
            movie.delete()
            return jsonify({
                'success': True,
                'delete': id
            }), 200
        else:
            abort(404)
    except Exception:
        abort(500)

  # Get actors

  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors(payload):
      all_actors = Actor.query.all()
      actors = [actor.format() for actor in all_actors]
      if actors is None:
        abort(404)

      return jsonify({
          'success': True,
          'actors': actors
      }), 200

  # Post actors

  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def post_actors(payload):
    
      body = request.get_json()

      new_name = body.get('name', None)
      new_age = body.get('age', None)
      new_gender = body.get('gender', None)

      if (new_name is None) or (new_age is None) or (new_gender is None):
        abort(422)
      try:
        actor = Actor(name=new_name, age=new_age, gender=new_gender)
      
        #if (movie.title == newmovie.title) or (movie.release_date == newmovie.release_date):
        
        actor.insert()
      except AuthError:
        abort(422)
      return jsonify({
            'success': True,
            "actor": [actor.format()]
        }),200
    

  # Patch actors

  @app.route('/actors/<int:id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actors(payload, id):
    try:
      actor = Actor.query.filter(Actor.id == id).one_or_none()
      if actor is None:
        abort(404)
      body = request.get_json()
      updated_name = body.get('name', None)
      updated_age = body.get('age', None)
      updated_gender = body.get('gender', None)
      if updated_name is not None:
        actor.name = updated_name
      if updated_age is not None:
        actor.age = updated_age
      if updated_gender is not None:
        actor.gender =updated_gender

      actor.update()
      return jsonify({
          "success": True,
          "actors":  actor.format()
      }), 200
    except AuthError:
      abort(422)

  # Delete actor

  @app.route('/actors/<int:id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actors(payload, id):
    try:
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if actor:
            actor.delete()
            return jsonify({
                'success': True,
                'delete': id
            }), 200
        else:
            abort(404)
    except Exception:
        abort(500)


   # Error handlers

   # Error handler for Bad request error (400)


  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad request error'
    }), 400

    # Error handler for resource not found (404)
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          'success': False,
          'error': 404,
          'message': 'Resource not found'
      }), 404

    # Error handler for unprocesable entity (422)
  @app.errorhandler(422)
  def unprocesable_entity(error):
      return jsonify({
          'success': False,
          'error': 422,
          'message': 'Unprocessable entity'
      }), 422

     # Error handler for internal server error (500)
  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
          'success': False,
          'error': 500,
          'message': 'An error has occured, please try again'
      }), 500

  @app.errorhandler(AuthError)
  def handle_auth_error(ex):
      response = jsonify(ex.error)
      response.status_code = ex.status_code
      return response


  return app

app = create_app()

#if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=8080, debug=True)
