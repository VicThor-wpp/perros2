document.addEventListener("DOMContentLoaded", function() {
  var loader = document.getElementById("loader");
  if (loader) {
      setTimeout(function() {
          loader.style.display = "none";
      }, 1500); 
  }

  // Array ampliado con 35 mensajes en total en español
  const messages = [
      "Buscando a los más peluditos...",
      "Colitas moviéndose...",
      "Ponte en modo patitas por un momento...",
      "Dando un último ladrido antes de mostrarse...",
      "¿Listo para un abrazo peludo?",
      "Espera un segundo, ¡están jugando!",
      "¿Has oído un aullido? ¡Eso es emoción!",
      "Meneando colas a la velocidad de la luz...",
      "¡Casi listos para la aventura perruna!",
      "Llamando a los guardianes de las galletas...",
      "Un segundo, están haciendo travesuras...",
      "Ordenando los juguetes para la presentación...",
      "Asegurando que todos tengan su correa...",
      "Puliendo narices para que brillen...",
      "Cada perro es una historia, ¿listo para leerla?",
      "Poniendo en fila a los más traviesos...",
      "Cada cola tiene su propio ritmo...",
      "Los perritos están eligiendo sus mejores poses...",
      "Los bigotes están en posición...",
      "Las huellas conducen a la felicidad...",
      "Buscando la pelota que se perdió ayer...",
      "Los perros dicen: '¡Casi listos para ti!'",
      "Buscando futuros hogares llenos de amor...",
      "Un ladrido puede ser el comienzo de una amistad eterna...",
      "Cada cola que se menea está esperando por un hogar...",
      "Estos perritos sueñan con abrazos y caricias...",
      "Ayudándoles a encontrar su felices para siempre...",
      "Un hogar no está completo sin un compañero peludo...",
      "Perritos rescatados buscando corazones que rescaten...",
      "Con cada adopción, una estrella brilla más en el cielo...",
      "Estos héroes de cuatro patas esperan por ti...",
      "Convierte un triste aullido en un feliz ladrido..."
  ];

  // Función para mostrar un mensaje aleatorio
  function showRandomMessage() {
      const randomIndex = Math.floor(Math.random() * messages.length);
      const randomMessage = messages[randomIndex];
      document.getElementById('loading-text').innerText = randomMessage;
  }

  // Llamar a la función una vez inicialmente
  showRandomMessage();

  // Cambiar el mensaje cada 2 segundos
  setInterval(showRandomMessage, 2000);

});