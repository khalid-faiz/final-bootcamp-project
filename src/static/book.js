// Constants
const API_KEY = 'AIzaSyBO3N2mPgF_XdWZMGIdHWY_K6BTTr2fLBI';
const API_ENDPOINT = 'https://www.googleapis.com/books/v1/volumes';

// DOM elements
const iconBtns = document.querySelectorAll('.reply-icon');

async function fetchAndRender(googleId){
    let item, response;
    if (!localStorage.getItem(googleId)) {
        response = await fetch(
            `${API_ENDPOINT}/${googleId}?key=${API_KEY}`
        );
        item = await response.json();
        // Save the book data in local Storage
        localStorage.setItem(googleId, JSON.stringify(item));
    }
    else{
        itemText = localStorage.getItem(googleId);
        item = JSON.parse(itemText);
    }
    // Destructure book information from the 'item' object
    let {
        id,
        volumeInfo: {
          title,
          authors,
          description,
          pageCount,
          categories,
          publishedDate,
          imageLinks: { thumbnail },
        },
      } = item;
      document.getElementById('book-title').innerText = title;
      document.getElementById('book-author').innerText = authors.join(" & ");
      document.getElementById('book-page-count').innerText = `${pageCount} Pages`;
      document.getElementById('book-publishing-date').innerText = publishedDate;
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
    
    document.getElementById('book-description').innerText = description;
    // Set a default category if none exists
    if (!categories) {
        categories = ["Generic"];
    }
    else{
        const categorieString = categories.join(' / ');
        const duplicatedCategories = categorieString.split(' / ');
        const categoriesSet = new Set(duplicatedCategories);
        categories = Array.from(categoriesSet);
    }
    // Add the categories
    const categoryContainer = document.getElementById('book-categories');
    categories?.forEach(category => {
        const span = document.createElement('span');
        span.className = "category-badge";
        let singleCategoryList = category.split("/");
        span.innerText = singleCategoryList[singleCategoryList.length-1];
        categoryContainer.appendChild(span);
    });
    // Add the image
    const bookImages = document.querySelectorAll(".book-image");
    bookImages.forEach(image => image.src = thumbnail);
}

// rendering the book's page
const googleId = document.getElementById("book-data-dict").innerText

fetchAndRender(googleId);


iconBtns.forEach(actionBtn=>{
   actionBtn.addEventListener('click', (event)=>{
    const parent = event.target.parentElement;
    const replyInput = parent.children[0];
    if (replyInput.classList.contains('hidden-input')) {
      replyInput.classList.remove("hidden-input");
      replyInput.classList.remove("collapse-input");
    }
    else{
      replyInput.classList.add("hidden-input");
      replyInput.classList.add("collapse-input");
    }
  })
})