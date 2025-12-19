document.addEventListener('DOMContentLoaded', function () {
    const holdCountdownEl = document.getElementById('hold-countdown');
    const qrCountdownEl = document.getElementById('expiry-time-display');
    const confirmBtn = document.getElementById('confirm-payment-btn');
    const backBtn = document.getElementById('back-to-step1');
    const paymentSelection = document.getElementById('payment-selection-section');
    const step2 = document.getElementById('step-scan-qr');
    const cashAmountCollect = document.getElementById('cash-amount-collect');
    const completeCashBtn = document.getElementById('complete-cash-btn');
    const qrDisplay = document.getElementById('qr-code-display');
    const refreshBtn = document.getElementById('refresh-qr-btn');
    const summaryMethod = document.getElementById('summary-method');
    const summaryAmount = document.getElementById('summary-payment-amount');
    const amountFull = document.getElementById('full-amount-display').textContent.trim();
    const amountDeposit = document.getElementById('deposit-amount-display').textContent.trim();

    const qrMethodContainer = document.getElementById('qr-method-container') || document.getElementById('qr-placeholder-section');
    const cashMethodContainer = document.getElementById('cash-method-container') || document.getElementById('step-confirm');

    let qrInterval;
    let holdInterval;
    let paymentCheckInterval;

    async function createInvoice(method) {
        const amountRaw = summaryAmount.textContent.replace(/[^0-9]/g, '');
        const paymentType = document.querySelector('input[name="payment_type"]:checked').value;
        const bookingId = document.getElementById('booking-id') ? document.getElementById('booking-id').value : null;
        const invoice_code = document.getElementById('invoice-code') ? document.getElementById('invoice-code').dataset.id : null;

        const data = {
            invoice_code: invoice_code,
            booking_id: bookingId,
            amount: amountRaw,
            payment_method: method,
            type: 'PAYMENT',
            payment_type: `${paymentType}`
        };

        try {
            Swal.showLoading();
            const response = await fetch('/invoice/update', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });

            const result = await response.json();
            if (response.ok) {
                Swal.fire({
                    icon: 'success',
                    title: 'Create Invoice Successful!',
                    text: 'Code: ' + result.data.invoice_code,
                    timer: 2000,
                    showConfirmButton: false
                });
                return result;
            } else {
                Swal.fire("Error", result.message || "Failed to create invoice", "error");
                return null;
            }
        } catch (error) {
            Swal.fire('Error', 'Could not create invoice. Please try again.', 'error');
            return null;
        }
    }

    function startPaymentPolling(invoiceCode) {
        if (paymentCheckInterval) clearInterval(paymentCheckInterval);

        paymentCheckInterval = setInterval(async () => {
            try {
                const response = await fetch(`/invoice/check-status/${invoiceCode}`);
                const result = await response.json();
                if (result.data.status === 'PAID') {
                    clearInterval(paymentCheckInterval);
                    showSuccessModal();
                }
            } catch (error) {

            }
        }, 3000);
    }

    function formatTime(ms) {
        if (ms <= 0) return "00:00";
        const totalSeconds = Math.floor(ms / 1000);
        const m = Math.floor(totalSeconds / 60).toString().padStart(2, '0');
        const s = (totalSeconds % 60).toString().padStart(2, '0');
        return `${m}:${s}`;
    }

    function startTimer(element, expiryTime, type) {
        if (!element || !expiryTime) return;
        if (type === 'QR' && qrInterval) clearInterval(qrInterval);
        if (type === 'HOLD' && holdInterval) clearInterval(holdInterval);

        const expiryDate = new Date(expiryTime.replace(/-/g, "/")).getTime();

        const interval = setInterval(() => {
            const now = new Date().getTime();
            const diff = expiryDate - now;

            element.textContent = formatTime(diff);

            if (diff <= 0) {
                clearInterval(interval);
                if (type === 'QR') {
                    element.textContent = "EXPIRED";
                    if (qrDisplay) qrDisplay.style.filter = "grayscale(1) opacity(0.3)";
                    if (refreshBtn) refreshBtn.style.display = "block";
                    if (paymentCheckInterval) {
                        clearInterval(paymentCheckInterval);
                    }
                } else {
                    element.style.opacity = "0.5";
                    confirmBtn.disabled = true;
                    confirmBtn.textContent = "EXPIRED";
                }
            }
        }, 1000);

        if (type === 'QR') qrInterval = interval;
        else holdInterval = interval;
    }

    function init() {
        if (step2) {
            step2.style.display = 'none';
            step2.style.opacity = '0';
        }
        const holdExpiry = holdCountdownEl ? holdCountdownEl.getAttribute('data-expiry') : null;
        if (holdExpiry) startTimer(holdCountdownEl, holdExpiry, 'HOLD');
    }

    if (backBtn) {
        backBtn.addEventListener('click', function () {
            if (qrInterval) clearInterval(qrInterval);
            if (paymentCheckInterval) clearInterval(paymentCheckInterval);
            step2.style.opacity = "0";
            setTimeout(() => {
                step2.style.display = 'none';
                paymentSelection.style.display = 'block';
                setTimeout(() => {
                    paymentSelection.style.opacity = "1";
                    paymentSelection.style.transform = "translateY(0)";
                }, 50);
            }, 300);
        });
    }

    document.querySelectorAll('input[name="payment_type"]').forEach(radio => {
        radio.addEventListener('change', function () {
            const isFull = this.value === 'FULL';
            const selectedAmount = isFull ? amountFull : amountDeposit;
            const methodChecked = document.querySelector('input[name="payment_method"]:checked');
            const methodText = methodChecked && methodChecked.value === 'CASH' ? 'Cash' : 'Bank Transfer';
            confirmBtn.textContent = `PAY NOW (${selectedAmount})`;
            summaryMethod.textContent = `${methodText} (${isFull ? 'Full' : 'Deposit'})`;
            summaryAmount.textContent = selectedAmount;
        });
    });

    confirmBtn.addEventListener('click', async function () {
        const selectedAmount = summaryAmount.textContent;
        const methodChecked = document.querySelector('input[name="payment_method"]:checked').value;

        confirmBtn.disabled = true;
        confirmBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';

        const result = await createInvoice(methodChecked);

        if (result && result.data) {
            paymentSelection.style.transition = "opacity 0.3s, transform 0.3s";
            paymentSelection.style.opacity = "0";
            paymentSelection.style.transform = "translateY(-10px)";

            setTimeout(() => {
                paymentSelection.style.display = 'none';
                step2.style.display = 'block';

                if (methodChecked === 'CASH') {
                    if (qrMethodContainer) qrMethodContainer.style.display = 'none';
                    if (cashMethodContainer) cashMethodContainer.style.display = 'block';
                    if (cashAmountCollect) cashAmountCollect.textContent = selectedAmount;
                } else {
                    if (cashMethodContainer) cashMethodContainer.style.display = 'none';
                    if (qrMethodContainer) qrMethodContainer.style.display = 'block';

                    if (qrDisplay && result.data.qr_link) {
                        qrDisplay.innerHTML = `<img src="${result.data.qr_link}" class="img-fluid" style="max-width:250px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);" alt="Payment QR">`;
                    }

                    const expiryDisplay = document.getElementById('expiry-time-display');
                    const rawExpiry = result.data.expires_at;

                    if (expiryDisplay && rawExpiry) {
                        startTimer(expiryDisplay, rawExpiry, 'QR');
                    }

                    startPaymentPolling(result.data.invoice_code);
                }

                setTimeout(() => {
                    step2.style.transition = "opacity 0.4s ease";
                    step2.style.opacity = "1";
                    confirmBtn.disabled = false;
                    confirmBtn.textContent = `PAY NOW (${selectedAmount})`;
                }, 50);
            }, 300);
        } else {
            confirmBtn.disabled = false;
            confirmBtn.textContent = `PAY NOW (${selectedAmount})`;
        }
    });

    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            window.location.reload();
        });
    }

    if (completeCashBtn) {
        completeCashBtn.addEventListener('click', function () {
            Swal.fire({
                title: 'Confirm Payment',
                text: `Have you received ${summaryAmount.textContent} in cash?`,
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#28a745',
                cancelButtonColor: '#6c757d',
                confirmButtonText: 'Yes, Received!'
            }).then(async (resultSwal) => {
                if (resultSwal.isConfirmed) {
                    completeCashBtn.disabled = true;
                    completeCashBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
                    setTimeout(() => {
                        showSuccessModal();
                    }, 500);
                }
            });
        });
    }

    function showSuccessModal() {
        const modalEl = document.getElementById('successModal');
        if (modalEl) {
            const successModal = new bootstrap.Modal(modalEl);
            successModal.show();
            let timeLeft = 5;
            const delayDisplay = document.getElementById('delay-time');
            const timer = setInterval(() => {
                timeLeft--;
                if (delayDisplay) delayDisplay.textContent = timeLeft;
                if (timeLeft <= 0) {
                    clearInterval(timer);
                    window.location.href = "/";
                }
            }, 1000);
        } else {
            window.location.href = "/";
        }
    }

    init();
});