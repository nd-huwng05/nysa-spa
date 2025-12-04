// main.js

document.addEventListener('DOMContentLoaded', function() {

    // --- 1. Khởi tạo AOS (Animate On Scroll) ---
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 1000,
            easing: 'ease-in-out',
            once: true,
            mirror: false
        });
    }

    // --- 2. Hiệu ứng Hover cho Hình ảnh và Thẻ Stats ---
    const statsCard = document.querySelector('.stats-card');
    const imageSecondary = document.querySelector('.image-secondary');

    // Hiệu ứng dịch chuyển nhẹ cho Stats Card khi hover
    if (statsCard) {
        statsCard.addEventListener('mouseenter', function() {
            statsCard.style.transition = 'transform 0.3s ease';
            statsCard.style.transform = 'translateY(-5px)';
        });
        statsCard.addEventListener('mouseleave', function() {
            statsCard.style.transform = 'translateY(0)';
        });
    }

    // Hiệu ứng nổi lên và zoom nhẹ cho Ảnh phụ khi hover
    if (imageSecondary) {
        imageSecondary.addEventListener('mouseenter', function() {
            // Dịch chuyển nhẹ ra ngoài vị trí ban đầu và scale lên
            imageSecondary.style.transform = 'translateX(-3%) translateY(-3%) scale(1.03)';
            imageSecondary.style.boxShadow = '0 25px 60px rgba(0, 0, 0, 0.8)';
            imageSecondary.style.zIndex = '40';
        });
        imageSecondary.addEventListener('mouseleave', function() {
            // Quay về vị trí CSS mặc định
            imageSecondary.style.transform = 'translateX(0) translateY(0) scale(1)';
            imageSecondary.style.boxShadow = '0 15px 50px rgba(0, 0, 0, 0.5)';
            imageSecondary.style.zIndex = '20';
        });
    }

    // --- 3. Hiệu ứng Đếm số (Count-up Animation) ---
    const statsItems = document.querySelectorAll('.stats-item h3');

    function countUp(el, endValue) {
        let current = 0;
        const duration = 2000;
        const step = endValue / (duration / 10);

        const timer = setInterval(() => {
            current += step;
            if (current >= endValue) {
                clearInterval(timer);
                current = endValue;
            }
            el.textContent = Math.floor(current) + '+';
        }, 10);
    }

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                statsItems.forEach(item => {
                    if (!item.hasAttribute('data-counted')) {
                         const valueText = item.textContent.replace('+', '');
                         const endValue = parseInt(valueText);
                         countUp(item, endValue);
                         item.setAttribute('data-counted', 'true');
                    }
                });
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    const aboutSection = document.querySelector('.about-section');
    if (aboutSection) {
        observer.observe(aboutSection);
    }
});