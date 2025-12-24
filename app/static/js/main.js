function addServiceToCart(serviceId, callback) {
    fetch(`/cart/add/${serviceId}`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'}
    })
        .then(response => callback(response.ok))
        .catch(error => {
            console.error('Error adding item:', error);
            callback(false);
        });
}

function removeItemFromCart(serviceId, callback) {
    fetch(`/cart/remove/${serviceId}`, {
        method: "POST",
        headers: {'Content-Type': 'application/json'}
    })
        .then(response => callback(response.ok))
        .catch(error => {
            console.error('Error removing item:', error);
            callback(false);
        });
}