// document.addEventListener("DOMContentLoaded", function () {
//     let metodoPagoRadios = document.querySelectorAll("input[name='metodo_pago']");
//     let pagoInfo = document.getElementById("pago-info");
//     let qrImage = document.getElementById("qr-image");
//     let numeroPago = document.getElementById("numero-pago");

//     metodoPagoRadios.forEach(radio => {
//         radio.addEventListener("change", function () {
//             mostrarPago(this.value.toLowerCase());  // Asegúrate que coincida con el valor en minúscula
//         });
//     });

//     function mostrarPago(metodo) {
//         pagoInfo.style.display = "none";  // Ocultar primero por seguridad

//         if (metodo === "nequi") {
//             qrImage.src = "/static/images/qr.jpg";
//             numeroPago.innerHTML = "Número de Nequi: 3143477416";
//         } else if (metodo === "bancolombia") {
//             qrImage.src = "/static/images/qr.jpg";
//             numeroPago.innerHTML = "Número de Bancolombia: 3143477416";
//         } else {
//             return;
//         }

//         pagoInfo.style.display = "block";  // Mostrar el contenedor solo si hay coincidencia
//     }
// });


