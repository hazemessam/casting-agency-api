# Third party imports
from flask import request, jsonify, abort

# Application imports
from app import app
from models import Actor, Movie
from auth import AuthError, requires_auth


#---------------------------------
# Actor routes and views
#---------------------------------

# Get all actors
@app.route('/actors')
@requires_auth('get:actors')
def get_all_actors():
    actors = Actor.query.all()
    if actors and len(actors) == 0:
        abort(404)

    return jsonify({
        'actors': [actor.format() for actor in actors]
    })


# Create actor
@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def create_actor():
    req_body = request.get_json()
    name = req_body.get('name')
    age = req_body.get('age')
    gender = req_body.get('gender')

    if not name:
        abort(400)

    actor = Actor(
        name=name,
        age=age,
        gender=gender
    )
    actor.insert()

    return jsonify(actor.format()), 201


# Get actor by its id
@app.route('/actors/<int:id>')
@requires_auth('get:actors')
def get_actor(id):
    actor = Actor.query.get(id)
    if not actor:
       abort(404)

    return jsonify(actor.format())


# Update actor by its id
@app.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(id):
    actor = Actor.query.get(id)
    if not actor:
        abort(404)

    name = request.json.get('name')
    if name:
        actor.name = name
    
    age = request.json.get('age')
    if age:
        actor.age = age
    
    gender = request.json.get('gender')
    if gender:
        actor.gender = gender

    actor.update()

    return jsonify(actor.format())


# Delete actor by its id
@app.route('/actors/<int:id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(id):
    actor = Actor.query.get(id)
    if not actor:
        abort(404)

    actor.delete()

    return jsonify({
        'deleted': actor.id
    })


#---------------------------------
# Movie routes and views
#---------------------------------

# Get all movies
@app.route('/movies')
@requires_auth('get:movies')
def get_all_movies():
    movies = Movie.query.all()
    if movies and len(movies) == 0:
        abort(404)

    return jsonify({
        'movies': [movie.format() for movie in movies]
    })


# Create movie
@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def create_movie():
    title = request.json.get('title')
    release_date = request.json.get('release_date')

    if not title:
        abort(400)

    movie = Movie.query.filter(Movie.title == title.title()).first()
    if movie:
        abort(422)

    movie = Movie(
        title=title,
        release_date=release_date
    )
    movie.insert()

    return jsonify(movie.format()), 201


# Get movie by its id
@app.route('/movies/<int:id>')
@requires_auth('get:movies')
def get_movie(id):
    movie = Movie.query.get(id)
    if not movie:
       abort(404)

    return jsonify(movie.format())


# Update movie by its id
@app.route('/movies/<int:id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(id):
    movie = Movie.query.get(id)
    if not movie:
        abort(404)

    title = request.json.get('title')
    if title:
        movie.title = title.title()
    
    release_date = request.json.get('release_date')
    if release_date:
        movie.release_date = release_date

    movie.update()

    return jsonify(movie.format())


# Delete movie by its id
@app.route('/movies/<int:id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(id):
    movie = Movie.query.get(id)
    if not movie:
        abort(404)

    movie.delete()

    return jsonify({
        'deleted': movie.id
    })


#---------------------------------
# Error handler
#---------------------------------

@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error['description']
    }), error.status_code


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400


@app.errorhandler(404)
def not_found(err):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'not found'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': 'false',
        'error': 405,
        'message': 'method not allowed'
    }), 405


@app.errorhandler(422)
def unproccessable(error):
    return jsonify({
        'success': 'false',
        'error': 422,
        'message': 'unproccessable'
    }), 422


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'success': 'false',
        'error': 500,
        'message': 'internal server error'
    }), 500