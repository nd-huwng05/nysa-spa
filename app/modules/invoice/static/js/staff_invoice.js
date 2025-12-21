
/**
 * INVOICE MANAGEMENT LOGIC
 */
'use strict';

// 1. MOCK DATA
const INVOICES = [
    {
        id: 'INV-2025-001', customer: 'Nguyễn Khách A', date: '2025-12-20 10:30',
        items: [{name:'Combo Thư Giãn', price:450000}, {name:'Mặt Nạ', price:150000}],
        total: 600000, paid: 0, status: 'unpaid'
    },
    {
        id: 'INV-2025-002', customer: 'Trần Thị B', date: '2025-12-20 11:00',
        items: [{name:'Gội Đầu Dưỡng Sinh', price:200000}],
        total: 200000, paid: 200000, status: 'paid'
    },
    {
        id: 'INV-2025-003', customer: 'Phạm Văn C', date: '2025-12-20 12:15',
        items: [{name:'Trị Liệu Cổ Vai', price:350000}],
        total: 350000, paid: 100000, status: 'partial' // Thanh toán 1 phần
    }
];

let currentInvoice = null;

// 2. RENDER TABLE
function renderInvoiceTable(keyword = '') {
    const tbody = document.getElementById('invoiceTableBody');
    const statusFilter = document.getElementById('statusFilter').value;

    // Filter Data
    const filtered = INVOICES.filter(inv => {
        const matchesKey = inv.id.toLowerCase().includes(keyword.toLowerCase()) || inv.customer.toLowerCase().includes(keyword.toLowerCase());
        const matchesStatus = statusFilter === 'all' ||
                              (statusFilter === 'paid' && inv.status === 'paid') ||
                              (statusFilter === 'unpaid' && (inv.status === 'unpaid' || inv.status === 'partial'));
        return matchesKey && matchesStatus;
    });

    // Render HTML
    tbody.innerHTML = filtered.map(inv => {
        const due = inv.total - inv.paid;

        // Status Badge Logic
        let badgeClass = '';
        let badgeText = '';
        if(inv.status === 'paid') { badgeClass = 'bg-green-100 text-green-700'; badgeText = 'PAID'; }
        else if(inv.status === 'partial') { badgeClass = 'bg-blue-100 text-blue-700'; badgeText = 'PARTIAL'; }
        else { badgeClass = 'bg-red-100 text-red-700'; badgeText = 'UNPAID'; }

        return `
        <tr class="border-b border-gray-100 hover:bg-gray-50 transition">
            <td class="py-4 px-4 font-bold text-gray-700">${inv.id}</td>
            <td class="py-4 px-4">
                <div class="font-bold text-gray-800">${inv.customer}</div>
            </td>
            <td class="py-4 px-4 text-sm text-gray-500">${inv.date}</td>
            <td class="py-4 px-4 font-bold text-gray-800">${formatMoney(inv.total)}</td>
            <td class="py-4 px-4 text-green-600 font-medium">${formatMoney(inv.paid)}</td>
            <td class="py-4 px-4 text-red-500 font-bold">${formatMoney(due)}</td>
            <td class="py-4 px-4">
                <span class="px-3 py-1 rounded-full text-xs font-bold ${badgeClass}">${badgeText}</span>
            </td>
            <td class="py-4 px-4 text-center">
                ${inv.status !== 'paid' 
                    ? `<button onclick="openPaymentModal('${inv.id}')" class="text-white bg-[var(--accent-color)] hover:bg-[#a06d42] px-3 py-1.5 rounded text-xs font-bold shadow-sm transition">PAY</button>`
                    : `<button class="text-gray-400 hover:text-gray-600 px-3 py-1.5 rounded text-xs font-bold border border-gray-200"><i class="fas fa-print"></i></button>`
                }
            </td>
        </tr>`;
    }).join('');
}

// 3. PAYMENT LOGIC
function openPaymentModal(id) {
    const inv = INVOICES.find(i => i.id === id);
    if(!inv) return;
    currentInvoice = inv;

    // Fill Modal Data
    document.getElementById('modalInvoiceId').innerText = inv.id;
    document.getElementById('modalCustName').innerText = inv.customer;

    // Render Items
    document.getElementById('modalItemsList').innerHTML = inv.items.map(i =>
        `<div class="flex justify-between"><span>${i.name}</span><span>${formatMoney(i.price)}</span></div>`
    ).join('');

    // Totals
    const due = inv.total - inv.paid;
    document.getElementById('modalSubtotal').innerText = formatMoney(inv.total);
    document.getElementById('modalTotal').innerText = formatMoney(due); // Show remaining due

    // Reset Inputs
    document.getElementById('cashReceived').value = '';
    document.getElementById('cashChange').innerText = '0đ';
    selectPaymentMethod('cash'); // Default

    document.getElementById('paymentModal').showModal();
}

function selectPaymentMethod(method) {
    // UI Toggle
    document.querySelectorAll('.pay-btn').forEach(btn => btn.classList.remove('active-method'));
    if(method === 'cash') document.getElementById('btnCash').classList.add('active-method');
    if(method === 'transfer') document.getElementById('btnTransfer').classList.add('active-method');
    if(method === 'card') document.getElementById('btnCard').classList.add('active-method');

    // Show/Hide Cash Input
    const cashArea = document.getElementById('cashInputArea');
    if(method === 'cash') {
        cashArea.classList.remove('hidden');
        document.getElementById('cashReceived').focus();
    } else {
        cashArea.classList.add('hidden');
    }
}

function calculateChange() {
    if(!currentInvoice) return;
    const due = currentInvoice.total - currentInvoice.paid;
    const received = parseFloat(document.getElementById('cashReceived').value) || 0;
    const change = received - due;

    const elChange = document.getElementById('cashChange');
    if(change >= 0) {
        elChange.innerText = formatMoney(change);
        elChange.className = 'font-bold text-green-600';
    } else {
        elChange.innerText = 'Insufficient';
        elChange.className = 'font-bold text-red-500';
    }
}

function confirmPayment() {
    if(!currentInvoice) return;

    Swal.fire({
        title: 'Confirm Payment?',
        text: `Complete payment for ${currentInvoice.id}`,
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#C18C5D',
        confirmButtonText: 'Yes, Paid'
    }).then((result) => {
        if (result.isConfirmed) {
            // Logic cập nhật trạng thái (Mockup)
            currentInvoice.paid = currentInvoice.total;
            currentInvoice.status = 'paid';

            renderInvoiceTable(); // Refresh table
            document.getElementById('paymentModal').close();

            Swal.fire({
                icon: 'success',
                title: 'Payment Successful!',
                timer: 1500,
                showConfirmButton: false
            });
        }
    });
}

// Utils
function formatMoney(n) { return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(n); }

// Init
renderInvoiceTable();