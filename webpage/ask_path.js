const axios = require('axios').default;
const path = "http://127.0.0.1:8000/ask";


function ask_path(_start, _arrival) {
    data = {
        start: _start,
        arrival: _arrival
    }

    axios.get(path, {
        params: data
    })
        .then(response => {
            console.log(response.data);
        })
        .catch(error => {
            console.log(error);
        });
}

document.addEventListener("DOMContentLoaded", function() {
    const submitBtn = document.getElementById("submitBtn");
    
    submitBtn.addEventListener("click", function() {
        const startValue = document.getElementById("start").value;
        const arrivalValue = document.getElementById("arrival").value;
        console.log(startValue, arrivalValue);
        ask_path(startValue, arrivalValue);
    });
});
