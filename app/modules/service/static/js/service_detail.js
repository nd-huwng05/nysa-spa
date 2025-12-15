document.addEventListener('DOMContentLoaded', () => {

    // 1. Initialize Animation (AOS)
    AOS.init({
        duration: 800,
        once: true,
        offset: 80
    });

    // 2. Parallax Effect
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
            setTimeout(() => { parallaxText.style.transition = 'none'; }, 500);
        });
    }

    const swiper = new Swiper('.portfolio-details-slider', {
        loop: true,
        speed: 800,
        autoplay: {
            delay: 4000,
            disableOnInteraction: false,
        },
        effect: 'slide',
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        grabCursor: true,
    });

    const bookBtn = document.querySelector('.btn-accent');
    if(bookBtn) {
        bookBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const originalText = this.innerText;
            this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Checking...';
            this.style.opacity = '0.8';
            setTimeout(() => {
                alert('Thank you! Your booking request has been received.');
                this.innerText = originalText;
                this.style.opacity = '1';
            }, 1500);
        });
    }

    const dateInput = document.querySelector('input[type="date"]');
    if(dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.value = today;
        dateInput.min = today;
    }
});