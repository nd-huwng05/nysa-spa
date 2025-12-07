(function () {
  "use strict";

  /* --- NAVIGATION & LAYOUT --- */
  const mobileNavToggleBtn = document.querySelector('.mobile-nav-toggle');

  function mobileNavToggle() {
    document.body.classList.toggle('mobile-nav-active');
    mobileNavToggleBtn.classList.toggle('bi-list');
    mobileNavToggleBtn.classList.toggle('bi-x');

    if (document.body.classList.contains('mobile-nav-active')) {
      document.body.classList.remove('scrolled');
    } else {
      document.body.classList.add('scrolled');
    }
  }

  if (mobileNavToggleBtn) {
    mobileNavToggleBtn.addEventListener('click', mobileNavToggle);
  }

  document.querySelectorAll('#navmenu a').forEach(navLink => {
    navLink.addEventListener('click', () => {
      if (document.body.classList.contains('mobile-nav-active')) {
        mobileNavToggle();
      }
    });
  });

  document.querySelectorAll('.navmenu .toggle-dropdown').forEach(toggleBtn => {
    toggleBtn.addEventListener('click', function (e) {
      e.preventDefault();
      const parentLi = this.parentNode;
      parentLi.classList.toggle('active');
      const submenu = parentLi.querySelector('ul');
      if (submenu) submenu.classList.toggle('dropdown-active');
      e.stopImmediatePropagation();
    });
  });

  /* --- SCROLLSPY --- */
  let navmenulinks = document.querySelectorAll('.navmenu a');

  function navmenuScrollspy() {
    navmenulinks.forEach(navmenulink => {
      if (!navmenulink.hash) return;
      let section = document.querySelector(navmenulink.hash);
      if (!section) return;
      let position = window.scrollY + 200;
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        document.querySelectorAll('.navmenu a.active').forEach(link => link.classList.remove('active'));
        navmenulink.classList.add('active');
      } else {
        navmenulink.classList.remove('active');
      }
    })
  }
  window.addEventListener('load', navmenuScrollspy);
  document.addEventListener('scroll', navmenuScrollspy);

  /* --- DOM CONTENT LOADED --- */
  document.addEventListener('DOMContentLoaded', function () {

    // Scroll Top Button
    const scrollTop = document.querySelector('.scroll-top');
    if (scrollTop) {
      const togglescrollTop = () => {
        if (window.scrollY > 100) {
          scrollTop.classList.add('active');
        } else {
          scrollTop.classList.remove('active');
        }
      }
      window.addEventListener('load', togglescrollTop);
      document.addEventListener('scroll', togglescrollTop);
      scrollTop.addEventListener('click', (e) => {
        e.preventDefault();
        window.scrollTo({
          top: 0,
          behavior: 'smooth'
        });
      });
    }

    // Init AOS (Global Animation)
    if (typeof AOS !== 'undefined') {
      AOS.init({
        duration: 1000,
        easing: 'ease-in-out',
        once: true,
        mirror: false
      });
    }
  });

  /* --- GLOBAL SWIPER CONFIG --- */
  function initSwiper() {
    document.querySelectorAll(".init-swiper").forEach(function (swiperElement) {
      let config = JSON.parse(
        swiperElement.querySelector(".swiper-config").innerHTML.trim()
      );
      if (swiperElement.classList.contains("swiper-tab")) {
        initSwiperWithCustomPagination(swiperElement, config);
      } else {
        new Swiper(swiperElement, config);
      }
    });
  }
  window.addEventListener("load", initSwiper);

})();