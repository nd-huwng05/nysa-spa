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

function showSingleSweetAlert(messageText, iconType, alertTitle) {
    if (messageText) {
        Swal.fire({
            icon: iconType || 'error',
            title: alertTitle || 'Thông báo',
            text: messageText,
        });
    }
}

document.body.addEventListener("show-flash-message", function(evt) {
    const data = evt.detail;
    Swal.fire({
        icon: data.type,
        title: 'Thông báo',
        text: data.message,
        showConfirmButton: true
    });
});