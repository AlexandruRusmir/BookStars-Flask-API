from main import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_public = db.Column(db.Boolean, nullable=False)
    text = db.Column(db.String(2000), nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    score = db.Column(db.Float, nullable=False)