document.addEventListener('DOMContentLoaded', function () {

    /**
     * 2. KHỞI TẠO SWIPER
     */
    var swiper = new Swiper(".myTestimonialSwiper", {
        loop: true,
        speed: 800,

        // --- QUAN TRỌNG: FIX LỖI WIDTH BỊ NHỎ / VỠ LAYOUT ---
        // Giúp Swiper tự cập nhật lại khi container cha thay đổi kích thước hoặc hiển thị (do AOS)
        observer: true,
        observeParents: true,
        // ----------------------------------------------------

        // Tự động chạy
        autoplay: {
            delay: 4000,
            disableOnInteraction: false,
            pauseOnMouseEnter: true,
        },

        // Dấu chấm phân trang
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
            dynamicBullets: true,
        },

        // Cấu hình Responsive (Tự thay đổi theo màn hình)
        breakpoints: {
            // Mobile: 1 Slide
            0: {
                slidesPerView: 1,
                spaceBetween: 20,
            },
            // Tablet: 2 Slides
            768: {
                slidesPerView: 1,
                spaceBetween: 30,
            },
            // Desktop: 3 Slides
            1024: {
                slidesPerView: 2,
                spaceBetween: 30,
            },
            // Màn hình lớn: 3 Slides rộng rãi hơn
            1200: {
                slidesPerView: 3,
                spaceBetween: 30,
            }
        },
    });
});