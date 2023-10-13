from src import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Define many-to-many intermediate tables
user_book = db.Table(
                        'user_book',
                        db.Column(
                            'user_id', 
                            db.Integer, 
                            db.ForeignKey('user.id')
                            ),
                        db.Column(
                            'book_id',
                            db.Integer,
                            db.ForeignKey('book.id')
                            )
                     )
user_category = db.Table(
                        'user_category',
                        db.Column(
                            'user_id',
                            db.Integer,
                            db.ForeignKey('user.id')
                            ),
                        db.Column(
                            'category_id',
                            db.Integer,
                            db.ForeignKey('category.id')
                            )
                     )
book_category = db.Table(
                        'book_category',
                        db.Column(
                            'book_id',
                            db.Integer,
                            db.ForeignKey('book.id')
                            ),
                        db.Column(
                            'category_id',
                            db.Integer,
                            db.ForeignKey('category.id')
                            )
                     )


# User model.
# Inhirting UserMixin for authentication
class User(UserMixin, db.Model):
    # Columns
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships
    # One-to-many
    comments = db.relationship('Comment', backref="user")
    ratings = db.relationship('Rating', backref="user")

    # Many-to-many
    books = db.relationship(
        'Book',
        secondary=user_book,
        backref="user"
        )
    categories = db.relationship(
        'Category', 
        secondary=user_category,
        backref="user"
        )

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<User {self.name} | Email: {self.email}>'


# Book model
class Book(db.Model):
    # Columns
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String, unique=True, nullable=False)
    is_public = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships
    # One-to-many
    comments = db.relationship('Comment', backref="book")
    ratings = db.relationship('Rating', backref="book")

    # Many-to-many
    users = db.relationship(
        'User',
        secondary=user_book,
        backref="book"
        )
    categories = db.relationship(
        'Category',
        secondary=book_category,
        backref="book"
        )

    def __init__(self, google_id, is_public=False):
        self.google_id = google_id
        self.is_public = is_public

    def __repr__(self):
        return f'<Book {self.google_id}>'
    
    # Define a function that returns a dictionary representation
    def to_dict(self):
        return {"id": self.id, "google_id": self.google_id}

# Category model  
class Category(db.Model):
    # Columns
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    # Relationship
    # Many-to-many
    users = db.relationship(
        'User',
        secondary=user_category,
        backref="category"
        )
    Books = db.relationship(
        'Book',
        secondary=book_category,
        backref="category"
        )

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Category {self.name}>'


# Comment model
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=True)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    is_editted = db.Column(db.Boolean, nullable=False, default=False)
    timestamp = db.Column(db.DateTime, server_default=func.now())

    # Forign keys
    # Many-to-one
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))

    def __init__(self, content, is_deleted, is_editted):
        self.content = content
        self.is_deleted = is_deleted
        self.is_editted = is_editted

    def __repr__(self):
        return f'<Comment {self.content}>'


# Rating model
class Rating(db.Model):
    # Columns
    __tablename__ = "rating"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=True)

    # Forign keys
    # Many-to-one
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))