# This is The Final EPFL Project

## App Description

Book-ishy is supposed to be a platform for readers, where they can add thier books, track thier progress, and add some notes in each book they add.

Also, users can view public books, which are added for the admin user page to moderate them, when ever 2 or more users have the same book. After approval, they become public books, which authenticated users can comment on, and comment on other peoples comments.

A user is able to apply full CRUD operations on anything related to them, whether it is a book, a comment or thier accout itself.

## Database

The app will use a SQLAlchemy (sqlite as a starter db) database, with six tables.

Edit: I'll use google book api, so things are easier.

### `user`

Containing these columns:

1. `id`: Automatically generated.
2. `name`: Unique string field.
3. `email`: Unique valid email address (not necessairly working, but with a valid format).
4. `password`: Hashed then stored.

### `book`

1. `id`.
2. `google_id`: to retrive book's data from google.
4. `is_public`: a boolean to indicate if the book is public.

### `category`

1. `id`.
2. `name`: Unique string field.

### `comment`

1. `id`.
2. `content`.
3. `timestamp`.
4. `is_deleted`: to indicate the comment has been deleted..
5. `is_edited`: to indicate the comment has been edited by the user.

### Relational Tables

#### `user_book`: many-to-many

1. `id`.
2. FK: `user.id`.
3. FK: `book.id`.
4. `status`: 0,1,2 indicating to-read, reading and read.
5. `notes`: user notes on this book.

#### `user_category`: many-to-many

1. `id`.
2. FK: `user.id`.
3. FK: `category.id`.

#### `book_category`: many-to-many

1. `id`.
2. FK: `book.id`.
3. FK: `category.id`.

### `book_user_comment`: many-to-many

1. `id`.
2. FK: `comment.id`.
3. FK: `book.id` but the book in question should have `is_public` with a value of `1`.
4. FK: `user.id`.
5. FK: `book_user_comment.id`, for creating nested comments, if it's null, then will be a top-tree comment.

### `book_user_rating`: many-to-many

1. `id`.
2. `rating`: a string from 1-5.
3. FK: `book.id` but the book in question should have `is_public` with a value of `1`.
4. FK: `user.id`.

## Veiws

Here are the views for the app:

- `/`:
  1. Shows buttons for: `/user/login` `/user/register` if the user.is_authenticated (with a session manager), else `/user` `/user/logout`.
  2. Shows input fields for searching/filtering for books, or users. Results from either public books (where book.is_public).
  3. Shows a list of public books. Where it redirects to `/book/<int:book.id>`, Then a user can add a rating, or comment.
     * Adding a comment through the route `POST /book/<int:book.id>/comment`.
       - Deleting a comment through `DELETE /book/<int:book.id>/comment/<int:comment.id>`.
       - Editing a comment through `PUT /book/<int:book.id>/comment/<int:comment.id>`.
- `/user`:
  1. Shows profile data if the user is authenticated. Else it redirects to `/user/register` with a 401 status code.
  2.  `PUT /user`: edit the user profile with the same condition as 1.
  3.  `DELETE /user`: delete the user profile with the same condition as 1.
  4.  `/user/login`: login for old users.
  5.  `/user/register`: register a new user.
  6.  `/user/book`: GET shows a list of user books, and POST adds a new book.
      * `/user/book/<int:book.id>`: shows a book's data.
      * `DELETE /user/book/<int:book.id>`: delete a book.
      * `PUT /user/book/<int:book.id>`: edit a book.

## Searching and Filtering

Now the important thing that worth noting, the search and filter functionality which will be available for almost all the data we have. With the following features.

1. On home page: Filter search results based on public books (title, description or category), usernames (category interests), or comments.
