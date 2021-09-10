import os
import sys
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from auth import AuthError, requires_auth
import json
from models import setup_db, Movie, Actor, db_drop_create_all

def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)

  CORS(app, resources={'/': {"origins": "*"}})
  return app

app = create_app()
#db_drop_create_all() 


@app.route('/')
def welcome():
  message = 'Welcome to the Casting Agency'
  return jsonify(message)

#Get movies

@app.route("/movies", methods=["GET"])
@requires_auth("get:movies")
def get_movies_list(payload):
  all_movies = Movie.query.all()
  movies = [movie.format() for movie in all_movies]
  if movies is None:
    abort(404)
   
  return jsonify({
    'success': True,
    'status_code' :200,
    'all_movies': movies
      }),200
 
# Post movies

@app.route("/movies", methods=["POST"])
@requires_auth("post:movies")
def add_movie(payload):
  body = request.get_json()
  new_title = body.get("title")
  new_release_date = body.get("release_date")

  if new_title is None or new_release_date is None:
    abort(422)
  
  try:
    movie = Movie(title=new_title, release_date=new_release_date)
    movie.insert()
    return jsonify({
      "success": True,
      "status_code": 200,
      "Added Movie": movie.format()
    }), 200
  except Exception:
    abort(400)


#patch movies

@app.route("/movies/<int:movie_id>", methods=["PATCH"])
@requires_auth("patch:movies")
def update_movie(payload, movie_id):
  movie = Movie.query.get(movie_id)
  print("Movie to be patched", movie)
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
        movie.release_date = release_date

      movie.update()
      return jsonify({
            'success': True,
            'movie': movie.format(),
        }), 200

  except Exception:
      abort(422)

# Delete movies

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

#Get actors

@app.route("/actors", methods=["GET"])
@requires_auth("get:actors")
def get_actors_list(payload):
  all_actors = Actor.query.all()
  actors = [actor.format() for actor in all_actors]
  if actors is None:
    abort(404)

  return jsonify({
      'success': True,
      'actors': actors
      }), 200

# Post actors

@app.route("/actors", methods=["POST"])
@requires_auth("post:actors")
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
  except Exception:
    abort(422)
  return jsonify({
    'success': True,
    "actor": [actor.format()]
    }),200

#Patch actors

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
      actor.gender = updated_gender

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
    abort(404)

# Error handlers

# Error handler for Bad request
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

#Error handler for unauthorized
@app.errorhandler(401)
def not_authorized(error):
  return jsonify({
      'success': False,
      'error': 401,
      'message': 'Unauthorized'
  }), 401

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
def auth_error(error):
  return jsonify({
      "success": False,
      "error": error.status_code,
      "message": error.error['description']
  }), error.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
