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