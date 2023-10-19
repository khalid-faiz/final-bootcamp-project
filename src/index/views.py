import json
from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from src import db
from src.models import User, Book, Category, Comment, Rating

index_bp = Blueprint("index", __name__)


class CommentBranch():
    def __init__(self, parent_comment):
        self.content = parent_comment.content
        self.is_deleted = parent_comment.is_deleted
        self.is_editted = parent_comment.is_editted
        self.user = parent_comment.user
        self.id = parent_comment.id
        self.timestamp = parent_comment.timestamp
        self.comments = [CommentBranch(comment) for comment in Comment.query.filter_by(parent_comment_id=self.id).all()]

def get_comment_branches(top_level_comments):
    return [CommentBranch(comment) for comment in top_level_comments]

@index_bp.route("/")
def home():
    books = list(map(lambda book:book.google_id,Book.query.all()))
    return render_template("index/home.html", books = json.dumps(books), book_count=len(books))

@index_bp.route("/book/<google_id>")
def book(google_id):
    book = Book.query.get(google_id)
    if book:
        # get top-level comments
        top_level_comments = Comment.query\
                    .filter(Comment.book_id == book.google_id)\
                    .filter(Comment.parent_comment_id == None).all()
    else:
        top_level_comments = []
    return render_template(
            "index/book.html",
            google_id=google_id,
            comments=get_comment_branches(top_level_comments)
        )

@index_bp.route("/book/<google_id>/comment", methods=["POST"])
@login_required
def comment(google_id):
    parent_comment_id = None
    try:
        if request.form["parent_comment_id"]:
            parent_comment_id = int(request.form["parent_comment_id"])
            if parent_comment_id:
                parent_comment = Comment.query.get(parent_comment_id)
    except:
        pass
    
    comment_content = request.form["comment_content"]
    comment = Comment(comment_content)
        
    user = current_user
    book = Book.query.get(google_id)
    
    if not book:
        book = Book(google_id)

    user.comments.append(comment)
    book.comments.append(comment)

    if parent_comment_id:
        comment.parent_comment_id = parent_comment_id

    db.session.commit()
    return redirect(url_for("index.book", google_id=google_id))
