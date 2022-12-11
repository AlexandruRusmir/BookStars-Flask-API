from main import db

class BlogMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_of_the_week_id = db.Column(db.Integer, db.ForeingKey('bookOfTheWeek.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(2000), nullable=False)