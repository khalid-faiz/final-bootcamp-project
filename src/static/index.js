// Constants
const API_KEY = 'AIzaSyBO3N2mPgF_XdWZMGIdHWY_K6BTTr2fLBI';
const API_ENDPOINT = 'https://www.googleapis.com/books/v1/volumes';
// Get book ids from DOM, appended in python
const bookGoogleIds = JSON.parse(document.getElementById("book-id-list").innerText);

// Function to fetch books and populate the container
async function fetchBooks(bookGoogleIds, childBookContainers) {
    console.log(childBookContainers);
    // Fetch individual book data for each google id
    for (let index = 0; index < bookGoogleIds.length; index++) {
        const bookGoogleId = bookGoogleIds[index];
        const divCarouselItem = childBookContainers[index];
        let volumeInfo, imageLinks, thumbnail;
        if (!localStorage.getItem(bookGoogleId)) {
            // Fetch the book data from Google Books API
            response = await fetch(
                `${API_ENDPOINT}/${bookGoogleId}?key=${API_KEY}`
            );
            ;({
                volumeInfo: {
                    imageLinks: { thumbnail }
                }
            } = await response.json())
            // Save the book data in local Storage
            localStorage.setItem(bookGoogleId, JSON.stringify(item));
        } else {
            itemText = localStorage.getItem(bookGoogleId);
            ;({
                volumeInfo: {
                    imageLinks: { thumbnail }
                }
            } = JSON.parse(itemText));
        }
        divCarouselItem.style.backgroundImage = `url(${thumbnail})`;
        divCarouselItem.dataset.href = `/book/${bookGoogleId}`;

    }
}

fetchBooks(bookGoogleIds, document.querySelectorAll('.slider-item'));


document.addEventListener('DOMContentLoaded', () => {

//------ Slider Begin
const carousel = document.querySelector('.carousel-slider');
const carouselSlider = new MicroSlider(carousel, { indicators: false });
const hammer = new Hammer(carousel);
const carouselTimer = 2000;
let carouselAutoplay = setInterval(() => carouselSlider.next(), carouselTimer);

//------- Mouseenter Event
carousel.onmouseenter = function(e) {
    clearInterval(carouselAutoplay); 
}

//----- Mouseleave Event
carousel.onmouseleave = function(e) {
    clearInterval(carouselAutoplay); 
    carouselAutoplay = setInterval(() => carouselSlider.next(), carouselTimer);
}

//----- Mouseclick Event
carousel.onclick = function(e) {
    clearInterval(carouselAutoplay); 
}

//------ Gesture Tap Event
hammer.on('tap', function(e) {
    clearInterval(carouselAutoplay);
});

//----- Gesture Swipe Event
hammer.on('swipe', function(e) {
    clearInterval(carouselAutoplay); 
    carouselAutoplay = setInterval(() => carouselSlider.next(), carouselTimer);
});

let slideLink = document.querySelectorAll('.slider-item');
if (slideLink && slideLink !== null && slideLink.length > 0){
    slideLink.forEach( el => el.addEventListener('click', e => {
        e.preventDefault();
        let href = el.dataset.href;
        let target = el.dataset.target;
        if (href !== '#' &&  e.target.classList.contains('active')) window.open(href, target);
    }));
}
});