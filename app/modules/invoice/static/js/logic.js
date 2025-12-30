(function() {
    let paymentCheckInterval = null;

    function getInvoiceCode() {
        const invoiceEl = document.getElementById('bank-transfer-content') || document.querySelector('.font-monospace.fw-bold');
        if (invoiceEl) {
            const code = invoiceEl.textContent.trim();
            return (code && code !== "None" && code !== "") ? code : null;
        }
        return null;
    }

    function startPaymentPolling(invoiceCode) {
        if (!invoiceCode) return;
        if (paymentCheckInterval) clearInterval(paymentCheckInterval);

        paymentCheckInterval = setInterval(function() {
            fetch('/invoice/check-status/' + invoiceCode)
                .then(function(response) {
                    if (!response.ok) throw new Error();
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
                    console.error(error);
                });
        }, 3000);
    }

    function stopPolling() {
        if (paymentCheckInterval) {
            clearInterval(paymentCheckInterval);
            paymentCheckInterval = null;
        }
    }

    document.addEventListener('click', function(e) {
        const btn = e.target.closest('#complete-cash-btn');
        if (!btn) return;

        const invoiceCode = getInvoiceCode();
        if (!invoiceCode) return;

        const summaryAmountEl = document.getElementById('summary-payment-amount');
        const amount = summaryAmountEl ? summaryAmountEl.textContent : '0đ';

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
                btn.disabled = true;
                btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';

                fetch('/invoice/update-status/' + invoiceCode)
                    .then(function (response) {
                        if (!response.ok) throw new Error();
                        return response.json();
                    })
                    .then(function (data) {
                        if (typeof window.showSuccessModal === 'function') {
                            window.showSuccessModal();
                        }
                    })
                    .catch(function (error) {
                        btn.disabled = false;
                        btn.innerHTML = '<i class="bi bi-check-circle me-2"></i>Complete Transaction';
                        Swal.fire({ icon: 'error', title: 'Error', text: 'Could not update status.' });
                    });
            }
        });
    });

    document.body.addEventListener('htmx:afterSwap', function(evt) {
        const code = getInvoiceCode();
        if (code) startPaymentPolling(code);
    });

    window.addEventListener('stop-payment-polling', stopPolling);
    window.addEventListener('qr-expired', stopPolling);
})();