let currentDate = new Date();

document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const dateParam = urlParams.get('date');

    if (dateParam) {
        currentDate = new Date(dateParam);
    }

    updateDateDisplay();
});

function updateDateDisplay() {
    const displayElement = document.getElementById('currentDateDisplay');
    if (!displayElement) return;

    const today = new Date();
    const isToday = currentDate.getDate() === today.getDate() &&
                    currentDate.getMonth() === today.getMonth() &&
                    currentDate.getFullYear() === today.getFullYear();

    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    const dateString = currentDate.toLocaleDateString('en-US', options);

    displayElement.innerText = isToday ? `Today, ${dateString}` : dateString;
}

function navigateDate(offset) {
    let currentUrl = localStorage.getItem('last_active_url') || window.location.href;
    let urlObj = new URL(currentUrl, window.location.origin);

    let dateParam = urlObj.searchParams.get('date');
    let targetDate = dateParam ? new Date(dateParam) : new Date();

    targetDate.setDate(targetDate.getDate() + offset);

    const newDateString = formatDateISO(targetDate);

    urlObj.searchParams.set('date', newDateString);
    const newUrl = urlObj.pathname + urlObj.search;

    currentDate = targetDate;
    updateDateDisplay();

    loadTab(newUrl, null);
    localStorage.setItem('last_active_url', newUrl);
}

function formatDateISO(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

async function loadTab(url, element) {
    const container = document.getElementById('tab-staff');

    container.innerHTML = `
        <div class="flex items-center justify-center h-[60vh]">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#C18C5D]"></div>
        </div>`;

    if (element) {
        const allMenus = document.querySelectorAll('.menu-item');
        allMenus.forEach(el => {
            el.classList.remove('text-[#C18C5D]', 'bg-[#F7F5F2]', 'border-r-4', 'border-[#C18C5D]');
            el.classList.add('text-gray-600', 'hover:bg-gray-50', 'border-r-4', 'border-transparent');
        });

        element.classList.remove('text-gray-600', 'hover:bg-gray-50', 'border-transparent');
        element.classList.add('text-[#C18C5D]', 'bg-[#F7F5F2]', 'border-[#C18C5D]');
    }

    localStorage.setItem('last_active_url', url);

    try {
        const response = await fetch(url);
        if (!response.ok) {
            if (typeof Swal !== 'undefined') {
                Swal.fire({
                    icon: 'error',
                    title: 'Error load page',
                    timer: 2000,
                    showConfirmButton: false
                });
            }
        } else {
            const result = await response.text();
            container.innerHTML = result;

            let loadedUrlObj = new URL(url, window.location.origin);
            let loadedDate = loadedUrlObj.searchParams.get('date');

            if (loadedDate) {
                currentDate = new Date(loadedDate);
            }

            updateDateDisplay();
        }

    } catch (error) {
        if (typeof Swal !== 'undefined') {
            Swal.fire({
                icon: 'error',
                title: 'Error Connect',
                text: error.message || error,
                confirmButtonColor: '#C18C5D'
            });
        }
    }
}