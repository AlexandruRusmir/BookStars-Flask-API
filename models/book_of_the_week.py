from main import db 

class BookOfTheWeek(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.integer, db.ForeignKey('book.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)