document.addEventListener("DOMContentLoaded", function() {

  document.getElementById('adoptionForm').addEventListener('submit', submitAdoptionForm);

  function submitAdoptionForm(e) {
      let dogName = localStorage.getItem("selectedDogName");
      e.preventDefault();
  
      var formData = new FormData(document.getElementById('adoptionForm'));
  
      fetch('https://script.google.com/macros/s/AKfycbwMBTxK4WqW_zAMyiyQqQpWUs-ts0PKpjguGmOLg4271oQ3DR5EPaeLoaR_-NHgokFt/exec', {
          method: 'POST',
          body: formData
      })
      .then(response => response.text())
      .then(data => {
          // Actualizar el contenido del modal con la respuesta del servidor
          document.getElementById('modalMessage').innerHTML = "<h3>Tus datos se enviaron correctamente</h3><br>Nos pondremos en contacto a la brevedad.<br> ¡Muchas gracias!";

          // Mostrar el modal
          var modal = document.getElementById("myModal");
          modal.style.display = "block";

          // Al hacer clic en <span> (x), cerrar el modal
          document.getElementsByClassName("close")[0].onclick = function() {
              modal.style.display = "none";
          }

          // Al hacer clic fuera del modal, cerrarlo
          window.onclick = function(event) {
              if (event.target == modal) {
                  modal.style.display = "none";
              }
          }

          // Datos para el mensaje de WhatsApp
          let name = document.getElementById('name').value;
          let lastname = document.getElementById('lastname').value;
          let city = document.getElementById('city').value;
          let phone = document.getElementById('phone').value;

          let message = `Hola, mi nombre es ${name} ${lastname} de la ciudad de ${city}, te contacto desde https://sebuscahumano.com/. Estoy interesado en adoptar a ${dogName}. Mi número de teléfono es ${phone}. ¡Gracias!`;
          let whatsappURL = `https://wa.me/59894767181?text=${encodeURIComponent(message)}`;

          // Abre una ventana emergente de inmediato, pero solo carga 'about:blank' por ahora
          window.open(`${whatsappURL}`, '_blank');

          resetForm();

      })
      .catch(error => {
          console.error('Hubo un error al enviar el formulario!', error);
      });
  }

  function resetForm() {
      document.getElementById('adoptionForm').reset();
  }

});
