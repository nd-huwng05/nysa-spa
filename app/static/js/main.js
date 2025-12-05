(function () {
    "use strict";

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

    // Tự động đóng menu khi click vào link bên trong
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

    document.addEventListener('DOMContentLoaded', function () {

        const scrollTop = document.querySelector('.scroll-top');

        if (scrollTop) {
            // Hàm kiểm tra vị trí cuộn để hiện/ẩn nút
            const togglescrollTop = () => {
                if (window.scrollY > 100) {
                    scrollTop.classList.add('active');
                } else {
                    scrollTop.classList.remove('active');
                }
            }

            // Lắng nghe sự kiện khi tải trang và khi cuộn
            window.addEventListener('load', togglescrollTop);
            document.addEventListener('scroll', togglescrollTop);

            // Xử lý sự kiện click để cuộn mượt mà lên đầu
            scrollTop.addEventListener('click', (e) => {
                e.preventDefault(); // Ngăn chặn hành động mặc định của thẻ a
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth' // Hiệu ứng trượt mượt
                });
            });
        }
    });


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
})();