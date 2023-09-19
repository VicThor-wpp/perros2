document.addEventListener("DOMContentLoaded", () => {
  const perro = JSON.parse(localStorage.getItem("selectedDogInfo"));

  if (perro) {
    const img = document.createElement("img");
    img.src = `static/perritos/${perro.imagen}`;
    img.alt = perro.nombre;

    const divinfo = document.createElement("div");
    const h1 = document.createElement("h1");
    h1.textContent = perro.nombre;

    const descripcion = document.createElement("p");
    descripcion.textContent = perro.descripcion;

    const tepareces = document.createElement("h2");
    tepareces.textContent = `¿Te parecés a ${perro.nombre}?`;

    const botonesver = document.createElement("div");
    botonesver.className = "botonesver";

    const botonadoptalo = document.createElement("a");
    botonadoptalo.href = "contacto";
    botonadoptalo.className = "button";
    botonadoptalo.textContent = "Adoptalo";

    // Add event listener to the link to save dog's name to local storage
    botonadoptalo.addEventListener("click", (e) => {
      localStorage.setItem("selectedDogName", perro.nombre);
    });

    // Aquí puedes seleccionar un contenedor existente en vermas.html y agregarle el contenido
    const container = document.querySelector(".dog-info-container");
    container.appendChild(img);
    container.appendChild(divinfo);
    divinfo.appendChild(h1);
    divinfo.appendChild(descripcion);
    divinfo.appendChild(tepareces);
    botonesver.appendChild(botonadoptalo);
    divinfo.appendChild(botonesver);
  } else {
    console.log("Error al cargar perro");
  }
});
