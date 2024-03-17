import { updateState, addObserver, getState } from './state.js';

// Définir un observateur pour surveiller les changements d'état
const stateObserver = () => {
    const newState = getState();
    console.log('New state:', newState);
    // Mettez à jour votre interface utilisateur en fonction du nouvel état ici
};

// Ajouter l'observateur
addObserver(stateObserver);

document.addEventListener("DOMContentLoaded", function () {
    const items = document.querySelectorAll(".clickable-item");
    const buildingButton = document.getElementById("buildingButton");
    const classroomButton = document.getElementById("classroomButton");
    const buildingSubmit = document.getElementById("buildingSubmit");
    const classroomSubmit = document.getElementById("classroomSubmit");

    buildingButton.addEventListener("click", function () {
        toggleForm("buildingForm");
    });

    classroomButton.addEventListener("click", function () {
        toggleForm("classroomForm");
    });

    buildingSubmit.addEventListener("click", function () {
        submitInput("building");
    });

    classroomSubmit.addEventListener("click", function () {
        submitInput("classroom");
    });


    items.forEach(function (item) {
        item.addEventListener("mouseover", function () {
            this.style.transform = "scale(1.1)";
        });

        item.addEventListener("mouseout", function () {
            this.style.transform = "scale(1)";
        });
    });
});

// Not sure if the code above is even necessary
// The code below is for the form toggling
let currentFormId = null;

function toggleForm(formId) {
    const buildingForm = document.getElementById("buildingForm");
    const classroomForm = document.getElementById("classroomForm");

    // Means that the same button is clicked again
    if (currentFormId === formId) {
        if (formId === "buildingForm") {
            buildingForm.classList.toggle("hidden");
        } else if (formId === "classroomForm") {
            classroomForm.classList.toggle("hidden");
        }
        // If the same button is clicked again, toggle visibility

        // Means that a different button is clicked
    } else {
        // Hide the form associated with the previously clicked button
        if (currentFormId === "buildingForm") {
            buildingForm.classList.add("hidden");
        } else if (currentFormId === "classroomForm") {
            classroomForm.classList.add("hidden");
        }

        // Show the form associated with the currently clicked button
        if (formId === "buildingForm") {
            buildingForm.classList.remove("hidden");
        } else if (formId === "classroomForm") {
            classroomForm.classList.remove("hidden");
        }

        // Update the currentFormId
        currentFormId = formId;
    }
}

// The code below is for the form submission when clicking on the submit button
function submitInput(formId) {
    if (formId === "building") {

        const input = document.getElementById("building").value;
        navigator.geolocation.getCurrentPosition(function(position) {
            const coords = [position.coords.latitude, position.coords.longitude];
            sendBuildingRequest(coords, input);
        });

    } else if (formId === "class") {
        const inputSrc = document.getElementById("classSrc").value;
        const inputDst = document.getElementById("classDst").value;
        sendClassroomRequest(inputSrc, inputDst);
    }
}

function getUserPosition() {
    // A Promise is a proxy for a value not necessarily known when the promise is created.
    return new Promise((resolve, reject) => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    let userLat = position.coords.latitude;
                    let userLng = position.coords.longitude;
                    resolve({lat:userLat, long:userLng});
                },
                function(error) {
                    reject(error);
                }
            );
        } else {
            reject("Geolocation is not supported by this browser.");
        }
    });
}

function sendBuildingRequest(_start, _arrival) {
    const data = {
        start: _start,
        arrival: _arrival
    };
    fetch("http://127.0.0.1:8000/api/ask_outside", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })
    .then(response => {
    if (response.ok) {
        // TODO
        return response.json();
    }
    throw new Error('Network response was not ok.');
    })
    .then(data => {
        // Handle the response from the FastAPI server
        console.log("The data received from the fastapi server " + data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function sendClassroomRequest(inputSrc, inputDst) {
    const data = {
        start: inputSrc,
        arrival: inputDst
    };

    fetch("http://127.0.0.1:8000/api/ask_from_inside", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        if (data.same_building) {
            manageSameBuilding(data);
        }
        // Handle the response from the api server
        console.log(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function manageSameBuilding(data){
    updateState({
        path: data.path,
        images: data.images,
        arrival_building: true,
        first_images: null
    });

    window.location.href = "interior.html";
}

function manageDifferentBuilding(data){
    updateState({
        path: data.path,
        images: data.images,
        arrival_building: false,
        first_images: data.first_building_images
    });

    window.location.href = "interior.html";
}
