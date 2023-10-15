import json
from flask import Blueprint, render_template, request
from src.models import User, Book, Category, Comment, Rating

index_bp = Blueprint("index", __name__)


@index_bp.route("/")
def home():
    return render_template("index/home.html")

@index_bp.route("/book")
def book():
    args = request.args
    book_id = args.get("id")
    
    google_id = args.get("google_id")
    book = json.dumps({"book_id":book_id, "google_id":google_id})
    print(book)
    return render_template("index/book.html", book=book)