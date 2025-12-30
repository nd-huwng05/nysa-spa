document.addEventListener('DOMContentLoaded', function () {
    const holdCountdownEl = document.getElementById('hold-countdown');
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
    const header = document.getElementById('header');

    let qrInterval;
    let holdInterval;

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

        const dateString = expiryTime.replace(/-/g, "/");
        const expiryDate = new Date(dateString).getTime();

        const updateTimer = () => {
            const now = new Date().getTime();
            const diff = expiryDate - now;

            if (isNaN(diff) || diff <= 0) {
                element.textContent = "00:00";
                if (type === 'QR') {
                    if (qrDisplay) qrDisplay.style.filter = "grayscale(1) opacity(0.3)";
                    if (refreshBtn) refreshBtn.style.display = "block";
                    clearInterval(qrInterval);
                    window.dispatchEvent(new CustomEvent('qr-expired'));
                } else {
                    element.style.opacity = "0.5";
                    confirmBtn.disabled = true;
                    confirmBtn.textContent = "EXPIRED";
                    clearInterval(holdInterval);
                }
                return;
            }

            element.textContent = formatTime(diff);
        };

        const interval = setInterval(updateTimer, 1000);
        updateTimer();

        if (type === 'QR') qrInterval = interval;
        else holdInterval = interval;
    }

    document.body.addEventListener('htmx:afterSwap', function (evt) {
        const qrCountdown = document.getElementById('expiry-time-display');
        if (qrCountdown) {
            const rawExpiry = qrCountdown.getAttribute('data-expiry');
            if (rawExpiry) {
                startTimer(qrCountdown, rawExpiry, 'QR');
            }
        }
    });

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
            window.dispatchEvent(new CustomEvent('stop-payment-polling'));

            if (header) header.style.setProperty('display', 'flex', 'important');

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

    confirmBtn.addEventListener('click', function (e) {
        const selectedAmount = summaryAmount.textContent;
        const methodChecked = document.querySelector('input[name="payment_method"]:checked').value;

        paymentSelection.style.transition = "opacity 0.3s, transform 0.3s";
        paymentSelection.style.opacity = "0";
        paymentSelection.style.transform = "translateY(-10px)";

        setTimeout(() => {
            paymentSelection.style.display = 'none';
            step2.style.display = 'block';
            step2.style.opacity = '1';

            const currentQrContainer = document.getElementById('qr-method-container');
            const currentCashContainer = document.getElementById('cash-method-container');

            if (methodChecked === 'CASH') {
                if (header) header.style.setProperty('display', 'none', 'important');
                if (currentQrContainer) currentQrContainer.style.setProperty('display', 'none', 'important');
                if (currentCashContainer) {
                    currentCashContainer.style.setProperty('display', 'block', 'important');
                    if (cashAmountCollect) cashAmountCollect.textContent = selectedAmount;
                }
            } else {
                if (header) header.style.setProperty('display', 'flex', 'important');
                if (currentCashContainer) currentCashContainer.style.setProperty('display', 'none', 'important');
                if (currentQrContainer) {
                    currentQrContainer.style.setProperty('display', 'block', 'important');

                    const qrCountdown = document.getElementById('expiry-time-display');
                    if (qrCountdown) {
                        const rawExpiry = qrCountdown.getAttribute('data-expiry');
                        if (rawExpiry) startTimer(qrCountdown, rawExpiry, 'QR');
                    }
                }
            }

            setTimeout(() => {
                step2.style.transition = "opacity 0.4s ease";
                step2.style.opacity = "1";
            }, 50);
        }, 300);
    });

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
            }).then((resultSwal) => {
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

    window.showSuccessModal = showSuccessModal;
    init();
})