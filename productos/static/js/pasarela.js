document.addEventListener("DOMContentLoaded", function () {
    // Seleccionamos todos los botones de método de pago
    let metodoPagoRadio = document.querySelectorAll("input[name='metodo_pago']");
    let pagoInfo = document.getElementById("pago-info");
    let qrImage = document.getElementById("qr-image");
    let numeroPago = document.getElementById("numero-pago");

    metodoPagoRadio.forEach(radio => {
        radio.addEventListener("change", function () {
            mostrarPago(this.value);
        });
    });

    function mostrarPago(metodo) {
        if (metodo === "Nequi") {
            qrImage.src = "/static/images/qr.jpg";  // Ruta de la imagen en STATIC
            numeroPago.innerHTML = "Número de Nequi: 3143477416";
        } else if (metodo === "Bancolombia") {
            qrImage.src = "../static/images/qr.jpg";
            numeroPago.innerHTML = "Número de Bancolombia: 3143477416";
        } else {
            pagoInfo.style.display = "none";
            return;
        }

        pagoInfo.style.display = "block";
    }
});