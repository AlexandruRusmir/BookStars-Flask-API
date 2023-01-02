from flask import Flask, jsonify, make_response, request
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import uuid
import jwt
import datetime
import os
# from models.blog_message import BlogMessage
# from models.book import Book
# from models.book_of_the_week import BookOfTheWeek
# from models.review import Review
# from models.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'introduce_one'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'booksA.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
 
db = SQLAlchemy(app)

class BlogMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_of_the_week_id = db.Column(db.Integer, db.ForeignKey('book_of_the_week.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(2000), nullable=False)

class BookOfTheWeek(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(500), nullable = False)
    rating = db.Column(db.Float, nullable = False)
    image_url = db.Column(db.String(2500), nullable = False)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_public = db.Column(db.Boolean, nullable=False)
    text = db.Column(db.String(2000), nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    score = db.Column(db.Float, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer, nullable = False)
    user_name = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(50), nullable = False)

with app.app_context():
   db.create_all()
   db.session.commit()

# new_book = Book(name='The Power of Now',
#                 author='Eckhart Tolle',
#                 description='In the first chapter, Tolle introduces readers to enlightenment and its natural enemy, the mind. He awakens readers to their role as a creator of pain and shows them how to have a pain-free identity by living fully in the present. The journey is thrilling, and along the way, the author shows how to connect to the indestructible essence of our Being, "the eternal, ever-present One Life beyond the myriad forms of life that are subject to birth and death."',
#                 image_url='https://www.google.com/imgres?imgurl=https%3A%2F%2Fm.media-amazon.com%2Fimages%2FI%2F417VRErnKPL._AC_SY780_.jpg&imgrefurl=https%3A%2F%2Fwww.amazon.com%2FPower-Now-Guide-Spiritual-Enlightenment%2Fdp%2F1577314808&tbnid=y_gFp5Vsi7zRjM&vet=12ahUKEwinj4Dl9vH7AhXdIMUKHbHFB3gQMygAegUIARCrAg..i&docid=SSc8RwKtOhlM1M&w=315&h=500&q=the%20power%20of%20now&ved=2ahUKEwinj4Dl9vH7AhXdIMUKHbHFB3gQMygAegUIARCrAg',
#                 rating=0)                 
# db.session.add(new_book)  
# new_book = Book(name='How to win friends and influence people',
#                 author='Dale Carnegie',
#                 description='Dale Carnegie’s rock-solid, time-tested advice has carried countless people up the ladder of success in their business and personal lives. One of the most groundbreaking and timeless bestsellers of all time, How to Win Friends & Influence People will teach you:six ways to make people like you, twelve ways to win people to your way of thinking, nine ways to change people without arousing resentment.',
#                 image_url='https://m.media-amazon.com/images/I/41OksZQYt+L._SX320_BO1,204,203,200_.jpg',
#                 rating=0)                 
# db.session.add(new_book) 
# new_book = Book(name='The 5 love languages',
#                 author='Gary Chapman',
#                 description='Falling in love is easy. Staying in love—that\'s the challenge. How can you keep your relationship fresh and growing amid the demands, conflicts, and just plain boredom of everyday life?In this book, you\'ll discover the secret that has transformed millions of relationships worldwide. Whether your relationship is flourishing or failing, Dr. Gary Chapman\'s proven approach to showing and receiving love will help you experience deeper and richer levels of intimacy with your partner—starting today.',
#                 image_url='https://m.media-amazon.com/images/I/51c0ewv4OML._SX417_BO1,204,203,200_.jpg',
#                 rating=0)                 
# db.session.add(new_book) 
# new_book = Book(name='1984',
#                 author='George Orwell',
#                 description='A startling and haunting novel, 1984 creates an imaginary world that is completely convincing from start to finish. No one can deny the novel’s hold on the imaginations of whole generations, or the power of its admonitions—a power that seems to grow, not lessen, with the passage of time.',
#                 image_url='https://m.media-amazon.com/images/I/41aM4xOZxaL._SX277_BO1,204,203,200_.jpg',
#                 rating=0)                 
# db.session.add(new_book) 
# new_book = Book(name='Kafka on the shore',
#                 author='Haruki Murakami',
#                 description='A startling and haunting novel, 1984 creates an imaginary world that is completely convincing from start to finish. No one can deny the novel’s hold on the imaginations of whole generations, or the power of its admonitions—a power that seems to grow, not lessen, with the passage of time.',
#                 image_url='https://m.media-amazon.com/images/I/41aM4xOZxaL._SX277_BO1,204,203,200_.jpg',
#                 rating=0)                 
# db.session.add(new_book)
# db.session.commit() 

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       if 'x-access-tokens' in request.headers:
           token = request.headers['x-access-tokens']
       if not token:
           return jsonify({'message': 'a valid token is missing'})
       try:
           data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
           current_user = User.query.filter_by(public_id=data['public_id']).first()
       except:
           return jsonify({'message': 'token is invalid'})
       return f(current_user, *args, **kwargs)
   return decorator

@app.route('/register', methods=['POST'])
def signup_user(): 
   data = request.get_json() 
   hashed_password = generate_password_hash(data['password'], method='sha256')
   new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
   db.session.add(new_user) 
   db.session.commit()   
   return jsonify({'message': 'registered successfully'})

@app.route('/login', methods=['POST']) 
def login_user():
   auth = request.authorization  
   if not auth or not auth.username or not auth.password: 
       return make_response('could not verify', 401, {'Authentication': 'login required"'})   
   user = User.query.filter_by(name=auth.username).first()  
   if check_password_hash(user.password, auth.password):
       token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=50)}, app.config['SECRET_KEY'], "HS256")
       return jsonify({'token' : token})
   return make_response('could not verify',  401, {'Authentication': '"login required"'})

@app.route('/book', methods=['POST'])
@token_required
def create_book(current_user):
   data = request.get_json()
   new_book = Book(name=data['name'], author=data['author'], description=data['description'], image_url=data['imageUrl'], rating=0) 
   db.session.add(new_book)  
   db.session.commit() 
   return jsonify({'message' : 'new books created'})

@app.route('/books', methods=['GET'])
def get_books():
   books = Book.query.all()
   output = []
   for book in books:
       book_data = {}
       book_data['id'] = book.id
       book_data['name'] = book.name
       book_data['author'] = book.author
       book_data['imageUrl'] = book.image_url
       book_data['description'] = book.description
       output.append(book_data)
 
   return jsonify({'list_of_books' : output})

if  __name__ == '__main__': 
    app.run(debug=True)