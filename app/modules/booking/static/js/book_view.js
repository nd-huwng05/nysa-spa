let selectedVoucher = null;
let currentTotalServicePrice = 0;

function toggleEditInfo(btn) {
    const inputs = document.querySelectorAll('#step-3 input, #step-3 select, #step-3 textarea');
    const isCurrentlyReadonly = document.getElementById('custName').hasAttribute('readonly');

    inputs.forEach(input => {
        if(input.id === 'custEmail') return;

        if(isCurrentlyReadonly) {
            input.removeAttribute('readonly');
            input.removeAttribute('disabled');
        } else {
            input.setAttribute('readonly', true);
            if(input.tagName === 'SELECT') input.setAttribute('disabled', true);
        }
    });

    if(isCurrentlyReadonly) {
        btn.innerHTML = '<i class="fas fa-save me-1"></i> Save';
        btn.classList.remove('btn-outline-primary');
        btn.classList.add('btn-primary');
    } else {
        btn.innerHTML = '<i class="fas fa-pen me-1"></i> Update';
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-outline-primary');
    }
}

function updateComboMaster(comboId, staffId) {
    const comboBox = document.querySelector(`.combo-box[data-id="${comboId}"]`);
    const childSelects = comboBox.querySelectorAll('.child-select');

    if (staffId !== 'split') {
        childSelects.forEach(select => {
            select.value = staffId;
            select.setAttribute('disabled', true);
            const serviceId = select.id.split('-')[2];
            updateAllocation(serviceId);
        });
    } else {
        childSelects.forEach(select => {
            select.removeAttribute('disabled');
        });
    }
}

function updateAllocation(serviceId) {
    const selectBox = document.getElementById(`staff-select-${serviceId}`);
    if(!selectBox) return;

    const staffName = selectBox.options[selectBox.selectedIndex].text;
    const summaryLabel = document.getElementById(`sum-staff-${serviceId}`);
    if(summaryLabel) {
        summaryLabel.innerText = staffName;
    }
    updateSummaryTotal();
}

function formatTime(d) {
    return d.toTimeString().substring(0, 5);
}

function formatCurrency(amount) {
    if (typeof amount !== 'number') return '0đ';
    return amount.toLocaleString('vi-VN') + 'đ';
}

function calculateDiscount(voucher, total) {
    if (!voucher || total < voucher.min_order_value) return 0;

    let discount = 0;
    const value = parseFloat(voucher.discount_value);
    const max = parseFloat(voucher.max_discount_amount);

    if (voucher.discount_type === 'percent') {
        discount = total * (value / 100);
    } else if (voucher.discount_type === 'fixed') {
        discount = value;
    }

    if (max && discount > max) {
        discount = max;
    }

    return Math.round(discount);
}

function removeVoucher() {
    selectedVoucher = null;

    document.querySelectorAll('.apply-voucher-btn').forEach(b => {
        b.innerHTML = 'Apply';
        b.classList.remove('btn-success');
        b.classList.add('btn-outline-success');
    });

    updateSummaryTotal();
}

function applyManualVoucher(btn) {
    const inputContainer = document.getElementById('voucherCodeInput');
    inputContainer.classList.toggle('d-none');

    const isHidden = inputContainer.classList.contains('d-none');
    btn.innerHTML = isHidden
        ? '<i class="fas fa-ticket-alt me-1"></i> Enter Code'
        : '<i class="fas fa-list-ul me-1"></i> Hide Input';

    btn.classList.toggle('btn-outline-secondary');
    btn.classList.toggle('btn-secondary');
}

function applyVoucherCode() {
    const code = document.getElementById('inputVoucherCode').value.toUpperCase();
    if (!code) return;

    document.getElementById('inputVoucherCode').value = '';
}

function selectVoucher(btn, code) {
    const itemElement = btn.closest('.voucher-item');

    document.querySelectorAll('.apply-voucher-btn').forEach(b => {
        b.innerHTML = 'Apply';
        b.classList.remove('btn-success');
        b.classList.add('btn-outline-success');
    });

    if (selectedVoucher && selectedVoucher.code === code) {
        removeVoucher();
        return;
    }

    btn.innerHTML = '<i class="fas fa-check me-1"></i> Applied';
    btn.classList.remove('btn-outline-success');
    btn.classList.add('btn-success');

    selectedVoucher = {
        code: code,
        discount_type: itemElement.getAttribute('data-type'),
        discount_value: parseFloat(itemElement.getAttribute('data-value')),
        max_discount_amount: parseFloat(itemElement.getAttribute('data-max-amount')) || null,
        min_order_value: parseFloat(itemElement.getAttribute('data-min-order')),
    };

    updateSummaryTotal();
}

function updateSummaryTotal() {
    let total = 0;
    document.querySelectorAll('.service-item').forEach(item => {
        total += parseInt(item.getAttribute('data-price') || 0);
    });
    currentTotalServicePrice = total;

    let discountAmount = 0;

    if (selectedVoucher) {
        discountAmount = calculateDiscount(selectedVoucher, total);
    }

    const finalTotal = total - discountAmount;

    document.getElementById('sumSubTotal').innerText = formatCurrency(currentTotalServicePrice);
    const discountRow = document.getElementById('discount-display-row');
    const appliedCode = document.getElementById('appliedVoucherCode');
    const amountDisplay = document.getElementById('discountAmount');

    if (discountAmount > 0) {
        discountRow.style.display = 'flex';
        appliedCode.innerText = selectedVoucher.code;
        // ĐIỀU CHỈNH CHUỖI HIỂN THỊ: Loại bỏ dấu trừ (-)
        amountDisplay.innerText = `${formatCurrency(discountAmount)}`;
    } else {
        discountRow.style.display = 'none';

        if (selectedVoucher && selectedVoucher.min_order_value > currentTotalServicePrice) {
             Swal.fire({
                icon: 'warning',
                title: 'Voucher Not Applied',
                text: `Code ${selectedVoucher.code} requires a minimum order value of ${formatCurrency(selectedVoucher.min_order_value)}. Please select more services.`
            });
             selectedVoucher = null;
        }
    }

    document.getElementById('sumTotal').innerText = formatCurrency(finalTotal);
    document.getElementById('btnSubmit').disabled = (finalTotal <= 0 || total === 0);
}

function checkStep1() {
    const date = document.getElementById('inputDate').value;
    const time = document.getElementById('inputTime').value;
    const estimateBox = document.getElementById('timeEstimate');
    const timePlaceholder = document.getElementById('time-placeholder');
    const timelineNodes = document.querySelectorAll('.timeline-node');

    if(date && time) {
        document.getElementById('step-2').classList.remove('disabled');
        document.getElementById('step-3').classList.remove('disabled');
        document.getElementById('step-4').classList.remove('disabled');
        document.getElementById('btnSubmit').disabled = false;
        if(timePlaceholder) timePlaceholder.classList.add('d-none');
        timelineNodes.forEach(node => node.classList.remove('d-none'));

        let currentMockTime = new Date(`2000-01-01T${time}:00`);
        let totalMinutes = 0;
        let runningTotalServicePrice = 0;

        const serviceItems = document.querySelectorAll('.service-item');

        serviceItems.forEach(item => {
            const duration = parseInt(item.getAttribute('data-duration'));
            const price = parseInt(item.getAttribute('data-price') || 0);
            const id = item.getAttribute('data-id');

            let endTime = new Date(currentMockTime.getTime() + duration * 60000);

            const timeStr = `${formatTime(currentMockTime)} - ${formatTime(endTime)}`;

            const timeLabel = document.getElementById(`sum-time-${id}`);
            if(timeLabel) timeLabel.innerText = timeStr;

            updateAllocation(id);

            totalMinutes += duration;
            runningTotalServicePrice += price;
            currentMockTime = endTime;
        });

        currentTotalServicePrice = runningTotalServicePrice;

        estimateBox.style.display = 'flex';
        document.getElementById('durationText').innerText = `Total duration: ${totalMinutes} mins`;
        document.getElementById('endTimeText').innerText = `Est. finish: ${formatTime(currentMockTime)}`;

        document.getElementById('sumTimeDisplay').innerText = time;
        document.getElementById('sumEndTimeDisplay').innerText = `(Est. finish at ${formatTime(currentMockTime)})`;
        const dateObj = new Date(date);
        document.getElementById('sumDateDisplay').innerText = dateObj.toLocaleDateString('en-US', {weekday: 'long', day:'numeric', month:'long'});

        updateSummaryTotal();

    } else {
        document.getElementById('step-2').classList.add('disabled');
        document.getElementById('step-3').classList.add('disabled');
        document.getElementById('step-4').classList.add('disabled');
        estimateBox.style.display = 'none';
        document.getElementById('btnSubmit').disabled = true;
        if(timePlaceholder) timePlaceholder.classList.remove('d-none');
        timelineNodes.forEach(node => node.classList.add('d-none'));

        currentTotalServicePrice = 0;
        selectedVoucher = null;
        updateSummaryTotal();
    }
}