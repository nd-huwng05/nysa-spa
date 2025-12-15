const STORAGE_KEY = 'cart_selected_items'

function formatCurrency(amount) {
    return new Intl.NumberFormat('vi-VN', {style: 'currency', currency: 'VND'}).format(amount);
}

function calculateTotal() {
    let total = 0;
    const checkboxes = document.querySelectorAll('.service-check:checked');

    const summaryList = document.getElementById('selected-services-list');
    summaryList.innerHTML = '';

    if (checkboxes.length === 0) {
        summaryList.innerHTML = '<p class="text-muted text-center fst-italic">No Service</p>';
    }

    checkboxes.forEach(box => {
        const price = parseInt(box.getAttribute('data-price'));
        const cartItem = box.closest('.cart-item');
        const name = cartItem.querySelector('.item-name').innerText;

        total += price;

        const itemRow = document.createElement('div');
        itemRow.className = 'summary-item';
        itemRow.innerHTML = `
            <span class="name" title="${name}">${name}</span>
            <span class="price">${formatCurrency(price)}</span>
        `;

        summaryList.appendChild(itemRow);
    });
    document.getElementById('total-price').innerText = formatCurrency(total);
}

function removeItem(itemId) {
    const item = document.getElementById(itemId);
    if (item) {
        item.style.transition = 'opacity 0.3s, transform 0.3s';
        item.style.opacity = '0';
        item.style.transform = 'scale(0.9)';

        setTimeout(() => {
            item.remove();
            calculateTotal();
        }, 300);
    }
}

document.addEventListener('DOMContentLoaded', calculateTotal);

document.addEventListener("DOMContentLoaded", function () {
    loadCheckedState();

    const checkboxes = document.querySelectorAll('.service-check');
    checkboxes.forEach(box => {
        box.addEventListener('change', function () {
            saveCheckedState();
        });
    });
})

function saveCheckedState() {
    let selectedIds = [];
    document.querySelectorAll('.service-check:checked').forEach(box => {
        selectedIds.push(box.value);
    });
    localStorage.setItem(STORAGE_KEY, JSON.stringify(selectedIds));
}

function loadCheckedState() {
    const storedIds = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
    if (storedIds.length > 0) {
        storedIds.forEach(id => {
            let checkbox = document.querySelector(`.service-check[value="${id}"]`);
            if (checkbox) {
                checkbox.checked = true;
            }
        });
        if (typeof calculateTotal === "function") {
            calculateTotal();
        }
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const btnProcessingBook = document.getElementById('processing-booking-from-cart')
    btnProcessingBook.addEventListener('click', function () {
        const checkedBoxes = document.querySelectorAll('.service-check:checked');
        if (!btnProcessingBook) {
            console.log("NOT FOUND PROCESSING BOOKING BTN")
        }

        if (checkedBoxes.length == 0) {
            alert("You need choose least one service")
            return;
        }

        const params = new URLSearchParams();
        checkedBoxes.forEach(box => {
            params.append('service', box.value);
        });

        const queryString = params.toString()
        window.location.href = `/booking/appointment?${queryString}`;
    })
})