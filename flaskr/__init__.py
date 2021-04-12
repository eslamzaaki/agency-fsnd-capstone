# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import click
import json
import os
import unittest
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from auth.auth import *
from models import Actor, Movie, setup_db

# ---------------------------------------------------------
# Config
# ---------------------------------------------------------


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # CORS app
    cors = CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
            response.headers.add(
                'Access-Control-Allow-Headers',
                'Content-Type,Authorization,true'
            )
            response.headers.add(
                'Access-Control-Allow-Methods',
                'GET,PATCH,POST,DELETE,OPTIONS'
            )
            return response

    # ---------------------------------------------------------
    # Routes
    # ---------------------------------------------------------
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors():
            actors = Actor.query.all()

            if not actors:
                abort(404)

            return jsonify({
                'success': True,
                'actors': [actor.format() for actor in actors]
            }), 200

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies():

            movies = Movie.query.all()
            if not movies:
                abort(404)

            return jsonify({
                'success': True,
                'movies': [movie.format() for movie in movies]
            }), 200

        #  add an actor to the database.
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor():
            data = request.get_json()

            if 'name' not in data:
                abort(400)
            if 'age' not in data:
                abort(400)
            if 'gender' not in data:
                abort(400)

            actor = Actor(
                name=data['name'],
                age=data['age'],
                gender=data['gender']
            )
            try:
                actor.insert()
            except:
                abort(422)

            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 200

        #  add a movie to the database.
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie():
            data = request.get_json()

            if 'title' not in data:
                abort(400)
            if 'release' not in data:
                abort(400)

            movie = Movie(title=data['title'], release=data['release'])
            try:
                movie.insert()
            except:
                abort(422)

            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 200

        # update an actor in the database.
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(actor_id):
            if not actor_id:
                abort(400)

            actor = Actor.query.get(actor_id)
            if not actor:
                abort(404)

            data = request.get_json()

            if 'name' in data and data['name']:
                actor.name = data['name']

            if 'age' in data and data['age']:
                actor.age = data['age']

            if 'gender' in data and data['gender']:
                actor.gender = data['gender']
            try:
                actor.update()
            except:
                abort(422)

            return jsonify({
                'success': True,
                'actor': actor.format(),
            }), 200

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(movie_id):
            if not movie_id:
                abort(400)

            movie = Movie.query.get(movie_id)
            if not movie:
                abort(404)

            data = request.get_json()

            if 'title' in data and data['title']:
                movie.title = data['title']

            if 'release' in data and data['release']:
                movie.release = data['release']
            try:
                movie.update()
            except:
                abort(422)
            return jsonify({
                'success': True,
                'movie': movie.format(),
            }), 200

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(id):
            if not id:
                abort(400)

            actor = Actor.query.get(id)
            if not actor:
                abort(404)

            actor.delete()

            return jsonify({
                'success': True,
                'actor_id': id
            }), 200

        # delete movies in the database.
    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(id):
            if not id:
                abort(400)

            movie = Movie.query.get(id)
            if not movie:
                abort(404)

            movie.delete()

            return jsonify({
                'success': True,
                'movie_id': id
            }), 200

    # ---------------------------------------------------------
    # Error Handling
    # ---------------------------------------------------------
    @app.errorhandler(401)
    def not_authorized(error):
            return jsonify({
                "success": False,
                "error": 401,
                "message": "Authentication error"
            }), 401

    @app.errorhandler(403)
    def forbidden(error):
            return jsonify({
                "success": False,
                "error": 403,
                "message": "Forbidden"
            }), 403

    @app.errorhandler(404)
    def not_found(error):
            return jsonify({
                "success": False,
                "error": 404,
                "message": "Item not found"
            }), 404

    @app.errorhandler(422)
    def unprocessable(error):
            return jsonify({
                "success": False,
                "error": 422,
                "message": "Request could not be processed"
            }), 422

    @app.errorhandler(400)
    def bad_request(error):
            return jsonify({
                "success": False,
                "error": 400,
                "message": "Bad Request"
            }), 400

    @app.errorhandler(AuthError)
    def auth_error(error):
            return jsonify({
                'success': False,
                'error': error.status_code,
                'message': error.error['description']
            }), error.status_code

    return app
