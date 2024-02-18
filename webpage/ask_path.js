function ask_path(_start, _arrival) {
    const path = "http://127.0.0.1:8000/ask";
    const data = {
        start: _start,
        arrival: _arrival
    }
    axios.post(path, data);
}

document.addEventListener("DOMContentLoaded", function() {
    const submitBtn = document.getElementById("submitBtn");
    console.log("yo");
    submitBtn.addEventListener("click", function() {
        const startValue = document.getElementById("start").value;
        const arrivalValue = document.getElementById("arrival").value;
        console.log(startValue, arrivalValue);
        ask_path(startValue, arrivalValue);
    });
});
