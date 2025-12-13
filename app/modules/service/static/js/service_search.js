document.addEventListener('DOMContentLoaded', () => {

    const heroSection = document.getElementById('heroSection');
    const parallaxText = document.getElementById('parallaxText');

    if (heroSection && parallaxText) {
        heroSection.addEventListener('mousemove', (e) => {
            const x = (window.innerWidth - e.pageX * 2) / 100;
            const y = (window.innerHeight - e.pageY * 2) / 100;
            parallaxText.style.transform = `translateX(${x}px) translateY(${y}px)`;
        });

        heroSection.addEventListener('mouseleave', () => {
            parallaxText.style.transform = 'translate(0,0)';
            parallaxText.style.transition = 'transform 0.5s ease';
            setTimeout(() => {
                parallaxText.style.transition = 'none';
            }, 500);
        });
    }

    const loadMoreBtn = document.querySelectorAll('.btn-outline-accent');
    if (loadMoreBtn.length > 0) {
        loadMoreBtn.forEach(
            btn => {
                btn.addEventListener('click', function (e) {
                    e.preventDefault();
                    const originalText = this.innerText;
                    this.innerText = 'Loading...';
                    this.classList.add('disabled');

                    setTimeout(() => {
                        this.innerText = originalText;
                        this.classList.remove('disabled');
                    }, 1000);
                });
            }
        )
    }

    const form = document.getElementById('filterForm');
    const container = document.getElementById('serviceListContainer');
    const pageInput = document.getElementById('currentPage');

    function getDataServicesFilter() {
        container.style.opacity = '0.5';

        const formFilter = new FormData(form)
        console.log(formFilter)
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

    const inputs = form.querySelectorAll('select, input');
    inputs.forEach(input => {
        if(input.name === 'search') {
            let timeOut = null;
            input.addEventListener('keyup', () => {
                clearTimeout()
                timeOut = setTimeout(() => {
                    pageInput.value = 1;
                    getDataServicesFilter();
                }, 500);
            });
        }
        else if (input.name !== 'page') {
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
                if(page) {
                    pageInput.value = page
                    getDataServicesFilter();
                    document.querySelector('.filter-sort-bar').scrollIntoView({ behavior: 'smooth' });
                }
            })
        })
    }
    rebindPagination()
});