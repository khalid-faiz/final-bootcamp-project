# Import necessary modules and components from Flask, Flask-Login,
# And the application module
import json

from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from src import db
from src.models import User, Book, Category, Comment, Rating

# Create a Blueprint called "index" to organize routes and views related to
# The home page and the single book page
index_bp = Blueprint("index", __name__)

# Class for creating a tree structure for all the comments
#  Pulled of the database
class CommentBranch():
    def __init__(self, parent_comment):
        # It has the same properties as the comment
        self.content = parent_comment.content
        self.is_deleted = parent_comment.is_deleted
        self.is_editted = parent_comment.is_editted
        self.user = parent_comment.user
        self.id = parent_comment.id
        self.timestamp = parent_comment.timestamp
        # Plus a list of comment branches to retieve all of its child comments in a list of CommentBraches
        self.comments = [CommentBranch(comment) for comment in Comment.query.filter_by(parent_comment_id=self.id).all()]


# A helper method to get all the CommentBranches in a list
def get_comment_branches(top_level_comments):
    return [CommentBranch(comment) for comment in top_level_comments]

@index_bp.route("/")
def home():
    # Query all the books in the database and pass it to the template as a json string in a list form
    # Also pass the book count to the databse, so we can render that many elements in the DOM
    books = list(map(lambda book:book.google_id,Book.query.all()))
    return render_template("index/home.html", books = json.dumps(books), book_count=len(books))

# Route for a single book
@index_bp.route("/book/<google_id>")
def book(google_id):
    # Query the database with the book google ID
    book = Book.query.get(google_id)
    # If found get top level comments
    if book:
        # get top-level comments
        top_level_comments = Comment.query\
                    .filter(Comment.book_id == book.google_id)\
                    .filter(Comment.parent_comment_id == None).all()
    # Else, set the comments as an empty array
    else:
        top_level_comments = []
    # Render the book view to the user with the google ID, and all of its comments
    return render_template(
            "index/book.html",
            google_id=google_id,
            comments=get_comment_branches(top_level_comments)
        )
# Route for adding a comment
@index_bp.route("/book/<google_id>/comment", methods=["POST"])
@login_required
def comment(google_id):
    # Create a new Comment Object 
    comment_content = request.form["comment_content"]
    comment = Comment(comment_content)
        
    user = current_user
    book = Book.query.get(google_id)

    # Create a book object if not found
    if not book:
        book = Book(google_id)

    # Initiate the parent comment id with None
    parent_comment_id = None
    # Try and except to catch the error
    # When users are adding a top level comment
    try:
       # Get the parent comment if found
        if request.form["parent_comment_id"]:
            parent_comment_id = int(request.form["parent_comment_id"])
            if parent_comment_id:
                parent_comment = Comment.query.get(parent_comment_id)
    except:
        pass
    
    # Add the comment to the user and the book
    user.comments.append(comment)
    book.comments.append(comment)

    # Add a parent comment if there is
    if parent_comment_id:
        comment.parent_comment_id = parent_comment_id

    # Commit the session and redirect to the book page
    db.session.commit()
    return redirect(url_for("index.book", google_id=google_id))
