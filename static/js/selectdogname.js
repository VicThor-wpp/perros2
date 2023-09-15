document.addEventListener("DOMContentLoaded", function() {
    let dogName = localStorage.getItem("selectedDogName");

    if (dogName) {
        const inputElement = document.querySelector('.dogNameInput');
        inputElement.id = "dogName";
        inputElement.name = "dogName";
        inputElement.placeholder = dogName;
        inputElement.value = dogName; 
    }
});