const { unregisterCustomQueryHandler } = require("puppeteer");

document.addEventListener("DOMContentLoaded", function () {
    const items = document.querySelectorAll(".clickable-item");

    items.forEach(function (item) {
        item.addEventListener("mouseover", function () {
        this.style.transform = "scale(1.1)";
        });

        item.addEventListener("mouseout", function () {
        this.style.transform = "scale(1)";
        });
    });
});

// Not sure if the code above is even necesarry
// The code below is for the form toggling
var currentFormId = null;


function toggleForm(formId) {
    var buildingForm = document.getElementById("buildingForm");
    var classroomForm = document.getElementById("classroomForm");

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
        // Should also store user actual position from localisation.js somehow
        var input = document.getElementById("building").value;
        // getUserPosition();
        // alert(input);
        sendBuildingRequest(input);
    } else if (formId === "class") {
        var inputSrc = document.getElementById("classSrc").value;
        var inputDst = document.getElementById("classDst").value;
        alert(inputSrc + " " + inputDst);
    }
    // var input = document.getElementById(formId).value;
    // alert(input);
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



function sendBuildingRequest(input) {
    getUserPosition()
        .then(userPosition => {
            console.log(userPosition);
            const data = {
                start: [userPosition.lat, userPosition.long],
                arrival: input
            };
            // console.log("This is the data " + data);

            fetch("http://127.0.0.1:8000/api/ask_outside", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            })
            .then(response => response.json())
            .then(data => {
                // Handle the response from the FastAPI server
                console.log("The data received from the fastapi server " + data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        })
        .catch(error => {
            console.error(error);
        });
}

function sendClassroomRequest(inputSrc, inputDst) {
    const data = {
        start: inputSrc,
        arrival: inputDst
    };

    fetch("http://127.0.0.1:8000/api/ask_inside", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response from the api server
        console.log(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}