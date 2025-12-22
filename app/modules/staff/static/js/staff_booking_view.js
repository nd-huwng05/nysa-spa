'use strict';

let state = {
    cart: [],
    selectedCustomer: null,
    vouchers: []
};

let reloadTimer = null;

const formatMoney = (n) => new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(n);

const formatTime = (d) => {
    if (!d || isNaN(d.getTime())) return "00:00";
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });
};

const formatDateSimple = (d) => {
    if (!d || isNaN(d.getTime())) return "";
    const pad = (n) => String(n).padStart(2, '0');
    const y = d.getFullYear();
    const m = pad(d.getMonth() + 1);
    const day = pad(d.getDate());
    const h = pad(d.getHours());
    const min = pad(d.getMinutes());
    return `${y}-${m}-${day} ${h}:${min}:00`;
};

const formatDateTimePayload = (dateObj) => {
    if (!dateObj || isNaN(dateObj.getTime())) return null;
    const pad = (n) => String(n).padStart(2, '0');
    const y = dateObj.getFullYear();
    const m = pad(dateObj.getMonth() + 1);
    const d = pad(dateObj.getDate());
    const h = pad(dateObj.getHours());
    const min = pad(dateObj.getMinutes());
    const s = '00';
    return `${y}-${m}-${d} ${h}:${min}:${s}`;
};

function getSelectedStartTime() {
    const dVal = document.getElementById('bookingDate').value;
    const h = document.getElementById('selectHour').value;
    const m = document.getElementById('selectMin').value;

    if (!dVal) return null;

    const parts = dVal.split('-');
    if (parts.length === 3) {
        const year = parseInt(parts[0]);
        const month = parseInt(parts[1]) - 1;
        const day = parseInt(parts[2]);
        const hour = parseInt(h);
        const min = parseInt(m);
        return new Date(year, month, day, hour, min, 0, 0);
    }

    let dateObj = new Date(dVal);
    if (isNaN(dateObj.getTime())) return null;
    dateObj.setHours(parseInt(h), parseInt(m), 0, 0);
    return dateObj;
}

function toggleServiceMenuState() {
    const time = getSelectedStartTime();
    const serviceList = document.getElementById('serviceMenuList');
    const searchInput = document.querySelector('input[placeholder="Filter services..."]');

    if (!serviceList) return;

    if (time) {
        serviceList.style.opacity = '1';
        serviceList.style.pointerEvents = 'auto';
        if(searchInput) searchInput.disabled = false;
    } else {
        serviceList.style.opacity = '0.4';
        serviceList.style.pointerEvents = 'none';
        if(searchInput) searchInput.disabled = true;
    }
}

window.handleTimeChange = function() {
    toggleServiceMenuState();

    if (reloadTimer) clearTimeout(reloadTimer);

    window.renderCart();

    reloadTimer = setTimeout(async () => {
        await reloadAvailableStaffs();
        window.renderCart();
    }, 500);
};

window.openCreateModal = async function() {
    const modal = document.getElementById('createBookingModal');
    if (!modal) return;

    state.cart = [];
    state.selectedCustomer = null;
    state.vouchers = [];

    resetUI();
    initCurrentTime();
    toggleServiceMenuState();
    await window.renderServiceMenu("");

    modal.showModal();
};

function initCurrentTime() {
    const now = new Date();
    const datePart = now.getFullYear() + '-' + String(now.getMonth() + 1).padStart(2, '0') + '-' + String(now.getDate()).padStart(2, '0');
    const hour = String(now.getHours()).padStart(2, '0');
    const min = String(Math.floor(now.getMinutes() / 5) * 5).padStart(2, '0');

    const dateInput = document.getElementById('bookingDate');
    const hourInput = document.getElementById('selectHour');
    const minInput = document.getElementById('selectMin');

    if (dateInput && !dateInput.value) dateInput.value = datePart;
    if (hourInput && !hourInput.value) hourInput.value = hour;
    if (minInput && !minInput.value) minInput.value = min;

    if (dateInput) {
        dateInput.onchange = window.handleTimeChange;
        dateInput.oninput = window.handleTimeChange;
    }
    if (hourInput) hourInput.onchange = window.handleTimeChange;
    if (minInput) minInput.onchange = window.handleTimeChange;

    window.handleTimeChange();
}

async function reloadAvailableStaffs() {
    if (state.cart.length === 0) return;

    let currentStartTime = getSelectedStartTime();
    if (!currentStartTime) return;

    for (let i = 0; i < state.cart.length; i++) {
        let item = state.cart[i];
        let duration = Number(item.duration || 0);

        try {
            const simpleDateStr = formatDateSimple(currentStartTime);
            const response = await fetch(`/booking/staff-appointment-json?start=${encodeURIComponent(simpleDateStr)}&duration=${duration}`);
            const result = await response.json();

            if (result.data && Array.isArray(result.data)) {
                state.cart[i].availableStaffs = result.data.map(staff => ({
                    id: staff.id,
                    name: staff.fullname,
                    phone: staff.phone,
                    active: staff.active
                }));
            } else {
                state.cart[i].availableStaffs = [];
            }

        } catch (e) {
            console.warn(`Load staff error at index ${i}`, e);
            state.cart[i].availableStaffs = [];
        }

        if (currentStartTime) {
            currentStartTime = new Date(currentStartTime.getTime() + duration * 60000);
        }
    }
}

window.handleCustSearch = async function(query) {
    const box = document.getElementById('custSearchResults');
    if (!box) return;
    if (query.length < 2) {
        box.classList.add('hidden');
        return;
    }

    try {
        const response = await fetch(`/customer/search?data=${encodeURIComponent(query)}`);
        const result = await response.json();
        const customers = result.data || [];

        if (customers.length === 0) {
            box.innerHTML = `
                <div class="px-4 py-3 text-gray-400 text-sm italic border-b border-gray-50">No results found</div>
                <div onclick="window.showNewCustForm()" class="px-4 py-3 hover:bg-gray-50 cursor-pointer text-[#C18C5D] font-bold text-sm">
                    <i class="fas fa-plus-circle mr-1"></i> Create New Customer
                </div>`;
        } else {
            box.innerHTML = customers.map(c => `
                <div onclick='window.selectCustomer(${JSON.stringify(c)})' 
                     class="px-4 py-3 hover:bg-gray-50 cursor-pointer border-b border-gray-50 animate-fade-in">
                    <div class="font-bold text-gray-800 text-sm">${c.fullname || 'Unknown'}</div>
                    <div class="text-xs text-gray-500">${c.phone || ''}</div>
                </div>
            `).join('') + `
                <div onclick="window.showNewCustForm()" class="px-4 py-3 hover:bg-gray-50 cursor-pointer text-[#C18C5D] font-bold text-sm">
                    <i class="fas fa-plus-circle mr-1"></i> Create New Customer
                </div>`;
        }
        box.classList.remove('hidden');
    } catch (e) { console.error(e); }
};

window.showNewCustForm = function() {
    const searchInput = document.getElementById('custSearchInput');
    const newNameInput = document.getElementById('newCustName');
    const newPhoneInput = document.getElementById('newCustPhone');

    if (searchInput.value) {
        if (isNaN(searchInput.value)) {
            newNameInput.value = searchInput.value;
        } else {
            newPhoneInput.value = searchInput.value;
        }
    }
    document.getElementById('custSearchResults').classList.add('hidden');
    document.getElementById('newCustForm').classList.remove('hidden');
};

window.saveNewCust = async function() {
    const modal = document.getElementById('createBookingModal');
    const name = document.getElementById('newCustName').value.trim();
    const phone = document.getElementById('newCustPhone').value.trim();
    const email = document.getElementById('newCustEmail').value.trim();
    const address = document.getElementById('newCustAddress').value.trim();

    if (!name || !phone) {
        Swal.fire({ target: modal, icon: 'warning', title: 'Notice', text: 'Name & Phone required!' });
        return;
    }

    try {
        Swal.fire({ target: modal, title: 'Creating...', didOpen: () => Swal.showLoading() });
        const response = await fetch('/customer/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ fullname: name, phone: phone, email: email, address: address })
        });
        const result = await response.json();

        if (response.ok && result.status === "success") {
            window.selectCustomer(result.data);
            document.getElementById('newCustForm').classList.add('hidden');
            const inputs = document.getElementById('newCustForm').querySelectorAll('input');
            inputs.forEach(i => i.value = '');

            Swal.fire({ target: modal, icon: 'success', title: 'Success', timer: 1000, showConfirmButton: false });
        } else {
            throw new Error(result.message || 'Failed');
        }
    } catch (e) {
        Swal.fire({ target: modal, icon: 'error', title: 'Error', text: e.message });
    }
};

window.selectCustomer = async function(customer) {
    state.selectedCustomer = customer;
    document.getElementById('displayCustName').innerText = customer.fullname || customer.name;
    document.getElementById('displayCustPhone').innerText = customer.phone;
    document.getElementById('newCustForm').classList.add('hidden');
    document.getElementById('custSearchResults').classList.add('hidden');
    document.getElementById('custSearchInput').value = "";

    const subTotal = state.cart.reduce((sum, i) => sum + Number(i.price || 0), 0);
    await loadVouchers(customer.id, subTotal);
    window.calculateTotal();
};

async function loadVouchers(customerId, price = 0) {
    try {
        const response = await fetch(`/voucher/load?customer=${encodeURIComponent(customerId)}&price=${price}`);
        const result = await response.json();
        state.vouchers = result.data || [];

        const select = document.getElementById('voucherSelect');
        select.innerHTML = '<option value="0" data-discount="0" data-type="fixed">No Voucher</option>' +
            state.vouchers.map(v => `<option value="${v.id}" data-discount="${v.discount_value}" data-type="${v.discount_type}">${v.code} - ${v.description}</option>`).join('');

        select.onchange = window.calculateTotal;
    } catch (e) { console.warn("Voucher error"); }
}

window.renderServiceMenu = async function(query = "") {
    try {
        const response = await fetch(`/service/search?q=${encodeURIComponent(query)}`);
        const result = await response.json();
        const data = result.data || [];
        const container = document.getElementById('serviceMenuList');

        container.innerHTML = data.map(s => `
            <div onclick='window.addToCart(${JSON.stringify(s)})' 
                 class="group flex justify-between items-center p-3 bg-white border border-gray-100 rounded-lg cursor-pointer hover:border-[#C18C5D] shadow-sm transition-all">
                <div>
                    <div class="font-bold text-gray-800 text-sm">${s.name}</div>
                    ${s.type === 'combo' ? '<span class="text-[9px] bg-orange-50 text-orange-600 px-1 rounded font-bold">COMBO</span>' : `<span class="text-xs text-gray-400 italic">${s.duration_minutes}m</span>`}
                </div>
                <div class="font-bold text-[#C18C5D] text-sm">${formatMoney(s.price)}</div>
            </div>`).join('');

        toggleServiceMenuState();
    } catch (e) { console.error("Menu error"); }
};

window.addToCart = async function(service) {
    const timeCheck = getSelectedStartTime();
    if (!timeCheck) {
        Swal.fire({ icon: 'warning', title: 'Notice', text: 'Please select date and time first!' });
        return;
    }

    let subItems = service.items || [];

    const item = {
        ...service,
        price: Number(service.price || 0),
        duration: Number(service.duration_minutes || 0),
        uniqueId: Date.now(),
        isSplit: false,
        selectedStaffId: "",
        splitStaffs: subItems.map(sub => ({
            name: (typeof sub === 'string') ? sub : (sub.name || "Item"),
            staffId: ""
        }))
    };
    state.cart.push(item);

    window.renderCart();
    await reloadAvailableStaffs();
    window.renderCart();

    if (state.selectedCustomer) {
        const subTotal = state.cart.reduce((sum, i) => sum + i.price, 0);
        await loadVouchers(state.selectedCustomer.id, subTotal);
    }
};

window.removeFromCart = async function(uid) {
    state.cart = state.cart.filter(i => i.uniqueId !== uid);
    window.renderCart();
    await reloadAvailableStaffs();
    window.renderCart();

    if (state.selectedCustomer) {
        const subTotal = state.cart.reduce((sum, i) => sum + Number(i.price || 0), 0);
        await loadVouchers(state.selectedCustomer.id, subTotal);
    }
};

window.toggleComboSplit = function(uid) {
    const item = state.cart.find(i => i.uniqueId === uid);
    if (item) {
        item.isSplit = !item.isSplit;
        window.renderCart();
    }
};

window.renderCart = function() {
    const container = document.getElementById('cartContainer');
    const emptyState = document.getElementById('emptyState');

    if (state.cart.length === 0) {
        container.innerHTML = "";
        emptyState.classList.remove('hidden');
        window.calculateTotal();
        return;
    }

    emptyState.classList.add('hidden');

    let startTime = getSelectedStartTime();

    container.innerHTML = state.cart.map((item) => {
        let duration = item.duration || 0;
        let timeRange = "Waiting for time...";

        if (startTime) {
            let endTime = new Date(startTime.getTime() + duration * 60000);
            timeRange = `${formatTime(startTime)} - ${formatTime(endTime)}`;
            startTime = endTime;
        }

        const staffOptions = (item.availableStaffs || []).map(st =>
            `<option value="${st.id}" ${item.selectedStaffId == st.id ? 'selected' : ''}>${st.name}</option>`
        ).join('');

        return `
            <div class="border border-gray-100 rounded-lg bg-white overflow-hidden shadow-sm mb-3 animate-fade-in">
                <div class="bg-gray-50 px-4 py-2 border-b flex justify-between items-center">
                    <span class="text-[10px] font-black text-[#C18C5D] uppercase tracking-wider">${timeRange}</span>
                    <button onclick="window.removeFromCart(${item.uniqueId})" class="text-gray-300 hover:text-red-500 font-bold text-lg">×</button>
                </div>
                <div class="p-3">
                    <div class="flex justify-between mb-2">
                        <span class="font-bold text-gray-800 text-sm">${item.name}</span>
                        <span class="font-bold text-[#C18C5D]">${formatMoney(item.price)}</span>
                    </div>
                    ${item.type === 'combo' ? renderComboLogic(item, staffOptions) : renderSingleLogic(item, staffOptions)}
                </div>
            </div>`;
    }).join('');

    window.calculateTotal();
}

function renderSingleLogic(item, staffOptions) {
    return `
        <select onchange="window.updateStaff(${item.uniqueId}, this.value)" class="w-full text-xs border border-gray-200 rounded px-2 py-2 outline-none focus:border-[#C18C5D] cursor-pointer">
            <option value="">Select staff...</option>
            ${staffOptions}
        </select>`;
}

function renderComboLogic(item, staffOptions) {
    const isSplit = item.isSplit;

    const subItemsHtml = (item.splitStaffs && item.splitStaffs.length > 0)
        ? item.splitStaffs.map((sub, i) => `
            <div class="flex justify-between items-center py-2 border-t border-dashed border-gray-100 last:border-0 hover:bg-gray-50 transition-colors px-1">
                <span class="text-[11px] font-medium text-gray-600"><i class="fas fa-angle-right text-[var(--accent-color)] mr-1"></i> ${sub.name}</span>
                <select onchange="window.updateSubStaff(${item.uniqueId}, ${i}, this.value)" class="text-[10px] border border-gray-200 rounded px-2 py-1.5 outline-none w-32 focus:border-[var(--accent-color)] bg-white">
                    <option value="">Select staff...</option>
                    ${(item.availableStaffs || []).map(st => `<option value="${st.id}" ${sub.staffId == st.id ? 'selected' : ''}>${st.name}</option>`).join('')}
                </select>
            </div>
        `).join('')
        : `<div class="text-xs text-red-400 italic py-2">No sub-services found in data</div>`;

    return `
        <div class="flex items-center gap-2 mb-2">
            <span class="text-[10px] font-bold text-gray-400 uppercase">Split Staff</span>
            <div onclick="window.toggleComboSplit(${item.uniqueId})" 
                 class="w-8 h-4 rounded-full relative cursor-pointer transition-colors duration-300 ${isSplit ? 'bg-orange-400' : 'bg-gray-200'}">
                <div class="w-3 h-3 bg-white rounded-full absolute top-0.5 left-0.5 transition-transform duration-300 shadow-sm ${isSplit ? 'translate-x-4' : 'translate-x-0'}"></div>
            </div>
        </div>
        
        ${!isSplit 
            ? renderSingleLogic(item, staffOptions) 
            : `<div class="mt-2 pl-2 border-l-2 border-gray-100 animate-fade-in-down origin-top duration-300">
                 ${subItemsHtml}
               </div>`
        }
    `;
}

window.updateStaff = (uid, val) => { const itm = state.cart.find(i => i.uniqueId === uid); if (itm) itm.selectedStaffId = val; };
window.updateSubStaff = (uid, idx, val) => { const itm = state.cart.find(i => i.uniqueId === uid); if (itm) itm.splitStaffs[idx].staffId = val; };

window.calculateTotal = function() {
    const subTotal = state.cart.reduce((sum, i) => sum + Number(i.price || 0), 0);
    const voucherSelect = document.getElementById('voucherSelect');
    if (!voucherSelect) return;

    const selectedOption = voucherSelect.options[voucherSelect.selectedIndex];
    let discount = 0;

    if (selectedOption && selectedOption.value !== "0") {
        const val = Number(selectedOption.getAttribute('data-discount') || 0);
        const type = selectedOption.getAttribute('data-type');
        discount = type === 'percent' ? subTotal * (val / 100) : val;
    }

    const final = Math.max(0, subTotal - discount);
    document.getElementById('totalPrice').innerText = formatMoney(final);
};

window.submitBooking = async function() {
    const modal = document.getElementById('createBookingModal');

    if (!state.selectedCustomer) {
        return Swal.fire({ target: modal, icon: 'warning', title: 'Notice', text: 'Select a Customer!' });
    }
    if (state.cart.length === 0) {
        return Swal.fire({ target: modal, icon: 'warning', title: 'Notice', text: 'Cart is empty!' });
    }

    const startTimeObj = getSelectedStartTime();
    if (!startTimeObj) {
        return Swal.fire({ target: modal, icon: 'warning', title: 'Notice', text: 'Please select date and time first!' });
    }

    Swal.fire({ target: modal, title: 'Processing...', didOpen: () => Swal.showLoading(), allowOutsideClick: false });

    const totalSubAmount = state.cart.reduce((sum, i) => sum + Number(i.price || 0), 0);

    const voucherSelect = document.getElementById('voucherSelect');
    let totalAmount = totalSubAmount;
    let voucherId = null;

    if (voucherSelect && voucherSelect.value !== "0") {
        const selectedOption = voucherSelect.options[voucherSelect.selectedIndex];
        const val = Number(selectedOption.getAttribute('data-discount') || 0);
        const type = selectedOption.getAttribute('data-type');

        let discount = type === 'percent' ? totalSubAmount * (val / 100) : val;
        totalAmount = Math.max(0, totalSubAmount - discount);

        voucherId = voucherSelect.value;
    }

    let currentProcessTime = new Date(startTimeObj.getTime());

    const bookingDetails = state.cart.map(item => {
        const durationMs = (item.duration || 0) * 60000;
        const endTime = new Date(currentProcessTime.getTime() + durationMs);

        const startStr = formatDateTimePayload(currentProcessTime);
        const endStr = formatDateTimePayload(endTime);

        let subDetails = [];
        if (item.isSplit && item.splitStaffs && item.splitStaffs.length > 0) {
            subDetails = item.splitStaffs.map(sub => ({
                staff_id: sub.staffId ? parseInt(sub.staffId) : null,
                start: startStr,
                end: endStr
            }));
        }

        const detailPayload = {
            service_id: item.id,
            staff_id: item.selectedStaffId ? parseInt(item.selectedStaffId) : null,
            price: item.price,
            start: startStr,
            end: endStr,
            sub_detail: subDetails
        };

        currentProcessTime = endTime;

        return detailPayload;
    });

    const payload = {
        booking_time: formatDateTimePayload(startTimeObj),
        customer_id: state.selectedCustomer.id,
        notes: "",
        total_sub_amount: totalSubAmount,
        total_amount: totalAmount,
        voucher_id: voucherId,
        details: bookingDetails
    };



    try {
        const response = await fetch('/booking/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (response.ok) {
            await Swal.fire({ target: modal, icon: 'success', title: 'Success!', text: 'Booking Created', timer: 1500, showConfirmButton: false });
            location.reload();
        } else {
            throw new Error(result.message || result.error || 'Error from server');
        }
    } catch (e) {
        Swal.fire({ target: modal, icon: 'error', title: 'Error', text: e.message });
    }
};

function resetUI() {
    document.getElementById('displayCustName').innerText = 'Walk-in Guest';
    document.getElementById('displayCustPhone').innerText = 'No contact info';
    document.getElementById('custSearchInput').value = "";
    document.getElementById('newCustForm').classList.add('hidden');
    document.getElementById('totalPrice').innerText = '0 ₫';
    document.getElementById('voucherSelect').innerHTML = '<option value="0">No Voucher</option>';
}

async function submitAction(bookingId, action) {
    const targetElement = document.getElementById('checkin') || document.body;

    if (action === 'check_in') {
        const confirm = await Swal.fire({
            target: targetElement,
            title: 'Confirm Check-in',
            text: "Are you sure you want to check in this booking?",
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#C18C5D',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes',
            cancelButtonText: 'Cancel'
        });

        if (!confirm.isConfirmed) return;

        try {
            Swal.fire({
                target: targetElement,
                title: 'Processing...',
                didOpen: () => Swal.showLoading(),
                allowOutsideClick: false
            });

            const response = await fetch('/booking/checkin', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    booking_id: bookingId
                })
            });

            const result = await response.json();

            if (response.ok) {
                await Swal.fire({
                    target: targetElement,
                    icon: 'success',
                    title: 'Success!',
                    text: 'Check-in successful',
                    timer: 1500,
                    showConfirmButton: false
                });
                location.reload();
            } else {
                throw new Error(result.message || 'Server Error');
            }

        } catch (error) {
            Swal.fire({
                target: targetElement,
                icon: 'error',
                title: 'Error',
                text: error.message
            });
        }
    }
}