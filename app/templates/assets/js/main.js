(function () {
    "use strict";

    function toggleScrolled() {
        const selectBody = document.querySelector('body');
        const selectHeader = document.querySelector('#header');
        if (!selectHeader || (!selectHeader.classList.contains('scroll-up-sticky') && !selectHeader.classList.contains('sticky-top') && !selectHeader.classList.contains('fixed-top'))) return;

        window.scrollY > 100 ? selectBody.classList.add('scrolled') : selectBody.classList.remove('scrolled');
    }

    document.addEventListener('scroll', toggleScrolled);
    window.addEventListener('load', toggleScrolled);

    const mobileNavToggleBtn = document.querySelector('.mobile-nav-toggle');

    function mobileNavToggle() {
        document.body.classList.toggle('mobile-nav-active');
        mobileNavToggleBtn.classList.toggle('bi-list');
        mobileNavToggleBtn.classList.toggle('bi-x');
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
})();