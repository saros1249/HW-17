# app.py
from alchemy import db
from flask import Flask, request, jsonify
from flask_restx import Api, Resource
from schemas import *
from models import Movie, Director, Genre

app = Flask(__name__)

app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 3}

db.init_app(app)

api = Api(app)

movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):

        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')

        if director_id:
            movies = Movie.query.filter(Movie.director_id == director_id).all()
        elif genre_id:
            movies = Movie.query.filter(Movie.genre_id == genre_id).all()
        elif director_id and genre_id:
            movies = Movie.query.filter(Movie.director_id == director_id and Movie.genre_id == genre_id).all()
        else:
            movies = Movie.query.all()
        return movies_schema.dump(movies), 200

    def post(self):

        with db.session.begin():
            new_data = request.json
            new_movie = Movie(**new_data)
            db.session.add(new_movie)
            db.session.commit()
        return 'Добавлен новый фильм', 201


@movie_ns.route('/<int:movie_id>')
class MovieView(Resource):
    def get(self, movie_id):
        try:
            movie = Movie.query.get(movie_id)
            if movie:
                return movie_schema.dumps(movie), 200
            return 'Запрошенный фильм не найден', 404
        except Exception as e:
            return e, 404

    def put(self, movie_id):
        with db.session.begin():
            movie = Movie.query.get(movie_id)
            if movie:
                update_data = request.json
                movie.title = update_data['title']
                movie.description = update_data['description']
                movie.trailer = update_data['trailer']
                movie.year = update_data['year']
                movie.rating = update_data['rating']
                movie.genre_id = update_data['genre_id']
                movie.director_id = update_data['director_id']
                db.session.add(movie)
                db.session.commit()
                return f'Фильм с ID{movie_id} обновлён.', 200
            return 'Запрошенный фильм не найден', 404

    def patch(self, movie_id):
        with db.session.begin():
            movie = Movie.query.get(movie_id)
            if movie:
                update_data = request.json
                if 'title' in update_data:
                    movie.title = update_data['title']
                elif 'description' in update_data:
                    movie.description = update_data['description']
                elif 'trailer' in update_data:
                    movie.trailer = update_data['trailer']
                elif 'year' in update_data:
                    movie.year = update_data['year']
                elif 'rating' in update_data:
                    movie.rating = update_data['rating']
                elif 'genre_id' in update_data:
                    movie.genre_id = update_data['genre_id']
                elif 'director_id' in update_data:
                    movie.director_id = update_data['director_id']
                return 'Данные успешно обновлены'
            return f'Запрошенный фильм не найден', 404

    def delete(self, movie_id):
        with db.session.begin():
            movie = Movie.query.get(movie_id)
            if movie:
                db.session.delete(movie)
                db.session.commit()
                return f'Фильм с ID{movie_id} удaлён.', 204
            return f'Запрошенный фильм не найден', 404


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors = Director.query.all()
        return directors_schema.dump(directors), 200

    def post(self):
        with db.session.begin():
            new_data = request.json
            new_director = Director(**new_data)
            db.session.add(new_director)
            db.session.commit()
        return 'Добавлен новый режиссёр.', 201


@director_ns.route('/<int:director_id>')
class DirectorView(Resource):
    def get(self, director_id):
        try:
            director = Director.query.get(director_id)
            if director:
                return director_schema.dumps(director), 200
            return f'Запрошенный режиссёр не найден', 404
        except Exception as e:
            return e, 404

    def put(self, director_id):
        with db.session.begin():
            director = Director.query.get(director_id)
            if director:
                update_data = request.json
                director.name = update_data['name']
                db.session.add(director)
                db.session.commit()
                return f'Pежиссёр с ID{director_id} обновлён.', 200
            return f'Запрошенный режиссёр не найден', 404

    def delete(self, director_id):
        with db.session.begin():
            director = Director.query.get(director_id)
            if director:
                db.session.delete(director)
                db.session.commit()
                return f'Pежиссёр с ID{director_id} удaлён.', 204
            return f'Запрошенный режиссёр не найден', 404


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres = Genre.query.all()
        return genres_schema.dump(genres), 200

    def post(self):
        with db.session.begin():
            new_data = request.json
            new_genre = Genre(**new_data)
            db.session.add(new_genre)
            db.session.commit()
        return 'Добавлен новый жанр.', 201


@genre_ns.route('/<int:genre_id>')
class GenreView(Resource):
    def get(self, genre_id):
        try:
            genre = Genre.query.get(genre_id)
            if genre:
                return genre_schema.dumps(genre), 200
            return 'Запрошенный жанр не найден', 404
        except Exception as e:
            return e, 404

    def put(self, genre_id):
        with db.session.begin():
            genre = Genre.query.get(genre_id)
            if genre:
                update_data = request.json
                genre.name = update_data['name']
                db.session.add(genre)
                db.session.commit()
                return f'Жанр с ID{genre_id} обновлён.', 200
        return 'Запрошенный жанр не найден', 404

    def delete(self, genre_id):
        with db.session.begin():
            genre = Genre.query.get(genre_id)
            if genre:
                db.session.delete(genre)
                db.session.commit()
                return f'Жанр с ID{genre_id} удaлён.', 204
            return f'Запрошенный жанр не найден', 404


if __name__ == '__main__':
    app.run(debug=True)
