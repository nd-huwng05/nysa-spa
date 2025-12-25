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

function sendCheckToServer(checkbox) {
    const status = checkbox.checked;
    const id = checkbox.value;

    fetch('/cart/toggle-check', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},

        body: JSON.stringify({
            id: id,
            checked: status
        })
    });
}

