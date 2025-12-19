let selectedVoucher = null;
let currentTotalServicePrice = 0;
const SERVICE_BUFFER_MINUTES = 10;

document.addEventListener('DOMContentLoaded', function () {
    let initialTotal = 0;
    // CHỈNH SỬA: Tính tổng ban đầu chỉ lấy từ combo-box hoặc service-item độc lập
    document.querySelectorAll('#staffContainer > .combo-box, #staffContainer > .service-item:not(.combo-box .service-item)').forEach(item => {
        initialTotal += parseInt(item.getAttribute('data-price') || 0);
    });
    currentTotalServicePrice = initialTotal;

    flatpickr("#inputDate", {
        dateFormat: "Y-m-d",
        minDate: "today",
        disableMobile: "true",
        static: true,
        onChange: function (selectedDates, dateStr, instance) {
            checkStep1();
        }
    });

    const emailInput = document.getElementById('custEmail');
    if (emailInput && emailInput.value.trim() !== "") {
        fetchVoucher();
    }

    document.body.addEventListener('click', function (e) {
        const item = e.target.closest('.dropdown-item');
        if (!item) return;

        e.preventDefault();

        if (item.classList.contains('disabled') || item.tagName === 'HR') return;

        const wrapper = item.closest('.custom-select-wrapper');
        if (!wrapper) return;

        const button = wrapper.querySelector('.dropdown-toggle');
        const buttonSpan = button.querySelector('span');
        const hiddenInput = wrapper.querySelector('input[type="hidden"]');

        const text = item.textContent.trim();
        const value = item.getAttribute('data-value');
        const type = item.getAttribute('data-type');

        if (buttonSpan) buttonSpan.textContent = text;

        if (hiddenInput) {
            hiddenInput.value = value;
            const event = new Event('change', {bubbles: true});
            hiddenInput.dispatchEvent(event);
        }

        wrapper.querySelectorAll('.dropdown-item').forEach(i => i.classList.remove('active'));
        item.classList.add('active');

        if (type === 'hour' || type === 'minute') {
            handleTimeSelection();
        }

        if (hiddenInput && hiddenInput.closest('.combo-header')) {
            const comboBox = hiddenInput.closest('.combo-box');
            const comboId = comboBox.getAttribute('data-id');
            updateComboLogic(comboId, value);
        }

        if (hiddenInput && hiddenInput.id.startsWith('staff-select-')) {
            const serviceId = hiddenInput.id.replace('staff-select-', '');
            updateAllocation(serviceId);
        }
    });
});

function fetchVoucher() {
    const listContainer = document.querySelector('#step-4 .voucher-list-container');
    const emailInput = document.getElementById('custEmail');
    if (!listContainer || !emailInput) return;

    const email = emailInput.value.trim();
    if (email === "" || !email.includes('@')) return;

    const url = `/booking/voucher?total_price=${currentTotalServicePrice}&email=${encodeURIComponent(email)}`;

    fetch(url)
        .then(response => {
            if (response.ok) {
                return response.text();
            }
            throw new Error();
        })
        .then(htmlContent => {
            listContainer.outerHTML = htmlContent;
        })
        .catch(er => {
            Swal.fire({
                title: 'Error',
                text: '500 Error connect server',
                icon: 'error'
            });
        });
}

function handleTimeSelection() {
    const hourItem = document.querySelector('#hourWrapper .dropdown-item.active');
    const minuteItem = document.querySelector('#minuteWrapper .dropdown-item.active');
    const inputTime = document.getElementById('inputTime');

    if (hourItem && minuteItem) {
        const hour = hourItem.getAttribute('data-value');
        const minute = minuteItem.getAttribute('data-value');
        const finalTime = `${hour}:${minute}`;

        if (inputTime.value !== finalTime) {
            inputTime.value = finalTime;
            checkStep1();
        }
    }
}

function checkStep1() {
    const dateInput = document.getElementById('inputDate');
    const timeInput = document.getElementById('inputTime');
    const timelineNodes = document.querySelectorAll('.timeline-node');
    const timePlaceholder = document.getElementById('time-placeholder');

    let selectedDateObj = null;
    if (dateInput._flatpickr && dateInput._flatpickr.selectedDates.length > 0) {
        selectedDateObj = dateInput._flatpickr.selectedDates[0];
    } else if (dateInput.value) {
        selectedDateObj = new Date(dateInput.value);
    }
    const timeValue = timeInput.value;

    if (selectedDateObj && timeValue && timeValue.includes(':')) {
        document.getElementById('step-2').classList.remove('disabled');
        document.getElementById('step-3').classList.remove('disabled');
        document.getElementById('step-4').classList.remove('disabled');
        const btnSubmit = document.getElementById('btnSubmit');
        if (btnSubmit) btnSubmit.disabled = false;

        if (timePlaceholder) timePlaceholder.classList.add('d-none');
        timelineNodes.forEach(node => node.classList.remove('d-none'));

        let currentMockTime = new Date(selectedDateObj);
        const [hours, minutes] = timeValue.split(':').map(Number);
        currentMockTime.setHours(hours, minutes, 0, 0);

        let totalMinutes = 0;
        let runningTotalServicePrice = 0;
        let tempTime = new Date(currentMockTime);

        const container = document.getElementById('staffContainer');
        const topLevelNodes = container.querySelectorAll('#staffContainer > .combo-box, #staffContainer > .service-item:not(.combo-box .service-item)');

        topLevelNodes.forEach((node, index) => {
            if (index > 0) {
                tempTime = new Date(tempTime.getTime() + SERVICE_BUFFER_MINUTES * 60000);
                totalMinutes += SERVICE_BUFFER_MINUTES;
            }

            const currentTimeStr = formatDateTimeForApi(tempTime);

            if (node.classList.contains('combo-box')) {
                const comboId = node.getAttribute('data-id');
                let comboTotalDuration = 0;
                let comboStartTime = new Date(tempTime);

                const children = node.querySelectorAll('.service-item');
                children.forEach(child => {
                    comboTotalDuration += parseInt(child.getAttribute('data-duration') || 0);
                });

                const inputMaster = node.querySelector('.combo-header input[type="hidden"]');
                if (inputMaster) {
                    loadStaffData(inputMaster.id, currentTimeStr, comboTotalDuration, true, comboId);
                }

                children.forEach(child => {
                    const childDuration = parseInt(child.getAttribute('data-duration') || 0);
                    const childId = child.getAttribute('data-id');
                    const childInput = document.getElementById(`staff-select-${childId}`);

                    let childEndTime = new Date(tempTime.getTime() + childDuration * 60000);

                    const timeLabel = document.getElementById(`sum-time-${childId}`);
                    if (timeLabel) timeLabel.innerText = `${formatTime(tempTime)} - ${formatTime(childEndTime)}`;

                    if (childInput) {
                        const childStartStr = formatDateTimeForApi(tempTime);
                        childInput.setAttribute('data-start-api', childStartStr);
                        childInput.setAttribute('data-duration-api', childDuration);

                        const wrapper = childInput.closest('.custom-select-wrapper');
                        const btn = wrapper.querySelector('.dropdown-toggle');
                        if (!btn.classList.contains('d-none')) {
                            loadStaffData(childInput.id, childStartStr, childDuration, false, null);
                        }
                    }

                    tempTime = childEndTime;
                    totalMinutes += childDuration;
                });

                // CẬP NHẬT THỜI GIAN CHO COMBO CHA TRÊN SUMMARY
                const comboTimeLabel = document.getElementById(`sum-time-${comboId}`);
                if (comboTimeLabel) comboTimeLabel.innerText = `${formatTime(comboStartTime)} - ${formatTime(tempTime)}`;

                runningTotalServicePrice += parseInt(node.getAttribute('data-price') || 0);

            } else {
                const duration = parseInt(node.getAttribute('data-duration') || 0);
                const price = parseInt(node.getAttribute('data-price') || 0);
                const id = node.getAttribute('data-id');
                const inputStaff = document.getElementById(`staff-select-${id}`);

                let endTime = new Date(tempTime.getTime() + duration * 60000);

                const timeLabel = document.getElementById(`sum-time-${id}`);
                if (timeLabel) timeLabel.innerText = `${formatTime(tempTime)} - ${formatTime(endTime)}`;

                if (inputStaff) {
                    loadStaffData(inputStaff.id, currentTimeStr, duration, false, null);
                }

                updateAllocation(id);
                tempTime = endTime;
                totalMinutes += duration;
                runningTotalServicePrice += price;
            }
        });

        currentTotalServicePrice = runningTotalServicePrice;
        updateSummaryInfo(totalMinutes, tempTime, timeValue, selectedDateObj);
        updateSummaryTotal();

    } else {
        disableSteps();
    }
}

async function loadStaffData(elementId, startTime, duration, isMaster, comboId) {
    const input = document.getElementById(elementId);
    if (!input) return;

    const wrapper = input.closest('.custom-select-wrapper');
    if (!wrapper) return;

    wrapper.style.transition = 'all 0.2s ease';
    wrapper.style.opacity = '0.5';
    wrapper.style.filter = 'blur(1.5px)';
    wrapper.style.pointerEvents = 'none';
    wrapper.style.cursor = 'wait';

    try {
        const params = new URLSearchParams({
            start: startTime,
            duration: duration,
            input_id: elementId,
            is_master: isMaster
        });

        const response = await fetch(`/booking/staff-appointment?${params.toString()}`, {
            method: 'GET',
        });
        const htmlResponse = await response.text();

        if (htmlResponse && htmlResponse.trim().length > 0) {
            wrapper.outerHTML = htmlResponse;

            const newInput = document.getElementById(elementId);
            if (!newInput) return;

            const newWrapper = newInput.closest('.custom-select-wrapper');
            const newButton = newWrapper.querySelector('.dropdown-toggle');
            const newButtonSpan = newButton.querySelector('span');
            const newUl = newWrapper.querySelector('.dropdown-menu');

            const allItems = newUl.querySelectorAll('.dropdown-item');
            let firstValidStaff = null;

            for (let item of allItems) {
                const val = item.getAttribute('data-value');
                if (val && val !== 'split') {
                    firstValidStaff = item;
                    break;
                }
            }

            if (firstValidStaff) {
                const staffId = firstValidStaff.getAttribute('data-value');
                const staffName = firstValidStaff.textContent.trim();

                newInput.value = staffId;
                newButtonSpan.textContent = staffName;

                newUl.querySelectorAll('.dropdown-item').forEach(i => i.classList.remove('active'));
                firstValidStaff.classList.add('active');

                if (isMaster) {
                    updateComboLogic(comboId, staffId);
                } else {
                    const sId = newInput.id.replace('staff-select-', '');
                    updateAllocation(sId);
                }
            } else {
                fallbackNoStaff(newInput, newButtonSpan, isMaster, comboId);
            }
        }

    } catch (e) {
        console.error("API Error:", e);
        if (wrapper) {
            wrapper.style.opacity = '1';
            wrapper.style.filter = 'none';
            wrapper.style.pointerEvents = 'auto';
            wrapper.style.cursor = 'default';
            wrapper.querySelector('span').textContent = "Error";
        }
    }
}

function fallbackNoStaff(input, buttonSpan, isMaster, comboId) {
    if (isMaster) {
        input.value = "split";
        buttonSpan.textContent = "Split";
        updateComboLogic(comboId, 'split');
    } else {
        input.value = "";
        buttonSpan.textContent = "No service suitable";
    }
}

function updateComboLogic(comboId, masterValue) {
    const comboBox = document.querySelector(`.combo-box[data-id="${comboId}"]`);
    if (!comboBox) return;

    const childWrappers = comboBox.querySelectorAll('.service-item .custom-select-wrapper');

    if (masterValue === 'split') {
        childWrappers.forEach(wrapper => {
            const btn = wrapper.querySelector('.dropdown-toggle');
            const hiddenInput = wrapper.querySelector('input[type="hidden"]');

            btn.classList.remove('d-none');
            btn.classList.remove('disabled');

            const startApi = hiddenInput.getAttribute('data-start-api');
            const durationApi = hiddenInput.getAttribute('data-duration-api');

            if (startApi && durationApi) {
                loadStaffData(hiddenInput.id, startApi, durationApi, false, null);
            }
        });

    } else {
        childWrappers.forEach(wrapper => {
            const btn = wrapper.querySelector('.dropdown-toggle');
            const hiddenInput = wrapper.querySelector('input[type="hidden"]');

            btn.classList.add('d-none');
            btn.classList.add('disabled');

            hiddenInput.value = masterValue;

            const sId = hiddenInput.id.replace('staff-select-', '');
            updateAllocation(sId);
        });
    }
}

function updateAllocation(serviceId) {
    const input = document.getElementById(`staff-select-${serviceId}`);
    if (!input) return;

    const wrapper = input.closest('.custom-select-wrapper');
    const btn = wrapper.querySelector('.dropdown-toggle');
    let staffName = "";

    // CHỈNH SỬA: Cập nhật chính xác nhân viên vào node cha hoặc con trong summary
    if (btn.classList.contains('d-none')) {
        const comboBox = input.closest('.combo-box');
        if (comboBox) {
            staffName = comboBox.querySelector('.combo-header .dropdown-toggle span').textContent;
            const masterStaffLabel = document.getElementById(`sum-staff-master-${comboBox.getAttribute('data-id')}`);
            if (masterStaffLabel) masterStaffLabel.innerText = staffName;
        }
    } else {
        staffName = btn.querySelector('span').textContent;
    }

    const summaryLabel = document.getElementById(`sum-staff-${serviceId}`);
    if (summaryLabel) {
        summaryLabel.innerText = staffName;
    }
    updateSummaryTotal();
}

function updateSummaryInfo(totalMinutes, endTime, startTimeStr, dateObj) {
    document.getElementById('timeEstimate').style.display = 'flex';
    document.getElementById('durationText').innerText = `Total duration: ${totalMinutes} mins`;
    document.getElementById('endTimeText').innerText = `Est. finish: ${formatTime(endTime)}`;

    const sumTime = document.getElementById('sumTimeDisplay');
    if (sumTime) sumTime.innerText = startTimeStr;
    const sumEnd = document.getElementById('sumEndTimeDisplay');
    if (sumEnd) sumEnd.innerText = `(Est. finish at ${formatTime(endTime)})`;
    const sumDate = document.getElementById('sumDateDisplay');
    if (sumDate && dateObj) {
        sumDate.innerText = dateObj.toLocaleDateString('vi-VN', {weekday: 'long', day: 'numeric', month: 'long'});
    }
}

function disableSteps() {
    document.getElementById('step-2').classList.add('disabled');
    document.getElementById('step-3').classList.add('disabled');
    document.getElementById('step-4').classList.add('disabled');
    document.getElementById('timeEstimate').style.display = 'none';
    const btnSubmit = document.getElementById('btnSubmit');
    if (btnSubmit) btnSubmit.disabled = true;

    document.querySelectorAll('.timeline-node').forEach(n => n.classList.add('d-none'));
    if (document.getElementById('time-placeholder')) {
        document.getElementById('time-placeholder').classList.remove('d-none');
    }
    currentTotalServicePrice = 0;
    updateSummaryTotal();
}

function formatDateTimeForApi(date) {
    const y = date.getFullYear();
    const m = String(date.getMonth() + 1).padStart(2, '0');
    const d = String(date.getDate()).padStart(2, '0');
    const h = String(date.getHours()).padStart(2, '0');
    const min = String(date.getMinutes()).padStart(2, '0');
    return `${y}-${m}-${d} ${h}:${min}`;
}

function formatTime(date) {
    return date.toLocaleTimeString('en-GB', {hour: '2-digit', minute: '2-digit', hour12: false});
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

    if (voucher.discount_type === 'PERCENT') {
        discount = total * (value / 100);
    } else if (voucher.discount_type === 'FIXED') {
        discount = value;
    }

    if (max && max > 0 && discount > max) {
        discount = max;
    }

    return Math.round(discount);
}

function updateSummaryTotal() {
    let total = 0;
    document.querySelectorAll('#staffContainer > .combo-box, #staffContainer > .service-item:not(.combo-box .service-item)').forEach(item => {
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
        amountDisplay.innerText = `-${formatCurrency(discountAmount)}`;
    } else {
        appliedCode.innerText = '';
        discountRow.style.display = 'none';
        amountDisplay.innerText = `${formatCurrency(0)}`;
    }

    document.getElementById('sumTotal').innerText = formatCurrency(finalTotal);
    const btnSubmit = document.getElementById('btnSubmit');
    if (btnSubmit) btnSubmit.disabled = (total === 0);
}

async function toggleEditInfo(btn) {
    const inputs = document.querySelectorAll('#custName, #custPhone, #custAddress, #custEmail');
    const btnSpan = btn.querySelector('span');
    const icon = btn.querySelector('i');
    const isReadonly = inputs[0].hasAttribute('readonly');

    if (isReadonly) {
        inputs.forEach(input => input.removeAttribute('readonly'));
        btnSpan.textContent = 'Save';
        icon.className = 'fas fa-save me-2';
        btn.classList.remove('btn-outline-primary');
        btn.classList.add('btn-primary');
        inputs[0].focus();
    } else {
        btn.disabled = true;
        try {
            const updateData = {
                id: document.getElementById('custId').value,
                fullname: document.getElementById('custName').value,
                phone: document.getElementById('custPhone').value,
                address: document.getElementById('custAddress').value,
                email: document.getElementById('custEmail').value
            };

            const response = await fetch('/customer/update-info', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(updateData)
            });

            if (response.ok) {
                Swal.fire({
                    title: 'Success',
                    text: 'Information updated',
                    icon: 'success',
                    confirmButtonText: 'OK',
                    confirmButtonColor: '#3085d6'
                }).then(() => {
                    inputs.forEach(input => input.setAttribute('readonly', true));
                    btnSpan.textContent = 'Update';
                    icon.className = 'fas fa-pen me-2';
                    btn.classList.remove('btn-primary');
                    btn.classList.add('btn-outline-primary');
                    btn.disabled = false;
                    if (updateData.email && updateData.email.trim() !== "") {
                        fetchVoucher();
                    }
                });
            } else {
                btn.disabled = false;
                Swal.fire({title: 'Error', text: 'Update failed', icon: 'error'});
            }
        } catch (error) {
            btn.disabled = false;
            Swal.fire({title: 'Error', text: "Connection failed", icon: 'error'});
        }
    }
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
    btn.innerHTML = isHidden ? '<i class="fas fa-ticket-alt me-1"></i> Code' : '<i class="fas fa-list-ul me-1"></i> Hide';
    btn.classList.toggle('btn-outline-secondary');
    btn.classList.toggle('btn-secondary');
}

function applyVoucherCode() {
    const code = document.getElementById('inputVoucherCode').value.toUpperCase();
    if (!code) return;
    document.getElementById('inputVoucherCode').value = '';
}

function selectVoucher(btn, id, code) {
    const itemElement = btn.closest('.voucher-item');
    document.querySelectorAll('.apply-voucher-btn').forEach(b => {
        b.innerHTML = 'Apply';
        b.classList.remove('btn-success');
        b.classList.remove('btn-apply');
        b.classList.add('btn-outline-success');
    });

    if (selectedVoucher && selectedVoucher.code === code) {
        removeVoucher();
        return;
    }

    btn.innerHTML = '<i class="fas fa-check me-1"></i> Applied';
    btn.classList.remove('btn-outline-success');
    btn.classList.add('btn-success');
    btn.classList.add('btn-apply');

    selectedVoucher = {
        id : id,
        code: code,
        discount_type: itemElement.getAttribute('data-type'),
        discount_value: parseFloat(itemElement.getAttribute('data-value')),
        max_discount_amount: parseFloat(itemElement.getAttribute('data-max-amount')) || null,
        min_order_value: parseFloat(itemElement.getAttribute('data-min-order')),
    };
    updateSummaryTotal();
}

async function submitBooking() {
    const bookingDate = document.getElementById('inputDate').value;
    const bookingTime = document.getElementById('inputTime').value;
    const customerId = document.getElementById('custId').value;
    const notes = document.getElementById('custNotes')?.value || "";

    if (!bookingDate || !bookingTime) {
        Swal.fire("Error", "Please select both date and time!", "error");
        return;
    }

    const totalAmountStr = document.getElementById('sumTotal').innerText;
    const totalAmount = parseInt(totalAmountStr.replace(/\D/g, ''));
    const subAmountStr = document.getElementById('sumSubTotal').innerText;
    const subAmount = parseInt(subAmountStr.replace(/\D/g, ''));
    const details = [];
    const topLevelNodes = document.querySelectorAll('#staffContainer > .combo-box, #staffContainer > .service-item:not(.combo-box .service-item)');

    topLevelNodes.forEach(node => {
        if (node.classList.contains('combo-box')) {
            const comboId = node.getAttribute('data-id');
            const comboPrice = node.getAttribute('data-price');
            const comboTimeElem = document.getElementById(`sum-time-${comboId}`);

            if (!comboTimeElem) return;

            const comboTimeRange = comboTimeElem.innerText.split(' - ');
            const masterStaffId = document.getElementById(`staff-select-combo-${comboId}`)?.value;

            const comboDetail = {
                service_id: comboId,
                staff_id: masterStaffId,
                start: `${bookingDate} ${comboTimeRange[0]}`,
                end: `${bookingDate} ${comboTimeRange[1]}`,
                price: comboPrice,
                sub_detail: [],
            };

            node.querySelectorAll('.service-item').forEach(child => {
                const childId = child.getAttribute('data-id');
                const childTimeElem = document.getElementById(`sum-time-${childId}`);

                if (childTimeElem) {
                    const childTimeRange = childTimeElem.innerText.split(' - ');
                    const childStaffId = document.getElementById(`staff-select-${childId}`)?.value;

                    comboDetail.sub_detail.push({
                        service_id: childId,
                        type: 'COMBO',
                        staff_id: childStaffId,
                        start: `${bookingDate} ${childTimeRange[0]}`,
                        end: `${bookingDate} ${childTimeRange[1]}`,
                        price: 0
                    });
                }
            });
            details.push(comboDetail);
        } else {
            const sId = node.getAttribute('data-id');
            const sPrice = node.getAttribute('data-price');
            const sTimeElem = document.getElementById(`sum-time-${sId}`);

            if (sTimeElem) {
                const sTimeRange = sTimeElem.innerText.split(' - ');
                const sStaffId = document.getElementById(`staff-select-${sId}`)?.value;

                details.push({
                    service_id: sId,
                    type: 'SINGLE',
                    staff_id: sStaffId,
                    start: `${bookingDate} ${sTimeRange[0]}`,
                    end: `${bookingDate} ${sTimeRange[1]}`,
                    price: sPrice
                });
            }
        }
    });

    const payload = {
        customer_id: customerId,
        booking_time: `${bookingDate} ${bookingTime}`,
        total_sub_amount: subAmount,
        total_amount: totalAmount,
        voucher_id: selectedVoucher ? selectedVoucher.id : null,
        notes: notes,
        details: details
    };

    try {
        Swal.showLoading();
        const response = await fetch('/booking/create', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });

        const result = await response.json();
        if (response.ok) {
            Swal.fire({
                icon: 'success',
                title: 'Booking Successful!',
                text: 'Code: ' + result.data.booking_code,
                timer: 2000,
                showConfirmButton: false
            }).then(() => {
                window.location.href = "/invoice/payment?booking_id=" + result.data.booking_id;
            });
        } else {
            Swal.fire("Error", result.message || "Failed to create booking", "error");
        }
    } catch (error) {
        Swal.fire("Error", "Connection error", "error");
    }
}

