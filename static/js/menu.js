const menuToggle = document.getElementById("menu-toggle");
const menu = document.getElementById("menu");

menuToggle.addEventListener("click", () => {
    menu.classList.toggle("active");
    menuToggle.classList.toggle("active");
});

// Cierra el menú si se hace clic en un enlace del menú
menu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
        menu.classList.remove("active");
        menuToggle.classList.remove("active");
    });
});
