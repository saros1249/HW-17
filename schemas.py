#Схемы для зефира.
from marshmallow import Schema, fields


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Str()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()
directors_schema = DirectorSchema(many=True)
director_schema = DirectorSchema()
genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()
