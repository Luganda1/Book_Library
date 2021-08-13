# from sqlite3 import OperationalError
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import sqlite3

from jinja2 import meta
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from werkzeug.exceptions import BadRequestKeyError

'''
SQL = Struture Query Language
ORM = Object Relational Mapping 
'''
app = Flask(__name__)
# all_books = []
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# db = sqlite3.connect("books-collection.db")
# cursor = db.cursor()
# try:
#     cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
# except OperationalError:
#     None
# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
# db.commit()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}'

db.create_all()

# reading
# all_books = session.query(Book).all()



# new_book = Book(id=1, title="Harry Potter", author="J. K. Rowling", rating=9.3)
# new_book = Book(title="On Purpose", author="Mcauthor Catherine", rating=9.9)
# db.session.add(new_book)
# db.session.commit()
#
# # Update A Record By PRIMARY KEY
# book_id = 1
# book_to_update = Book.query.get(book_id)
# book_to_update.title = "Harry Potter and the Goblet of Fire"
# db.session.commit()
#
# # Delete A Particular Record By PRIMARY KEY
# book_id = 1
# book_to_delete = Book.query.get(book_id)
# db.session.delete(book_to_delete)
# db.session.commit()



@app.route('/')
def home():
    all_books = Book.query.all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form['title'],
        author = request.form['author'],
        rating = request.form['rate']
        print(f"title: {title} author: {author} rating: {rating}")
        try:
            new_book = Book(
                title=request.form['title'],
                author=request.form['author'],
                rating=request.form['rate']
            )
            db.session.add(new_book)
            db.session.commit()
        except IntegrityError:
            print(IntegrityError)

        return redirect(url_for('home'))
    return render_template('add.html')


@app.route("/edit", methods=["GET", "POST"])
def edit():
    book_id = request.args.get('id')
    book_selected = Book.query.get(book_id)
    print("title "+book_selected.title)
    if request.method == "POST":

        #UPDATE RECORD
        try:
            book_id = request.form["id"]
            book_to_update = Book.query.get(book_id)
            book_to_update.rating = request.form["rating"]
            db.session.commit()
        except BadRequestKeyError:
            print(BadRequestKeyError)
            pass
        return redirect(url_for('home'))

    return render_template('edit.html', book=book_selected)



@app.route("/delete")
def delete():
    book_id = request.args.get('id')
    print(book_id)
    # DELETE A RECORD BY ID
    try:
        book_to_delete = Book.query.get(book_id)
        print(book_to_delete)
        db.session.delete(book_to_delete)
        db.session.commit()
    except UnmappedInstanceError:
        print(UnmappedInstanceError)
        pass
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

