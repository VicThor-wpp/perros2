document.addEventListener('DOMContentLoaded', function() {
    let dogName = localStorage.getItem("selectedDogName");
    if (dogName) {
        document.getElementById("dogNameInput").value = dogName;
    }
});

document.getElementById("adoptionForm").addEventListener("submit", function (event) {
    let name = document.getElementById("name").value;
    let lastname = document.getElementById("lastname").value;
    let city = document.getElementById("city").value;
    let phone = document.getElementById("phone").value;

    if (name === "" || lastname === "" || city === "" || phone === "") {
        alert("Todos los campos son obligatorios.");
        event.preventDefault();
    }
    if (!phone.match(/[0-9]{9}/)) {
        alert("Introduce un número de teléfono válido.");
        event.preventDefault();
    }
});