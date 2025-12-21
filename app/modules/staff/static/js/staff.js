function formatDateISO(date) {
    const y = date.getFullYear();
    const m = String(date.getMonth() + 1).padStart(2, '0');
    const d = String(date.getDate()).padStart(2, '0');
    return `${y}-${m}-${d}`;
}

function navigateDate(offset) {
    let currentUrl = localStorage.getItem('last_active_url');
    
    if (!currentUrl) return;

    let urlObj = new URL(currentUrl, window.location.origin);

    let dateParam = urlObj.searchParams.get('date');
    let targetDate = dateParam ? new Date(dateParam) : new Date();

    targetDate.setDate(targetDate.getDate() + offset);

    urlObj.searchParams.set('date', formatDateISO(targetDate));

    const newUrl = urlObj.pathname + urlObj.search;

    loadTab(newUrl, null);
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
            Swal.fire({
                icon: 'error',
                title: 'Error load page',
                timer: 2000,
                showConfirmButton: false
            });
        } else {
            const result = await response.text();
            container.innerHTML = result;
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