document.addEventListener("DOMContentLoaded", function() {
    var loader = document.getElementById("loader");
    if (loader) {
        setTimeout(function() {
            loader.style.display = "none";
        }, 1500); 
    }
});
