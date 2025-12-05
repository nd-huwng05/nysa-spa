document.addEventListener('DOMContentLoaded', () => {

    // 1. Khởi tạo Animation khi cuộn trang (AOS)
    AOS.init({
        duration: 800,
        once: true,
        offset: 80
    });

    // 2. Parallax Effect cho Header Text (Bay theo chuột)
    const heroSection = document.getElementById('heroSection');
    const parallaxText = document.getElementById('parallaxText');

    if (heroSection && parallaxText) {
        heroSection.addEventListener('mousemove', (e) => {
            const x = (window.innerWidth - e.pageX * 2) / 100;
            const y = (window.innerHeight - e.pageY * 2) / 100;
            parallaxText.style.transform = `translateX(${x}px) translateY(${y}px)`;
        });

        // Reset vị trí khi chuột rời đi
        heroSection.addEventListener('mouseleave', () => {
            parallaxText.style.transform = 'translate(0,0)';
            parallaxText.style.transition = 'transform 0.5s ease';
            setTimeout(() => { parallaxText.style.transition = 'none'; }, 500);
        });
    }

    // 3. Load More Button Logic
    const loadMoreBtn = document.querySelector('.btn-outline-accent');
    if(loadMoreBtn) {
        loadMoreBtn.addEventListener('click', function(e) {
            e.preventDefault(); // Ngăn load lại trang
            const originalText = this.innerText;
            this.innerText = 'Đang tải...';
            this.classList.add('disabled');

            setTimeout(() => {
                alert('Đã tải thêm dịch vụ (Demo)');
                this.innerText = originalText;
                this.classList.remove('disabled');
            }, 1000);
        });
    }
});