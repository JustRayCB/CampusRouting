import { addObserver, getState } from "./state.js";

// Here we would listen to the api response and depending on the strings we have we would create a
// the vector of images by appending the values of the previously defined variables.

// Once we have the vector of images we would just iterate over it with the buttons.

// We would need to also store the order in which the commands arrive so we can put the images in the correct order
// and the user can navigate through them with the buttons.

let currentIndex = 0;
let images = getState().images;
const imageContainer = document.getElementById('image-container');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const arrivedBtn = document.getElementById('arrivedBtn');

function showImage(index) {
    const state = getState();
    if (state.arrival_building) {
        images = state.images;
    } else {
        images = state.first_images;
    }
    imageContainer.innerHTML = `<img src="${images[index]}" class="w-full h-auto">`;
}

// Could remove the modulo so that the user can't go from the last image to the first one
function showNextImage() {
    currentIndex = (currentIndex + 1) % images.length;
    if ( currentIndex === images.length - 1 ){
        nextBtn.classList.add('hidden');
        arrivedBtn.style.display = 'inline-block';
    }
    showImage(currentIndex);
}

function showPrevImage() {
    if (currentIndex === images.length - 1){
        nextBtn.classList.remove('hidden');
        arrivedBtn.style.display = 'none';
    }
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    showImage(currentIndex);
}

function clickArrived() {
    // TODO
    window.location.href = "/welcome";
}

// Initial image display
console.log(images);
showImage(currentIndex);

// Event listeners for navigation buttons
prevBtn.addEventListener('click', showPrevImage);
nextBtn.addEventListener('click', showNextImage);
arrivedBtn.addEventListener('click', clickArrived);

// Ajouter un observateur pour mettre à jour les images lorsque l'état change
const stateObserver = () => {
    images = getState().images;
    showImage(currentIndex);
};

// Ajouter l'observateur
addObserver(stateObserver);
