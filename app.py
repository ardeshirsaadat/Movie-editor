import os
from flask import Flask, request, abort, jsonify, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors():
        try:
            actors = Actor.query.all()
            if len(actors) == 0:
                abort(422)
            formated_actors = [actor.format() for actor in actors]
            return jsonify({'success': True, 'actors': formated_actors})
        except BaseException:
            abort(404)
        except AuthError:
            abort(AuthError)

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies():
        try:
            movies = Movie.query.all()
            if len(movies) == 0:
                abort(422)
            formated_movies = [movie.format() for movie in movies]
            return jsonify({'success': True, 'movies': formated_movies})
        except BaseException:
            abort(404)
        except AuthError:
            abort(AuthError)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actor')
    def post_actor():
        try:
            data = request.get_json()
            name = data.get('name', None)
            age = data.get('age', None)
            gender = data.get('gender', None)
            actor_object = Actor(name, int(age), gender)
            actor_object.insert()
            return jsonify({'success': True})
        except BaseException:
            abort(422)
        except AuthError:
            abort(AuthError)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movie')
    def post_movie():
        try:
            data = request.get_json()
            movie = data.get('movie', None)
            release_date = data.get('release_date', None)
            movie_object = Movie(movie, int(release_date))
            movie_object.insert()
            return jsonify({'success': True})
        except BaseException:
            abort(422)
        except AuthError:
            abort(AuthError)

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(id):
        try:
            actor_by_id = Actor.query.get(id)
            actor_by_id.delete()
            return jsonify({'success': True})
        except BaseException:
            abort(422)
        except AuthError:
            abort(AuthError)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(id):
        try:
            movie_by_id = Movie.query.get(id)
            movie_by_id.delete()
            return jsonify({'success': True})
        except BaseException:
            abort(422)
        except AuthError:
            abort(AuthError)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def update_actor(id):
        try:
            actor_to_update = Actor.query.get(id)
            if actor_to_update is None:
                abort(404)
            data = request.get_json()
            name = data.get('name', None)
            age = data.get('age', None)
            gender = data.get('gender', None)
            if name is not None:
                actor_to_update.name = name
            if age is not None:
                actor_to_update.age = int(age)
            if gender is not None:
                actor_to_update.gender = gender
            actor_to_update.update()
            return jsonify({
                'success': True,
                'actor': Actor.query.get(id).format()
            })
        except BaseException:
            abort(422)
        except AuthError:
            abort(AuthError)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(id):
        try:
            movie_to_update = Movie.query.get(id)
            if movie_to_update is None:
                abort(404)
            data = request.get_json()
            movie = data.get('movie', None)
            release_date = data.get('release_date', None)
            if movie is not None:
                movie_to_update.movie = movie
            if release_date is not None:
                movie_to_update.release_date = int(release_date)

            movie_to_update.update()
            return jsonify({
                'success': True,
                'movie': Movie.query.get(id).format()
            })
        except BaseException:
            abort(422)
        except AuthError:
            abort(AuthError)

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "bad request"
        }), 404

    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        return jsonify({
            "success": False,
            "error": error.error,
            "message": error.status_code
        }), error.status_code

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)