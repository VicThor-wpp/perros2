document.addEventListener("DOMContentLoaded", function () {
  let currentPath = window.location.pathname;
  let menuItems = document.querySelectorAll(".menu a");

  menuItems.forEach((item) => {
    if (item.getAttribute("href") === currentPath) {
      item.classList.add("active");
    }
  });
});
