// ✅ ScrollReveal - Animaciones en Scroll
document.addEventListener("DOMContentLoaded", function () {
    ScrollReveal().reveal('.fade-in', {
        distance: '20px',
        duration: 800,
        easing: 'ease-in-out',
        origin: 'bottom',
        reset: false
    });

    // ✅ Mostrar y ocultar el botón "Volver arriba"
    let btnVolverArriba = document.getElementById("btnVolverArriba");
    window.addEventListener("scroll", function () {
        if (window.scrollY > 300) {
            btnVolverArriba.style.display = "block";
        } else {
            btnVolverArriba.style.display = "none";
        }
    });

    // ✅ Hacer scroll suave cuando se hace clic en el botón
    btnVolverArriba.addEventListener("click", function () {
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    });

    // ✅ Fade-in al cargar la página
    let fadeElements = document.querySelectorAll('.fade-in');
    fadeElements.forEach(element => {
        element.classList.add('show');
    });

    // ✅ Modo oscuro
    const darkModeToggle = document.getElementById("darkModeToggle");
    const body = document.body;

    if (localStorage.getItem("dark-mode") === "enabled") {
        body.classList.add("dark-mode");
        darkModeToggle.innerText = "☀ Modo Claro";
    }

    darkModeToggle.addEventListener("click", function () {
        body.classList.toggle("dark-mode");
        if (body.classList.contains("dark-mode")) {
            localStorage.setItem("dark-mode", "enabled");
            darkModeToggle.innerText = "☀ Modo Claro";
        } else {
            localStorage.setItem("dark-mode", "disabled");
            darkModeToggle.innerText = "🌙 Modo Oscuro";
        }
    });
});
