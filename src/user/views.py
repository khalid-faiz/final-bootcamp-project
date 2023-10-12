from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user

from src import bcrypt, db, login_manager
from src.models import User, Book

from .forms import LoginForm, RegisterForm

import json

user_bp = Blueprint("user", __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()

def get_book_list(user: User):
    books_map = map(lambda x: {"id": x.id, "google_id": x.google_id}, user.books)
    books = json.dumps(list(books_map))
    return books

@user_bp.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("user/index.html", user=current_user)
    else:
        return redirect(url_for("user.login"))

@user_bp.route("/book", methods=["GET", "POST"])
@login_required
def book():
    if request.method == "GET":
        return render_template("user/book.html", books=get_book_list(current_user))
    elif request.method == "POST":
        google_id = request.form.get("google_id")
        book = Book.query.filter_by(google_id=google_id).first()
        if not book:
            book = Book(google_id=google_id)
            db.session.add(book)
            db.session.commit()
            current_user.books.append(book)
            db.session.commit()
        return render_template("user/book.html", books=get_book_list(current_user))

@user_bp.route("/book", methods=["DELETE"])
@login_required
def delete_book():
    args = request.args
    book_id = int(args.get("id"))
    book = Book.query.get(book_id)
    current_user.books.remove(book)
    db.session.commit()
    return render_template("user/book.html", books=get_book_list(current_user))
        
        

@user_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You are already registered.", "info")
        return redirect(url_for("index.home"))
    
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data, password=bcrypt.generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash(f"You registered and logged in {user.name}, Welcome to Bookishy", "success")

        return redirect(url_for("index.home"))
    
    return render_template("user/register.html", form=form)

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("index.home"))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect(url_for("index.home"))
        else:
            flash("Invalid email and/or password", "danger")
            return render_template("user/login.html", form=form)
    return render_template("user/login.html", form=form)

@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    return redirect(url_for("user.login"))