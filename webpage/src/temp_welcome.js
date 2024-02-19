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
  