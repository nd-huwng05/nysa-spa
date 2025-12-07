/**
 * Khởi tạo Swiper cho Hero Section
 */
document.addEventListener('DOMContentLoaded', function() {
    const heroSwiper = document.querySelector('.hero .init-swiper');

    if (heroSwiper) {
        new Swiper(heroSwiper, {
            loop: true,
            speed: 1000,
            autoplay: {
                delay: 6000,
                disableOnInteraction: false
            },
            effect: "fade",
            fadeEffect: {
                crossFade: true
            },
            slidesPerView: 1,
            navigation: {
                nextEl: ".swiper-button-next",
                prevEl: ".swiper-button-prev"
            }
        });
    }
});

function initSwiper() {
        document.querySelectorAll(".init-swiper").forEach(function (swiperElement) {
            // 1. Nó tìm thẻ có class .swiper-config để lấy cấu hình JSON
            let config = JSON.parse(
                swiperElement.querySelector(".swiper-config").innerHTML.trim()
            );

            if (swiperElement.classList.contains("swiper-tab")) {
                initSwiperWithCustomPagination(swiperElement, config);
            } else {
                // 2. Nó khởi tạo Swiper ở đây
                new Swiper(swiperElement, config);
            }
        });
    }

    window.addEventListener("load", initSwiper);

