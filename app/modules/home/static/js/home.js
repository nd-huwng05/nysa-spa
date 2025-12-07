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