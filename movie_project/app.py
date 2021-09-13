from flask import Flask
from flask_restful import Resource, Api, fields, reqparse, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

# Config app for MYSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:admin@localhost/movie_list'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    rating = db.Column(db.Integer)


# db.create_all()

# Configure Parser
movie_post_args = reqparse.RequestParser()
movie_post_args.add_argument('name', type=str, help="name is required.", required=True)
movie_post_args.add_argument('rating', type=int, help="rating is required.", required=True)

movies_put_args = reqparse.RequestParser()
movies_put_args.add_argument('name', type=str)
movies_put_args.add_argument('rating', type=int)

# Fields Resource
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'rating': fields.String
}


class Movie(Resource):
    @marshal_with(resource_fields)
    def get(self, movie_id):
        movie = Movies.query.filter_by(id=movie_id).first()
        if not movie:
            abort(404, message="movie not found")
        return movie

    @marshal_with(resource_fields)
    def post(self, movie_id):
        movie = Movies.query.filter_by(id=movie_id).first()
        if movie :
            abort(409, message="movie_id already exits...")
        # args
        args = movie_post_args.parse_args()
        movie = Movies(name=args['name'], rating=args['rating'])
        db.session.add(movie)
        db.session.commit()
        return movie, 201


api.add_resource(Movie, '/movie/<int:movie_id>')

if __name__ == "__main__":
    app.run(debug=True)
