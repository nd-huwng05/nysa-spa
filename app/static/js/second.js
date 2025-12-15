function showSingleSweetAlert(messageText, iconType, alertTitle) {
    if (messageText) {
        Swal.fire({
            icon: iconType || 'error', // Mặc định là 'error'
            title: alertTitle || 'Thông báo',
            text: messageText,
        });
    }
}