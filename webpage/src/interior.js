let images = JSON.parse(sessionStorage.getItem("images")) || [];
let instructions = JSON.parse(sessionStorage.getItem("instructions")) || [];
let sameBuilding = JSON.parse(sessionStorage.getItem("sameBuilding"));

// Here we would listen to the api response and depending on the strings we have we would create a
// the vector of images by appending the values of the previously defined variables.

// Once we have the vector of images we would just iterate over it with the buttons.

// We would need to also store the order in which the commands arrive so we can put the images in the correct order
// and the user can navigate through them with the buttons.

let currentIndex = 0;

const imageContainer = document.getElementById("image-container");
const arrivedBtn = document.getElementById("arrivedBtn");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const imageLabel = document.getElementById("image-label");

function showImage(index) {
	imageContainer.innerHTML = `<img src="${images[index]}" class="w-full h-auto">`;
    imageLabel.textContent = instructions[index];
}

function showNextImage() {
    if (currentIndex < images.length - 1) {
        currentIndex = (currentIndex + 1);
        if (currentIndex === images.length - 1 && !sameBuilding) {
            arrivedBtn.style.display = "block";
        }
    }
	showImage(currentIndex);
}

function showPrevImage() {
    if (currentIndex > 0) {
        currentIndex = (currentIndex - 1);
    }
	showImage(currentIndex);
}

function arrivedClick() {
    let image1 = JSON.parse(sessionStorage.getItem("finalImages")) || [];
    sessionStorage.setItem("images", JSON.stringify(image1));
    let instructions1 = JSON.parse(sessionStorage.getItem("finalInstructions")) || [];
    sessionStorage.setItem('sameBuilding', JSON.stringify(true));
    sessionStorage.setItem("instructions", JSON.stringify(instructions1));
    window.location.href = "localisation.html";
}

// Initial image display
showImage(currentIndex);

// Event listeners for navigation buttons
prevBtn.addEventListener("click", showPrevImage);
nextBtn.addEventListener("click", showNextImage);
arrivedBtn.addEventListener("click", arrivedClick);
