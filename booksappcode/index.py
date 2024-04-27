import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.sql import text
from dataclasses import dataclass

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite_container/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

bookslist = []
userslist = []
@dataclass
class User(db.Model):
    __tablename__ = 'users'
    id:int
    Name:str
    Gender:str
    DOB:str
    Location:str
    
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Gender = db.Column(db.String(100), nullable=False)
    DOB = db.Column(db.String(15), nullable=False)
    Location = db.Column(db.String(100), nullable=False)
    
    def __init__(self, Name, Gender, DOB, Location):
        self.Name = Name
        self.Gender = Gender
        self.DOB = DOB
        self.Location = Location

@dataclass
class Book(db.Model):
    __tablename__ = 'books'
    id:int
    Title:str
    Genre:str
    Author:str
    Condition:str

    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(100), nullable=False)
    Genre = db.Column(db.String(100), nullable=False)
    Author = db.Column(db.String(100), nullable=False)
    Condition = db.Column(db.String(20), nullable=False)

    def __init__(self, Title, Genre, Author, Condition):
        self.Title = Title
        self.Genre = Genre
        self.Author = Author
        self.Condition = Condition

@app.route('/books/<int:book_id>/')
def book(book_id):
    book = Book.query.get_or_404(book_id)
    return '<h1>{0}</h1>'.format(book.Title)

@app.route('/books/')
def books():
    books = Book.query.all()
    return jsonify(books)

@app.route('/users/')
def users():
    users = User.query.all()
    return jsonify(users)

#@app.route('/books', methods=['POST'])
#def add_books():
#    books.append(request.get_json())
#    return '', 204

@app.route('/books', methods=['POST'])
def add_book():
    bookslist.append(request.get_json())
    Title = bookslist[0]['Title']
    Genre = bookslist[0]['Genre']
    Author = bookslist[0]['Author']
    Condition = bookslist[0]['Condition']
    record = Book(Title, Genre, Author, Condition)
    # Flask-SQLAlchemy magic adds record to database
    db.session.add(record)
    db.session.commit()
    return '', 204

@app.route('/')
def testdb():
    try:
        db.session.query(text('1')).from_statement(text('SELECT 1')).all()
        db.create_all()
        return '<h1>Connects Successfully</h1>'
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

@app.route('/users/<int:user_id>/')
def user(user_id):
    user = User.query.get_or_404(user_id)
    return '<h1>{0}</h1>'.format(user.Name)

#@app.route('/users', methods=['POST'])
#def add_users():
#    users.append(request.get_json())
#    return '', 204

@app.route('/users', methods=['POST'])
def add_user():
    userslist.append(request.get_json())
    Name = userslist[0]['Name']
    Gender = userslist[0]['Gender']
    DOB = userslist[0]['DOB']
    Location = userslist[0]['Location']
    record = User(Name, Gender, DOB, Location)
    # Flask-SQLAlchemy magic adds record to database
    db.session.add(record)
    db.session.commit()
    return '', 204

