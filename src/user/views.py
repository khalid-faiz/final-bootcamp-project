# Import necessary modules and components from Flask, Flask-Login,
# And the application module
import json

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user

from src import bcrypt, db, login_manager
from src.models import User, Book
from .forms import LoginForm, RegisterForm

# Create a Blueprint named "user" to organize routes and views related to
# User management
user_bp = Blueprint("user", __name__)


# Define a user loader function to retrieve a User object by its ID
# Needed for authentication
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()


# Define a function to get a list of books associated with a user as a
# JSON string
def get_book_ids_list(user: User):
    # Map the user's books to a list of dictionaries with book information
    book_ids_map = map(lambda book: book.google_id , user.books)
    # Convert the list of dictionaries to a JSON string and return it
    book_ids = json.dumps(list(book_ids_map))
    return book_ids


# Route for the /user page, accessible only when a user is authenticated
@user_bp.route("/")
def index():
    if current_user.is_authenticated:
        # Render the user's page with user information
        return render_template("user/index.html", user=current_user)
    else:
        # Redirect to the login page if the user is not authenticated
        return redirect(url_for("user.login"))


# Route for managing books:
# Allows displaying user's books, adding, or deleting a book
@user_bp.route("/book", methods=["GET", "POST", "DELETE"])
@login_required
def book():
    # Add a new book
    if request.method == "POST":
        # Check if the book with the given Google ID exists
        google_id = request.form.get("google_id")
        book = Book.query.get(google_id)
        if not book:
            # If the book doesn't exist
            # Create a new Book object and add it to the database
            book = Book(google_id)
            db.session.add(book)
            db.session.commit()

        # Add the book to the user's list of books
        try:
            # Assert that the book isn't aleady in the user's list
            assert current_user.books.count(book) == 0
            current_user.books.append(book)
            db.session.commit()
        # On if assertion failed, flash a massage to the user
        except AssertionError:
            flash("This book is already in your library", "info")
        return redirect(url_for("user.book"))

    # Delete a user's book
    elif request.method == "DELETE":
        args = request.args
        book_id = args.get("google_id")
        # Retrieve the Book object to be deleted by its ID
        book = Book.query.get(book_id)
        # Remove the book from the user's list of books and commit the changes
        current_user.books.remove(book)
        db.session.commit()

    # Return the updated list of user's books
    return render_template("user/book.html", books=json.dumps([book.google_id for book in current_user.books]))


# Route for user registration, allowing new users to create an account
@user_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        # If the user is already authenticated, display a message and redirect
        flash("You are already signedup.", "info")
        return redirect(url_for("index.home"))

    # Create a registration form
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        # Create a new User object with the provided registration information
        user = User(
            name=form.name.data, 
            email=form.email.data, 
            password=bcrypt.generate_password_hash(form.password.data)
            )
        db.session.add(user)
        db.session.commit()

        # Log in the newly signedup user and display a success message
        login_user(user)
        flash(
            f"You signedup and logged in {user.name}, Welcome to Bookishy", 
            "success"
            )

        # Redirect to the home page
        return redirect(url_for("index.home"))
    
    # Render the registration page with the registration form 
    # for "GET" requests
    return render_template("user/signup.html", form=form)


# Route for user login, allowing signedup users to log in to their accounts
@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        # If the user is already authenticated, display a message and redirect
        flash("You are already logged in.", "info")
        return redirect(url_for("index.home"))

    # Create a login form
    form = LoginForm(request.form)
    if form.validate_on_submit():
        # Query the database for a user with the provided email
        user = User.query.filter_by(email=form.email.data).first()
        submit_pw = request.form["password"]
        if user and bcrypt.check_password_hash(user.password, submit_pw):
            # If the user exists and the password matches, log in the user
            login_user(user)
            # Then redirect to home page
            return redirect(url_for("index.home"))
        else:
            # If the login fails, display an error message
            flash("Invalid email and/or password", "danger")
            # Render the login page with the login form
            return render_template("user/login.html", form=form)
    # For "GET" requests render the login page
    return render_template("user/login.html", form=form)


# Route for user logout, allowing users to log out of their accounts
@user_bp.route("/logout")
@login_required
def logout():
    # Log the user out and display a success message
    logout_user()
    flash("You were logged out.", "success")
    # Redirect to the login page
    return redirect(url_for("user.login"))