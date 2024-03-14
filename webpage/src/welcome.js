
class PathRequestInside {
  constructor(start, arrival) {
    this.start = start;
    this.arrival = arrival;
  }
}

class PathRequestOutside {
  constructor(start, arrival) {
    this.start = start;
    this.arrival = arrival;
  }
}

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
const axios = require('axios');

// The code below is for the form submission when clicking on the submit button
function submitInput(formId) {
    if (formId === "building") {
        // Should also store user actual position from localisation.js somehow
        const input = document.getElementById("building").value;
        navigator.geolocation.getCurrentPosition(function(position) {
            const coords = [position.coords.latitude, position.coords.longitude];

            sendPathRequestOutside(new PathRequestOutside(input, coords))
                .then(r => {
                    if (r.status === 200) {
                        console.log("Success");
                    } else {
                        console.log("Failure");
                    }
                })
                .catch(error => {
                    console.error("Error:", error);
                });
        });


    } else if (formId === "class") {
        const inputSrc = document.getElementById("classSrc").value;
        const inputDst = document.getElementById("classDst").value;
        sendPathRequestFromClassroom(new PathRequestInside(inputSrc, inputDst))
          .then(r => {
            if (r.status === 200) {
              console.log("Success");
            } else {
              console.log("Failure");
            }
          })
          .catch(error => {
            console.error("Error:", error);
          });
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

async function sendPathRequestInside(request) {
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/ask_inside', request);
    console.log('Réponse de la requête Inside:', response.data);
    if (response.status === 200) {
      window.location.href = 'interior.html';
    }
  } catch (error) {
    console.error('Erreur lors de la requête Inside:', error);
  }
}

// Fonction pour envoyer une requête correspondant à PathRequestOutside
async function sendPathRequestOutside(request) {
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/ask_outside', request);
    console.log('Réponse de la requête Outside:', response.data);
    if (response.status === 200) {
      window.location.href = 'localisation.html';
    }
  } catch (error) {
    console.error('Erreur lors de la requête Outside:', error);
  }
}

async function sendPathRequestFromClassroom(request) {
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/ask_from_inside', request);
    console.log('Réponse de la requête Classroom:', response.data);
    return response;

    } catch (error) {
      console.error('Erreur lors de la requête Classroom:', error);
    }
}
