from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app  = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABSE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class BookModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f"Book(title = {self.title}, description = {self.description})"

#db.create_all()

book_put_args = reqparse.RequestParser()
book_put_args.add_argument('title', required=True)
book_put_args.add_argument('description', required=True)

resource_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "description": fields.String
}

class Book(Resource):
    @marshal_with(resource_fields)
    def get(self, book_id):
        result = BookModel.query.filter_by(id=book_id).first()
        if not result:
            abort(404, message=f"Could not find book with id {book_id}")
        return result, 200
    
    @marshal_with(resource_fields)
    def put(self, book_id):
        args = book_put_args.parse_args()
        book = BookModel(id=book_id, title=args["title"], description=args["description"])
        db.session.add(book)
        db.session.commit()
        return book, 201

    def delete(self, book_id):
        result = BookModel.query.filter_by(id=book_id).first()
        if not result:
            abort(404, message=f"Could not find book with id {book_id}")
        db.session.delete(result)
        db.session.commit()
        return "", 204


api.add_resource(Book, "/books/<book_id>")

if __name__ == "__main__":
    app.run(debug=True)