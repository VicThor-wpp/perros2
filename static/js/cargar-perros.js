fetch("static/js/data/perros.json")
  .then((response) => response.json())
  .then((data) => {
    const grid = document.querySelector(".image-grid");
    grid.innerHTML = "";

    data.forEach((perro) => {
      const item = document.createElement("div");
      item.className = "image-item";

      const botonesver = document.createElement("div");
      botonesver.className = "botonesver";

      const img = document.createElement("img");
      img.src = `static/perritos/${perro.imagen}`;
      img.alt = perro.nombre;

      const h2 = document.createElement("h2");
      h2.textContent = perro.nombre;

      const a = document.createElement("a");
      a.href = "contacto";
      a.className = "button";
      a.textContent = "Adoptar";

      const vermas = document.createElement("a");
      vermas.href = "vermas";
      vermas.className = "button";
      vermas.textContent = "Ver más";

      // Add event listener to the link to save dog's name to local storage
      a.addEventListener("click", (e) => {
        localStorage.setItem("selectedDogName", perro.nombre);
      });

      // Agregar este evento al enlace vermas para guardar la información del perro seleccionado
      vermas.addEventListener("click", (e) => {
        localStorage.setItem("selectedDogInfo", JSON.stringify(perro));
      });

      item.appendChild(img);
      item.appendChild(h2);
      botonesver.appendChild(a);
      botonesver.appendChild(vermas);
      item.appendChild(botonesver);

      grid.appendChild(item);
    });
  })
  .catch((error) => {
    console.error("Hubo un problema con la petición Fetch:", error);
  });
