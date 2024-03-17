// const images =
let images = JSON.parse(sessionStorage.getItem("images")) || [];
console.log(images);

// Here we would listen to the api response and depending on the strings we have we would create a
// the vector of images by appending the values of the previously defined variables.

// Once we have the vector of images we would just iterate over it with the buttons.

// We would need to also store the order in which the commands arrive so we can put the images in the correct order
// and the user can navigate through them with the buttons.

let currentIndex = 0;

const imageContainer = document.getElementById("image-container");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");

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
prevBtn.addEventListener("click", showPrevImage);
nextBtn.addEventListener("click", showNextImage);
