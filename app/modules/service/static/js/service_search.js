document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('filterForm');
    const container = document.getElementById('serviceListContainer');
    const pageInput = document.getElementById('currentPage');

    function getDataServicesFilter() {
        container.style.opacity = '0.5';

        const formFilter = new FormData(form)
        const params = new URLSearchParams(formFilter)

        fetch(`/service/list?${params.toString()}`)
            .then(response => response.text())
            .then(html => {
                container.innerHTML = html
                container.style.opacity = '1'
                rebindPagination();
            })
            .catch(err => console.error(err));
    }

    const inputs = form.querySelectorAll('input');
    inputs.forEach(input => {
        if (input.name === 'search') {
            let timeOut = null;
            input.addEventListener('keyup', () => {
                clearTimeout()
                timeOut = setTimeout(() => {
                    pageInput.value = 1;
                    getDataServicesFilter();
                }, 500);
            });
        } else if (input.name !== 'page') {
            input.addEventListener('change', () => {
                pageInput.value = 1;
                getDataServicesFilter();
            })
        }
    });

    function rebindPagination() {
        const links = container.querySelectorAll('.page-link');
        links.forEach(link => {
            link.addEventListener('click', function (e) {
                e.preventDefault()
                const page = this.getAttribute('data-page');
                if (page) {
                    pageInput.value = page
                    getDataServicesFilter();
                }
            })
        })
    }
    rebindPagination()
});