import json
from flask import Blueprint, render_template, request
from src.models import User, Book, Category, Comment, Rating

index_bp = Blueprint("index", __name__)


@index_bp.route("/")
def home():
    return render_template("index/home.html")

@index_bp.route("/book/<google_id>")
def book(google_id):
    return render_template("index/book.html", google_id=google_id)