// Constants
const API_KEY = 'AIzaSyBO3N2mPgF_XdWZMGIdHWY_K6BTTr2fLBI';
const API_ENDPOINT = 'https://www.googleapis.com/books/v1/volumes';

// DOM elements
const searchInput = document.getElementById('search-keyword');
const searchMessage = document.getElementById("search-message");
const resultsContainer = document.getElementById('results');
const userBookContainer = document.getElementById('books-container');


// Function to create HTML for a book card
function createBookCardHTML(item, withAddButton = true, bookDbId) {
  try {
    // Destructure book information from the 'item' object
    let {
      id,
      volumeInfo: {
        title,
        authors,
        description,
        pageCount,
        categories,
        imageLinks: { thumbnail },
      },
    } = item;

    // Sanitize and limit the description length
    if (description) {
      // Created an element because sometime the des.
      // is HTML, I want pure text.
      let span = document.createElement("span");
      span.innerHTML = description;
      description = span.textContent || span.innerText;
    } else {
      description = "No description";
    }
    // Set a default category if none exists
    if (!categories) {
      categories = ["Generic"];
    }

    const mainCategory = categories[0];

    // Define action button based on 'withAddButton' parameter
    let actionBtn = withAddButton
      ? `<form action="/user/book" method="POST">
                <input type="hidden" name="google_id" value="${id}">
                <button style="border-bottom-left-radius: 0 !important" class="btn rounded-0 rounded-bottom btn-success">Add
                to Library</button>
            </form>`
      : `<a class="btn btn-danger" onclick="fetch('/user/book?id=${bookDbId}', {method:'DELETE'}).then(() => {
                window.location.reload();
            })">Remove</a>`;

    // Generate the book card HTML
    let card = `
        <div class="col-sm-12 card p-1" style="max-width: 540px;">
            <div class="card-header text-muted">${mainCategory}</div>
            <div class="row g-0">
            <div class="col-4">
                <img class="rounded-0 card-img" src="${thumbnail}">
            </div>
            <div class="col-8">
                <div class="card-body ms-3">
                <h5 class="card-title">${title}</h5>
                <p class="card-text">${
                  description.length >= 250
                    ? description.slice(0, 249) + "..."
                    : description
                }</p>
                </div>
            </div>
            </div>
            <div class="btn-group" role="group">
            <button style="border-bottom-right-radius: 0 !important" type="button"
                class="btn rounded-0 rounded-bottom btn-secondary">Descussion</button>
            ${actionBtn}
            </div>
        </div>
        `;
    return card;
  } catch (error) {
    return ""; // Handle errors by returning an empty string
  }
}


// Function to fetch books and populate the container
async function fetchBooks(keyword, isFromIDsArray = false) {
  let books, booksArray, container;
  // If the user is searching
  if (!isFromIDsArray) {
    container = resultsContainer;
    // Fetch book data from the Google Books API
    const response = await fetch(
      `${API_ENDPOINT}?q=${keyword}&key=${API_KEY}`
    );
    const { items } = await response.json();
    booksArray = [...items];
  }
  // For showing user's books
  else {
    container = userBookContainer;
    // Get the book list from the DOM
    books = JSON.parse(container.innerText);
    console.log(books);
    booksArray = [];
    let item, response;
    // Fetch individual book data for each book in 'books'
    for (let index = 0; index < books.length; index++) {
      const book = books[index];
      const google_id = book.google_id;
      // Check if the book data is not in the localStorage
      if (!localStorage.getItem(google_id)) {
        // Fetch the book data from Google Books API
        response = await fetch(
          `${API_ENDPOINT}/${book.google_id}?key=${API_KEY}`
        );
        item = await response.json();
        // Save the book data in local Storage
        localStorage.setItem(book.google_id, JSON.stringify(item));
      }
      else {
        itemText = localStorage.getItem(book.google_id);
        item = JSON.parse(itemText);
      }
      booksArray.push(item);
    }
  }

  
  // Create HTML for book cards and populate the container
  let rows = "";
  for (let index = 0; index < booksArray.length; index++) {
    const item = booksArray[index];
    const card = createBookCardHTML(
      item,
      !isFromIDsArray,
      books ? books[index].id : ""
    );
    rows += card;
  }
  console.log(container);
  container.innerHTML = rows;
  container.style.display = "grid";
}


// Define the search event handeler
let timeout;
const handleSearch = (event)=>{
  let keyword = event.target.value;
  clearTimeout(timeout);
  timeout = setTimeout(()=>{
    if (keyword.trim().length < 2) {
      const messageHTML = `
        <div class="col-3"></div>
          <div class="col-6">
            <div class="alert alert-warning alert-dismissible fade show" role="alert">
              Please type some more
              <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
          </div>
        <div class="col-3"></div>`;
      searchMessage.innerHTML = messageHTML;
    }
    else{
      searchMessage.innerHTML = '';
      fetchBooks(keyword);
    }
  }, 750)
}

// Add an even listener for the input
searchInput.addEventListener('input', handleSearch);
searchInput.addEventListener('keyup', (event)=>{
  if (event.key == "Enter") {
    let keyword = event.target.value;
    handleSearch(event);
    event.target.value = '';
  }
})

// Fetch books and populate the container (isFromIDsArray = true for the initial load)
fetchBooks('', isFromIDsArray = true);
