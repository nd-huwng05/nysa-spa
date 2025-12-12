document.addEventListener('DOMContentLoaded', function () {
    // CONSTANTS
    const totalActualAmount = 2750000;
    const depositAmount = 550000;
    const invoiceCode = 'INV-20251212-001';
    let currentPaymentAmount = totalActualAmount;
    let isHolding = true;

    // DOM ELEMENTS
    const confirmBtn = document.getElementById('confirm-payment-btn');
    const paymentSelectionSection = document.getElementById('payment-selection-section');
    const qrPlaceholderSection = document.getElementById('step-scan-qr');
    const qrCodeDisplay = document.getElementById('qr-code-display');
    const summaryPaymentAmount = document.getElementById('summary-payment-amount');
    const summaryMethod = document.getElementById('summary-method');
    const fullAmountDisplay = document.getElementById('full-amount-display');
    const depositAmountDisplay = document.getElementById('deposit-amount-display');

    // --- INITIAL VALUE UPDATES ---
    const formatCurrency = (amount) => amount.toLocaleString('vi-VN', {minimumFractionDigits: 0});

    // Function to update payment summary based on radio selection
    const updatePaymentSummary = (isDeposit) => {
        currentPaymentAmount = isDeposit ? depositAmount : totalActualAmount;
        summaryPaymentAmount.textContent = `${formatCurrency(currentPaymentAmount)} VND`;
        confirmBtn.textContent = `PAY NOW (${formatCurrency(currentPaymentAmount)} VND)`;

        const typeText = isDeposit ? 'Deposit 20%' : 'Full';
        const methodText = document.querySelector('input[name="payment_method"]:checked').value === 'BANK_TRANSFER' ? 'Bank Transfer' : 'Cash';
        summaryMethod.textContent = `${methodText} (${typeText})`;
    };

    // Event Listeners for Radio Buttons
    document.querySelectorAll('input[name="payment_type"]').forEach(radio => {
        radio.addEventListener('change', (e) => updatePaymentSummary(e.target.value === 'DEPOSIT'));
    });
    document.querySelectorAll('input[name="payment_method"]').forEach(radio => {
        radio.addEventListener('change', () => {
            const isDeposit = document.querySelector('input[name="payment_type"]:checked').value === 'DEPOSIT';
            updatePaymentSummary(isDeposit);
        });
    });

    // --- PAYMENT BUTTON HANDLER ---
    confirmBtn.addEventListener('click', function () {
        if (!isHolding) return alert("Holding time expired!");

        // 1. Hide selection section
        paymentSelectionSection.style.display = 'none';

        // 2. Hide right-side hold timer
        document.getElementById('hold-timer-box').style.display = 'none';

        // 3. Show QR section
        qrPlaceholderSection.style.display = 'block';
        qrPlaceholderSection.scrollIntoView({behavior: 'smooth'});

        // 4. Generate QR Code
        const uniqueSuffix = currentPaymentAmount.toString().slice(0, 4);
        const content = `${invoiceCode}-${uniqueSuffix}`;
        document.getElementById('bank-transfer-content').textContent = content;

        qrCodeDisplay.innerHTML = '';
        new QRCode(qrCodeDisplay, {
            text: content,
            width: 220,
            height: 220,
            colorDark: "#2E2623",
            colorLight: "#ffffff"
        });

        // 5. Start QR Timer
        startQrTimer();
    });

    // --- COUNTDOWN LOGIC ---
    function startQrTimer() {
        let timer = 15 * 60; // 15 minutes
        const display = document.getElementById('countdown');
        const interval = setInterval(() => {
            let m = parseInt(timer / 60, 10);
            let s = parseInt(timer % 60, 10);
            display.textContent = (m < 10 ? "0" + m : m) + ":" + (s < 10 ? "0" + s : s);
            if (--timer < 0) clearInterval(interval);
        }, 1000);

        // Simulate success after 5s
        // setTimeout(() => {
        //     const modal = new bootstrap.Modal(document.getElementById('successModal'));
        //     modal.show();
        //     setTimeout(() => window.location.href = '/service/search-view', 3000);
        // }, 5000);
    }

    // Holding Timer (Simulated immediately)
    let holdTimer = 600;
    setInterval(() => {
        if (--holdTimer < 0) isHolding = false;
        let m = parseInt(holdTimer / 60, 10);
        let s = parseInt(holdTimer % 60, 10);
        document.getElementById('hold-countdown').textContent = (m < 10 ? "0" + m : m) + ":" + (s < 10 ? "0" + s : s);
    }, 1000);
});