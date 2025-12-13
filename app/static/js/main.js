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

    document.addEventListener('DOMContentLoaded', function () {

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

        if (typeof AOS !== 'undefined') {
            AOS.init({
                duration: 800,
                easing: 'ease-in-out',
                once: true,
                mirror: false
            });
        }
    });

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

    document.addEventListener('DOMContentLoaded', function () {
        const addButtons = document.querySelectorAll('.add-to-cart-btn');
        const deleteButtons = document.querySelectorAll('.delete-service-from-cart');

        addButtons.forEach(btn => {
            btn.addEventListener('click', function (e) {
                e.preventDefault()
                const serviceId = this.dataset.serviceId;

                flyToCart(this, () => {
                    addServiceToCart(serviceId, (success) => {
                        if (success) {updateCartVisuals(1);}
                        else {alert('Add service failed')}
                    })
                });
            });
        });

        function addServiceToCart(serviceId, callback) {
            fetch(`/cart/add/${serviceId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            }).then(response => {
                if (response.ok) {
                    callback(true);
                } else {
                    callback(false);
                }
            }).catch(error => {
                console.error('Error adding item:', error);
                callback(false);
            });
        }

        deleteButtons.forEach(btn => {
            btn.addEventListener('click', function (e) {
                e.preventDefault()
                const serviceId = this.dataset.serviceId;

                removeItemFromCart(serviceId, (success) => {
                    if(success) {
                        const itemRow = this.closest('.cart-item-row');
                        if (itemRow) itemRow.remove();
                        updateCartVisuals(-1);
                    } else {
                        alert("Delete service failed")
                    }
                })
            });
        });

        function removeItemFromCart(serviceId, callback) {
            fetch(`/cart/remove/${serviceId}`, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                }
            }).then(response => {
                if(response.ok) {
                    callback(true);
                } else {
                    callback(false);
                }
            }).catch(error => {
                console.error('Error removing item:', error);
                callback(false);
            });
        }

        function flyToCart(sourceBtn, onComplete) {
            const cartBtn = document.getElementById('header-cart-btn');
            if (!cartBtn) return onComplete();

            const flyingBall = document.createElement('div');
            flyingBall.classList.add('fly-item');
            document.body.appendChild(flyingBall);

            const startRect = sourceBtn.getBoundingClientRect();
            flyingBall.style.top = `${startRect.top + startRect.height / 2}px`;
            flyingBall.style.left = `${startRect.left + startRect.width / 2}px`;

            setTimeout(() => {
                const endRect = cartBtn.getBoundingClientRect();
                flyingBall.style.top = `${endRect.top + endRect.height / 2 - 10}px`;
                flyingBall.style.left = `${endRect.left + endRect.width / 2 - 10}px`;
                flyingBall.style.transform = 'scale(0.2)';
                flyingBall.style.opacity = '0.5';
            }, 10);

            setTimeout(() => {
                flyingBall.remove();
                if (onComplete) onComplete();
            }, 800);
        }

        function updateCartVisuals(change) {
            const cartBtn = document.getElementById('header-cart-btn');
            const cartBadge = document.getElementById('lblCartCount');

            if (!cartBtn) return;

            cartBtn.classList.add('cart-shake-active');

            if (cartBadge) {
                let currentVal = parseInt(cartBadge.innerText);
                if (isNaN(currentVal)) currentVal = 0;
                cartBadge.innerText = currentVal + change;
            }

            setTimeout(() => {
                cartBtn.classList.remove('cart-shake-active');
            }, 500);
        }
    });
})();