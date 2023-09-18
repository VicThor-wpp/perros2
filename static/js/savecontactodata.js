function submitAdoptionForm(e) {

    e.preventDefault();



    var formData = new FormData(document.getElementById('adoptionForm'));



    fetch('https://script.google.com/macros/s/AKfycbwMBTxK4WqW_zAMyiyQqQpWUs-ts0PKpjguGmOLg4271oQ3DR5EPaeLoaR_-NHgokFt/exec', {

        method: 'POST',

        body: formData

    })

        .then(response => response.text())

        .then(data => {

            // Update the modal's content with the server's response

            document.getElementById('modalMessage').innerHTML = "<h3>Tus datos se enviaron correctamente</h3><br>Nos pondremos en contacto a la brevedad.<br> ¡Muchas gracias!";



            // Display the modal

            var modal = document.getElementById("myModal");

            modal.style.display = "block";



            // Reset the form

            resetForm();



            // When the user clicks on <span> (x), close the modal

            document.getElementsByClassName("close")[0].onclick = function () {

                modal.style.display = "none";

            }



            // When the user clicks anywhere outside of the modal, close it

            window.onclick = function (event) {

                if (event.target == modal) {

                    modal.style.display = "none";

                }

            }

        })

        .catch(error => {

            console.error('There was an error submitting the form!', error);

        });

}



function resetForm() {

    document.getElementById('adoptionForm').reset();

}