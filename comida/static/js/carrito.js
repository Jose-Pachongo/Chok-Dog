// document.addEventListener("DOMContentLoaded", function () {
//     document.querySelectorAll(".agregar-carrito").forEach(boton => {
//         boton.addEventListener("click", function () {
//             let productId = parseInt(this.getAttribute("data-id"));
//             let productName = this.getAttribute("data-nombre");
//             let productPrice = parseFloat(this.getAttribute("data-precio"));

//             agregarAlCarrito(productId, productName, productPrice);
//         });
//     });
// });

document.addEventListener("DOMContentLoaded", function() {
    renderCarrito();
    actualizarContadorCarrito();

    // Agregar evento a los botones de "Agregar al carrito"
    document.querySelectorAll(".agregar-carrito").forEach(function(boton) {
      boton.addEventListener("click", function() {
        const productId = parseInt(this.getAttribute("data-id"));
        const productName = this.getAttribute("data-nombre");
        const productPrice = parseFloat(this.getAttribute("data-precio"));
        agregarAlCarrito(productId, productName, productPrice);
      });
    });

    // Eventos para actualizar cantidad y eliminar productos en el carrito
    const carritoBody = document.getElementById("carrito-body");
    if (carritoBody) {
      carritoBody.addEventListener("change", function(e) {
        if (e.target.classList.contains("actualizar-cantidad")) {
          const nuevaCantidad = parseInt(e.target.value);
          const productId = parseInt(e.target.getAttribute("data-id"));
          actualizarCantidad(productId, nuevaCantidad);
        }
      });

      carritoBody.addEventListener("click", function(e) {
        if (e.target.classList.contains("eliminar-item")) {
          const productId = parseInt(e.target.getAttribute("data-id"));
          eliminarItem(productId);
        }
      });
    }
  });
  
  // Función para agregar un producto al carrito
  function agregarAlCarrito(productId, productName, productPrice) {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];

    let item = carrito.find(i => i.id === productId);
    if (item) {
        item.cantidad += 1;
    } else {
        carrito.push({ id: productId, nombre: productName, precio: productPrice, cantidad: 1 });
    }

    localStorage.setItem('carrito', JSON.stringify(carrito));
    actualizarContadorCarrito();
    alert("Producto agregado al carrito.");
}

  // Función para renderizar el carrito
  function renderCarrito() {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    let carritoBody = document.getElementById("carrito-body");

    if (!carritoBody) return;

    carritoBody.innerHTML = "";
    let total = 0;

    carrito.forEach(item => {
        let precioNumerico = parseFloat(item.precio);  // Asegurar que es número
        const subtotal = precioNumerico * item.cantidad;
        total += subtotal;

        let row = document.createElement("tr");
        row.innerHTML = `
            <td>${item.nombre}</td>
            <td>
                <input type="number" value="${item.cantidad}" min="1" data-id="${item.id}" class="actualizar-cantidad">
            </td>
            <td>$${precioNumerico.toFixed(2)}</td>
            <td>$${subtotal.toFixed(2)}</td>
            <td>
                <button data-id="${item.id}" class="eliminar-item">Eliminar</button>
            </td>
        `;
        carritoBody.appendChild(row);
    });

    document.getElementById("total").textContent = "Total: $" + total.toFixed(2);
}

  // Función para actualizar el contador del carrito en la cabecera
  function actualizarContadorCarrito() {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    const totalItems = carrito.reduce((sum, item) => sum + item.cantidad, 0);
    const contador = document.getElementById("cart-counter");
    if (contador) {
      contador.textContent = totalItems;
      contador.classList.toggle("hidden", totalItems === 0);
    }
  }

  // Función para actualizar la cantidad de un producto en el carrito
  function actualizarCantidad(productId, nuevaCantidad) {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    carrito = carrito.map(item => {
      if (item.id === productId) {
        item.cantidad = nuevaCantidad;
      }
      return item;
    });
    localStorage.setItem('carrito', JSON.stringify(carrito));
    renderCarrito();
    actualizarContadorCarrito();
  }

  // Función para eliminar un producto del carrito
  function eliminarItem(productId) {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    carrito = carrito.filter(item => item.id !== productId);
    localStorage.setItem('carrito', JSON.stringify(carrito));
    renderCarrito();
    actualizarContadorCarrito();
  }