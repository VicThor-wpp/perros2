document.addEventListener('DOMContentLoaded', function() {
    const formulario = document.getElementById('formulario');
    const perros = [];

    formulario.addEventListener('submit', function(e) {
        e.preventDefault();

        const nombre = document.getElementById('nombre').value;
        const descripcion = document.getElementById('descripcion').value;
        const imagen = document.getElementById('imagen').value;

        const perro = {
            nombre,
            descripcion,
            imagen
        };

        perros.push(perro);

        console.log(perros);

        // Limpia el formulario después de agregar el perro
        formulario.reset();
    });
});
