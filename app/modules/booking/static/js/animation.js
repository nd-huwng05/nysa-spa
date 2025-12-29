document.addEventListener('DOMContentLoaded', function() {
    document.body.addEventListener('click', function(e) {
        const item = e.target.closest('.dropdown-item');
        if (!item || item.classList.contains('time-part-select')) return;

        const wrapper = item.closest('.custom-select-wrapper');
        if (!wrapper) return;

        const input = wrapper.querySelector('.staff-input');
        if (!input) return;

        e.preventDefault();

        const staffId = item.getAttribute('data-value');
        const staffName = item.textContent.trim();

        input.value = staffId;
        const btnText = wrapper.querySelector('.custom-dropdown-btn .text-limit');
        if (btnText) btnText.textContent = staffName;

        wrapper.querySelectorAll('.dropdown-item').forEach(el => el.classList.remove('active'));
        item.classList.add('active');

        const container = wrapper.closest('[data-row-key]');

        if (input.classList.contains('is-combo-master')) {
            const comboBox = wrapper.closest('.combo-box');

            if (staffId === 'split') {
                if (comboBox) {
                    const children = comboBox.querySelectorAll('.service-item');

                    children.forEach(child => {
                        const childBtn = child.querySelector('.custom-dropdown-btn');
                        if (childBtn) {
                            childBtn.classList.remove('d-none');
                            childBtn.classList.add('d-flex');
                        }

                        const childKey = child.getAttribute('data-row-key');
                        const childNameEl = child.querySelector('.custom-dropdown-btn .text-limit');

                        if (childKey && childNameEl) {
                            const originalName = childNameEl.textContent.trim();
                            updateSummaryExactlyByKey(childKey, originalName);

                            const childInput = child.querySelector('.staff-input');
                            const activeItem = child.querySelector('.dropdown-item.active');
                            if (childInput && activeItem) {
                                childInput.value = activeItem.getAttribute('data-value');
                            }
                        }
                    });

                    if (container) {
                        const parentKey = container.getAttribute('data-row-key');
                        updateSummaryExactlyByKey(parentKey, "");
                    }
                }
            } else {
                if (container) {
                    const parentKey = container.getAttribute('data-row-key');
                    updateSummaryExactlyByKey(parentKey, staffName);
                }

                if (comboBox) {
                    const children = comboBox.querySelectorAll('.service-item');
                    children.forEach(child => {
                        const childKey = child.getAttribute('data-row-key');
                        updateSummaryExactlyByKey(childKey, staffName);

                        const childBtn = child.querySelector('.custom-dropdown-btn');
                        const childInput = child.querySelector('.staff-input');
                        if (childBtn) {
                            childBtn.classList.add('d-none');
                            childBtn.classList.remove('d-flex');
                        }
                        if (childInput) childInput.value = staffId;
                    });
                }
            }
        } else {
            if (container) {
                const specificKey = container.getAttribute('data-row-key');
                updateSummaryExactlyByKey(specificKey, staffName);
            }
        }
    });
});

function updateSummaryExactlyByKey(key, newName) {
    if (!key) return;

    const summaryRow = document.querySelector(`#summaryTimeline [data-row-key="${key}"]`);

    if (summaryRow) {
        const staffLabel = summaryRow.querySelector('.js-sum-staff');

        if (staffLabel) {
            staffLabel.textContent = newName;
            staffLabel.style.opacity = '0.5';
            staffLabel.style.transition = 'opacity 0.3s';
            setTimeout(() => {
                staffLabel.style.opacity = '1';
                staffLabel.classList.add('text-primary');
                setTimeout(() => staffLabel.classList.remove('text-primary'), 500);
            }, 150);
        }
    }
}

const formatCurrency = (amount) => {
    return new Intl.NumberFormat('vi-VN').format(amount) + 'đ';
};

const parseCurrency = (str) => {
    if (!str) return 0;
    return parseInt(str.replace(/[^\d]/g, '')) || 0;
};

function selectVoucher(btn) {
    const voucherItem = btn.closest('.voucher-item');
    if (!voucherItem) return;

    const isApplied = btn.classList.contains('btn-success');
    const subTotalEl = document.getElementById('sumSubTotal');
    const subTotal = parseCurrency(subTotalEl.textContent);

    if (isApplied) {
        document.getElementById('voucher-code').value = '';

        const discountLabel = document.getElementById('discountAmount');
        if (discountLabel) {
            discountLabel.textContent = '0đ';
            discountLabel.style.color = 'inherit';
        }

        const voucherLabel = document.getElementById('appliedVoucherCode');
        if (voucherLabel) voucherLabel.textContent = '';

        const totalLabel = document.getElementById('sumTotal');
        if (totalLabel) totalLabel.textContent = formatCurrency(subTotal);

        const hiddenVoucher = document.getElementById('hidden_voucher');
        if (hiddenVoucher) hiddenVoucher.value = '';

        const hiddenTotal = document.getElementById('total_price');
        if (hiddenTotal) hiddenTotal.value = subTotal;

        voucherItem.classList.remove('border-primary', 'bg-light');
        btn.textContent = 'Apply';
        btn.classList.remove('btn-success');
        btn.classList.add('btn-outline-success');

        return;
    }

    const code = voucherItem.getAttribute('data-code');
    const type = voucherItem.getAttribute('data-type');
    const value = parseFloat(voucherItem.getAttribute('data-value')) || 0;
    const maxDiscount = parseFloat(voucherItem.getAttribute('data-max-amount')) || 0;

    document.querySelectorAll('.voucher-item').forEach(el => {
        el.classList.remove('border-primary', 'bg-light');
        const b = el.querySelector('.apply-voucher-btn');
        if (b) {
            b.textContent = 'Apply';
            b.classList.remove('btn-success');
            b.classList.add('btn-outline-success');
        }
    });

    let discountAmount = 0;

    if (type === 'FIXED') {
        discountAmount = value;
    } else if (type === 'PERCENT') {
        discountAmount = subTotal * (value / 100);
        if (maxDiscount > 0 && discountAmount > maxDiscount) {
            discountAmount = maxDiscount;
        }
    }

    if (discountAmount > subTotal) discountAmount = subTotal;

    const displayInput = document.getElementById('voucher-code');
    if (displayInput) displayInput.value = code;

    const voucherLabel = document.getElementById('appliedVoucherCode');
    const discountLabel = document.getElementById('discountAmount');

    if (voucherLabel) voucherLabel.textContent = code;
    if (discountLabel) {
        discountLabel.textContent = '-' + formatCurrency(discountAmount);
        discountLabel.style.color = '#dc3545';
    }

    const finalTotal = subTotal - discountAmount;
    const totalLabel = document.getElementById('sumTotal');
    if (totalLabel) {
        totalLabel.textContent = formatCurrency(finalTotal);
    }

    const hiddenVoucher = document.getElementById('hidden_voucher');
    const hiddenTotal = document.getElementById('total_price');

    if (hiddenVoucher) hiddenVoucher.value = code;
    if (hiddenTotal) hiddenTotal.value = finalTotal;

    voucherItem.classList.add('border-primary', 'bg-light');
    btn.textContent = 'Applied';
    btn.classList.remove('btn-outline-success');
    btn.classList.add('btn-success');

    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000
    });
    Toast.fire({
        icon: 'success',
        title: `Applied ${code}`
    });
}