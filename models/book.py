from main import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(300), nullable = False)
    rating = db.Column(db.Float, nullable = False)
    image_url = db.Column(db.String(2500), nullable = False)

