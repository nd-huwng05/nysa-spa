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
})