document.addEventListener("DOMContentLoaded", function() {
    renderCarrito();
    actualizarContadorCarrito();

    // const carritoIcono = document.getElementById("carrito-icon"); // Asegúrate de que el ícono tiene este ID
    // const carrito = JSON.parse(localStorage.getItem("carrito")) || [];

    // if (carrito.length === 0) {
    //     carritoIcono.style.display = "none"; // Oculta el ícono si el carrito está vacío
    // } else {
    //     carritoIcono.style.display = "block"; // Muestra el ícono si hay productos
    // }

    document.body.addEventListener("click", function(event) {
        const target = event.target;

        if (target.classList.contains("agregar-carrito")) {
            const productId = parseInt(target.getAttribute("data-id"));
            const productName = target.getAttribute("data-nombre");
            const productPrice = parseFloat(target.getAttribute("data-precio"));

            let ingredientesSeleccionados = [];
            document.querySelectorAll(`#modal${productId} input[type="checkbox"]:checked`).forEach(checkbox => {
                ingredientesSeleccionados.push(checkbox.value);
            });

            let selectSabor = document.querySelector(`.opcion-sabor[data-id="${productId}"]`);
            let saborSeleccionado = selectSabor && selectSabor.value ? selectSabor.value : null;

            if (selectSabor && !saborSeleccionado) {
                Swal.fire({
                    title: "Selecciona un sabor",
                    text: "Por favor, elige un sabor antes de agregar al carrito.",
                    icon: "warning",
                    showConfirmButton: true
                });
                return;
            }

            agregarAlCarrito(productId, productName, productPrice, ingredientesSeleccionados, saborSeleccionado);
        }

        if (target.classList.contains("agregar-carrito-bebida")) {
            const productId = parseInt(target.getAttribute("data-id"));
            const productName = target.getAttribute("data-nombre");
            let basePrice = parseFloat(target.getAttribute("data-precio"));

            let selectBebida = document.querySelector(`.opcion-bebida[data-id="${productId}"]`);
            let tipoBebida = selectBebida ? selectBebida.value : "soda";
            let extra = selectBebida ? parseFloat(selectBebida.selectedOptions[0].getAttribute("data-extra")) : 0;

            let finalPrice = basePrice + extra;

            agregarBebidaAlCarrito(productId, productName, finalPrice, tipoBebida);
        }

        if (target.closest(".eliminar-item")) {
            const productId = target.closest(".eliminar-item").getAttribute("data-id");
            eliminarItem(productId);
        }
    });

    document.body.addEventListener("change", function(event) {
        if (event.target.classList.contains("actualizar-cantidad")) {
            const productId = event.target.getAttribute("data-id");
            const nuevaCantidad = parseInt(event.target.value);
            actualizarCantidad(productId, nuevaCantidad);
        }
    });
});

function agregarAlCarrito(productId, productName, productPrice, ingredientes = [], sabor = null) {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    let uniqueId = `${productId}-${sabor ? sabor : "sinSabor"}-${ingredientes.length ? ingredientes.join(",") : "sinIngredientes"}`;
    
    // Buscar todos los ítems que coincidan con el mismo producto (pueden haber varios si ya se superó el límite antes)
    let items = carrito.filter(i => i.id === uniqueId || i.id.startsWith(`${uniqueId}-copia`));
    
    if (items.length > 0) {
        // Buscar el último ítem que no haya alcanzado el límite de 20
        let itemDisponible = items.find(i => i.cantidad < 20);
        
        if (itemDisponible) {
            // Si hay un ítem que no ha alcanzado el límite, incrementamos su cantidad
            itemDisponible.cantidad += 1;
        } else {
            // Si todos los ítems existentes están en el límite, creamos uno nuevo
            let copiaNum = items.length;
            let nuevoUniqueId = `${uniqueId}-copia${copiaNum}`;
            
            carrito.push({
                id: nuevoUniqueId,
                nombre: productName,
                precio: productPrice,
                cantidad: 1,
                ingredientes,
                sabor,
                esCopiaDe: uniqueId // Marcamos que es copia del producto original
            });
        }
    } else {
        // Si no existe el producto en el carrito, lo añadimos normalmente
        carrito.push({
            id: uniqueId,
            nombre: productName,
            precio: productPrice,
            cantidad: 1,
            ingredientes,
            sabor
        });
    }

    localStorage.setItem('carrito', JSON.stringify(carrito));
    renderCarrito();
    actualizarContadorCarrito();
    Swal.fire({ 
        title: "¡Producto agregado!", 
        text: `${productName}${sabor ? ` (${sabor})` : ""} ha sido añadido al carrito.`, 
        icon: "success", 
        showConfirmButton: false, 
        timer: 1000, 
        toast: true, 
        position: "top-end" 
    });
}

function agregarBebidaAlCarrito(productId, productName, productPrice, tipoBebida) {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    let uniqueId = `${productId}-${tipoBebida}`;
    let item = carrito.find(i => i.id === uniqueId);

    if (item) {
        item.cantidad += 1;
    } else {
        carrito.push({ id: uniqueId, nombre: `${productName} (${tipoBebida})`, precio: productPrice, cantidad: 1 });
    }

    localStorage.setItem('carrito', JSON.stringify(carrito));
    renderCarrito();
    actualizarContadorCarrito();
    Swal.fire({ title: "¡Bebida agregada!", text: `${productName} (${tipoBebida}) ha sido añadida al carrito.`, icon: "success", showConfirmButton: false, timer: 1000, toast: true, position: "top-end" });
}

function renderCarrito() {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    console.log("📌 Carrito en localStorage:", carrito); // ✅ Verifica si hay datos en localStorage

    let carritoBody = document.getElementById("carrito-body");

    if (!carritoBody) {
        console.error("⚠️ No se encontró el elemento con ID 'carrito-body'");
        return;
    }

    carritoBody.innerHTML = ""; // 🔹 Limpia la tabla antes de renderizar

    let total = 0;
    let esPaginaPago = window.location.pathname.includes("pago"); // 🔹 Detecta si estás en la página de pago

    carrito.forEach(item => {
        if (!item.id || !item.nombre || !item.precio) {
            console.warn("⚠️ Producto con datos faltantes:", item);
            return;
        }

        let precioNumerico = parseFloat(item.precio);
        let subtotal = precioNumerico * item.cantidad;
        total += subtotal;

        let ingredientesTexto = item.ingredientes && item.ingredientes.length > 0 ? `(${item.ingredientes.join(", ")})` : "";
        let saborTexto = item.sabor ? `(${item.sabor})` : "";

        let row = document.createElement("tr");
        row.innerHTML = `
            <td>${item.nombre} ${saborTexto} ${ingredientesTexto}</td>
            <td>
                ${esPaginaPago 
                    ? `<span>${item.cantidad}</span>`  // 🔹 En pago, solo se muestra la cantidad
                    : `<input type="number" value="${item.cantidad}" min="1" data-id="${item.id}" class="actualizar-cantidad" style="width: 50px; text-align: center;">`
                }
            </td>
            <td>$${precioNumerico.toLocaleString("es-CO")}</td>
            <td>$${subtotal.toLocaleString("es-CO")}</td>
            ${!esPaginaPago ? `
            
                <td>
                    <button data-id="${item.id}" class="eliminar-item">
                        <i class='bx bxs-trash'></i>
                    </button>
                </td>
            ` : ""}
        `;
        carritoBody.appendChild(row);
    });

    document.getElementById("total").textContent = "Total: $" + total.toLocaleString("es-CO");

    console.log("✅ Carrito renderizado correctamente:", carrito);
}



function actualizarContadorCarrito() {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    let totalItems = carrito.reduce((sum, item) => sum + item.cantidad, 0);
    let contador = document.getElementById("cart-counter");
    if (contador) contador.textContent = totalItems;
}

function actualizarCantidad(productId, nuevaCantidad) {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    let itemOriginal = carrito.find(item => item.id === productId);
    
    // Si la nueva cantidad es menor o igual a 20, simplemente actualizamos
    if (nuevaCantidad <= 20) {
        carrito = carrito.map(item => {
            if (item.id === productId) {
                return { ...item, cantidad: nuevaCantidad };
            }
            return item;
        });
    } else {
        // Si es mayor a 20, necesitamos manejar la división en múltiples ítems
        
        // Primero establecemos el ítem actual en 20
        carrito = carrito.map(item => {
            if (item.id === productId) {
                return { ...item, cantidad: 20 };
            }
            return item;
        });
        
        // Calculamos cuántas unidades quedan por distribuir
        let cantidadRestante = nuevaCantidad - 20;
        
        // Buscamos si hay copias existentes de este producto
        let baseId = productId;
        if (itemOriginal.esCopiaDe) {
            // Si el ítem ya es una copia, usamos el ID original
            baseId = itemOriginal.esCopiaDe;
        }
        
        let todasLasCopias = carrito.filter(i => 
            i.id.startsWith(`${baseId}-copia`) || 
            i.id === baseId
        ).sort((a, b) => {
            // Ordenamos para procesar las copias en orden
            if (a.id === baseId) return -1;
            if (b.id === baseId) return 1;
            return a.id.localeCompare(b.id);
        });
        
        // Intentamos distribuir la cantidad restante en las copias existentes
        for (let i = 0; i < todasLasCopias.length && cantidadRestante > 0; i++) {
            let copia = todasLasCopias[i];
            if (copia.id !== productId && copia.cantidad < 20) {
                let espacioDisponible = 20 - copia.cantidad;
                let cantidadAAgregar = Math.min(espacioDisponible, cantidadRestante);
                
                carrito = carrito.map(item => {
                    if (item.id === copia.id) {
                        return { ...item, cantidad: item.cantidad + cantidadAAgregar };
                    }
                    return item;
                });
                
                cantidadRestante -= cantidadAAgregar;
            }
        }
        
        // Si aún queda cantidad por distribuir, creamos nuevos ítems
        while (cantidadRestante > 0) {
            let copiaNum = todasLasCopias.length;
            let nuevoUniqueId = `${baseId}-copia${copiaNum}`;
            
            let cantidadItem = Math.min(cantidadRestante, 20);
            
            // Creamos una copia del ítem original con la nueva cantidad
            carrito.push({
                ...itemOriginal,
                id: nuevoUniqueId,
                cantidad: cantidadItem,
                esCopiaDe: baseId
            });
            
            cantidadRestante -= cantidadItem;
            todasLasCopias.length++; // Incrementamos para el siguiente ID
        }
    }

    localStorage.setItem('carrito', JSON.stringify(carrito));
    renderCarrito();
    actualizarContadorCarrito();
}




function eliminarItem(productId) {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    carrito = carrito.filter(item => item.id !== productId);
    localStorage.setItem('carrito', JSON.stringify(carrito));
    renderCarrito();
    actualizarContadorCarrito();
}



// vista previa

document.body.addEventListener("click", function(event) {
    const target = event.target;

    if (target.classList.contains("agregar-carrito-personalizado")) {
        const productId = parseInt(target.getAttribute("data-id"));
        const productName = target.getAttribute("data-nombre");
        
        // Seleccionar categoría
        let selectCategoria = document.querySelector(`.opcion-categoria[data-id="${productId}"]`);
        let categoriaSeleccionada = selectCategoria ? selectCategoria.value : "Normal";
        
        // Asignar precios basados en la categoría
        let finalPrice;
        switch (categoriaSeleccionada) {
            case "Normal":
                finalPrice = 12000;
                break;
            case "Especial":
                finalPrice = 15000;
                break;
            case "Clásica":
                finalPrice = 20000;
                break;
            case "Hamburguesa":
                finalPrice = 5000;
                break;
            default:
                finalPrice = 0; // Valor predeterminado en caso de error
        }

        console.log("Categoría seleccionada:", categoriaSeleccionada);
        console.log("Precio final:", finalPrice);

        // Generar un ID único basado en producto y categoría
        let uniqueId = `${productId}-${categoriaSeleccionada}`;

        // Agregar al carrito
        agregarAlCarrito(uniqueId, `${productName} (${categoriaSeleccionada})`, finalPrice);
    }
});



document.getElementById("btnPagar").addEventListener("click", function () {
    let carrito = JSON.parse(localStorage.getItem("carrito")) || [];

    if (carrito.length === 0) {
        Swal.fire({
            title: "Carrito vacío",
            text: "No tienes productos en el carrito.",
            icon: "warning",
            confirmButtonColor: "#D4AF37",
        });
        return;
    }

    fetch("/procesar-pago/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({ productos: carrito }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "ok") {
            localStorage.setItem("order_id", data.order_id); // Guardar ID del pedido
            window.location.href = data.url_pago; // Redirige al pago (QR o pasarela)
        } else {
            Swal.fire({
                title: "Error",
                text: "Hubo un problema al procesar el pago.",
                icon: "error",
                confirmButtonColor: "#D4AF37",
            });
        }
    });
});

