const images = [
    '../../data/images/instructions3D/arrived.png',
    '../../data/images/instructions3D/go_left.png',
    '../../data/images/instructions3D/go_right.png',
];

let currentIndex = 0;

const imageContainer = document.getElementById('image-container');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');

function showImage(index) {
    imageContainer.innerHTML = `<img src="${images[index]}" class="w-full h-auto">`;
}

// Could remove the modulo so that the user can't go from the last image to the first one
function showNextImage() {
    currentIndex = (currentIndex + 1) % images.length;
    //currentIndex = (currentIndex + 1) ;
    showImage(currentIndex);
}

function showPrevImage() {
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    //currentIndex = (currentIndex - 1 + images.length);
    showImage(currentIndex);
}

// Initial image display
showImage(currentIndex);

// Event listeners for navigation buttons
prevBtn.addEventListener('click', showPrevImage);
nextBtn.addEventListener('click', showNextImage);
