function createBookCardHTML(item, withAddButton = true, bookDbId) {
  try {
    let {
      id,
      volumeInfo: {
        title,
        subtitle,
        authors,
        description,
        pageCount,
        categories,
        imageLinks: { thumbnail },
      },
    } = item;
    if (description) {
      let span = document.createElement("span");
      span.innerHTML = description;
      description = span.textContent || span.innerText;
    } else {
      description = "No description";
    }
    if (!categories) {
      categories = ["Generic"];
    }
    const mainCategory = categories[0];
    let actionBtn = withAddButton
      ? `<form action="/user/book" method="POST">
                <input type="hidden" name="google_id" value="${id}">
                <button style="border-bottom-left-radius: 0 !important" class="btn rounded-0 rounded-bottom btn-success">Add
                to Library</button>
            </form>`
      : `<a class="btn btn-danger" onclick="fetch('/user/book?id=${bookDbId}', {method:'DELETE'}).then(() => {
                window.location.reload();
            })">Remove</a>`;
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
    return "";
  }
}
async function fetchBooks(isFromIDsArray = false) {
  let books, booksArray, container;
  if (!isFromIDsArray) {
    container = document.getElementById("results");
    let kw = document.getElementById("search-keyword").value;
    const response = await fetch(
      `https://www.googleapis.com/books/v1/volumes?q=${kw}&key=AIzaSyBO3N2mPgF_XdWZMGIdHWY_K6BTTr2fLBI`
    );
    const { items } = await response.json();
    booksArray = [...items];
  } else {
    container = document.getElementById("books-container");
    books = JSON.parse(container.innerText);
    booksArray = [];
    let item, response;
    for (let index = 0; index < books.length; index++) {
      const book = books[index];
      response = await fetch(
        `https://www.googleapis.com/books/v1/volumes/${book.google_id}`
      );
      item = await response.json();
      booksArray.push(item);
    }
  }

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
  container.innerHTML = rows;
  container.style.display = "grid";
  console.log(booksArray);
}
fetchBooks((isFromIDsArray = true));
