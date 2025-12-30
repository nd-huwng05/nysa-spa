(function() {
    let paymentCheckInterval = null;

    function startPaymentPolling(invoiceCode) {
        if (paymentCheckInterval) clearInterval(paymentCheckInterval);

        paymentCheckInterval = setInterval(function() {
            fetch('/invoice/check-status/' + invoiceCode)
                .then(function(response) {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(function(result) {
                    if (result.data && result.data.status === 'PAID') {
                        stopPolling();
                        if (typeof window.showSuccessModal === 'function') {
                            window.showSuccessModal();
                        }
                    }
                })
                .catch(function(error) {
                    console.error("Polling error:", error);
                });
        }, 3000);
    }

    function stopPolling() {
        if (paymentCheckInterval) {
            clearInterval(paymentCheckInterval);
            paymentCheckInterval = null;
        }
    }

    document.body.addEventListener('htmx:afterSwap', function(evt) {
        const invoiceEl = document.getElementById('bank-transfer-content');
        if (invoiceEl) {
            const code = invoiceEl.textContent.trim();
            if (code) {
                startPaymentPolling(code);
            }
        }
    });

    window.addEventListener('stop-payment-polling', stopPolling);
    window.addEventListener('qr-expired', stopPolling);
})();

if (completeCashBtn) {
    completeCashBtn.addEventListener('click', function () {
        var invoiceIdEl = document.querySelector('.font-monospace.fw-bold');
        var invoiceCode = invoiceIdEl ? invoiceIdEl.textContent.trim() : '';
        var amount = summaryAmount.textContent;

        Swal.fire({
            title: 'Confirm Payment',
            text: 'Have you received ' + amount + ' in cash?',
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#28a745',
            cancelButtonColor: '#6c757d',
            confirmButtonText: 'Yes, Received!'
        }).then(function (resultSwal) {
            if (resultSwal.isConfirmed) {
                completeCashBtn.disabled = true;
                completeCashBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';

                fetch('/invoice/update-status/' + invoiceCode)
                    .then(function (response) {
                        if (!response.ok) {
                            throw new Error('Update failed');
                        }
                        return response.json();
                    })
                    .then(function (data) {
                        if (typeof window.showSuccessModal === 'function') {
                            window.showSuccessModal();
                        }
                    })
                    .catch(function (error) {
                        console.error('Error:', error);
                        completeCashBtn.disabled = false;
                        completeCashBtn.innerHTML = '<i class="bi bi-check-circle me-2"></i>Complete Transaction';

                        Swal.fire({
                            icon: 'error',
                            title: 'Error',
                            text: 'Could not update payment status.'
                        });
                    });
            }
        });
    });
}