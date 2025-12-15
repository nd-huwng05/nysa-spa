(function () {
        "use strict";

        var isAnchor = window.location.hash;

        if (history.scrollRestoration) {
            if (isAnchor) {
                history.scrollRestoration = 'auto';
            } else {
                history.scrollRestoration = 'manual';
            }
        }

        window.addEventListener('load', function () {
            if (!isAnchor) {
                window.scrollTo(0, 0);
            }
        });

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

        function addServiceToCart(serviceId, callback) {
            fetch(`/cart/add/${serviceId}`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            })
                .then(response => callback(response.ok))
                .catch(error => {
                    console.error('Error adding item:', error);
                    callback(false);
                });
        }

        function removeItemFromCart(serviceId, callback) {
            fetch(`/cart/remove/${serviceId}`, {
                method: "POST",
                headers: {'Content-Type': 'application/json'}
            })
                .then(response => callback(response.ok))
                .catch(error => {
                    console.error('Error removing item:', error);
                    callback(false);
                });
        }

        function flyToCart(sourceBtn, onComplete) {
            const cartBtn = document.getElementById('header-cart-btn');
            if (!cartBtn) {
                if (onComplete) onComplete();
                return;
            }

            const flyingBall = document.createElement('div');
            flyingBall.classList.add('fly-item');
            document.body.appendChild(flyingBall);

            const startRect = sourceBtn.getBoundingClientRect();
            flyingBall.style.top = `${startRect.top + startRect.height / 2}px`;
            flyingBall.style.left = `${startRect.left + startRect.width / 2}px`;


            requestAnimationFrame(() => {
                const endRect = cartBtn.getBoundingClientRect();
                flyingBall.style.top = `${endRect.top + endRect.height / 2 - 10}px`;
                flyingBall.style.left = `${endRect.left + endRect.width / 2 - 10}px`;
                flyingBall.style.transform = 'scale(0.2)';
                flyingBall.style.opacity = '0.5';
            });

            setTimeout(() => {
                flyingBall.remove();
                if (onComplete) onComplete();
            }, 800);
        }

        var globalCartCount = 0;
        document.addEventListener('DOMContentLoaded', function () {
            const cartBadge = document.getElementById('lblCartCount');
            if (cartBadge) {
                globalCartCount = parseInt(cartBadge.innerText) || 0;
            }
        });


        function updateCartVisuals(change) {
            const cartBtn = document.getElementById('header-cart-btn');
            const cartBadge = document.getElementById('lblCartCount');

            globalCartCount += change;
            if (globalCartCount < 0) {
                globalCartCount = 0;

                if (globalCartCount === 0) {
                    cartBadge.style.display = 'none';
                } else {
                    cartBadge.style.display = 'block';
                }
            }

            if (cartBadge) {
                cartBadge.innerText = Math.max(0, globalCartCount);
                setTimeout(() => {
                    cartBtn.classList.remove('cart-shake-active');
                }, 500);
            }
        }


        document.addEventListener('DOMContentLoaded', function () {

            document.body.addEventListener('click', function (e) {

                const addBtn = e.target.closest('.add-to-cart-btn');

                if (addBtn) {
                    e.preventDefault();
                    const serviceId = addBtn.dataset.serviceId;

                    flyToCart(addBtn, () => {
                        addServiceToCart(serviceId, (success) => {
                            if (success) {
                                updateCartVisuals(1);
                            } else {
                                alert('Add service failed');
                            }
                        });
                    });
                    return;
                }

                const delBtn = e.target.closest('.delete-service-from-cart');

                if (delBtn) {
                    e.preventDefault();
                    const serviceId = delBtn.dataset.serviceId;

                    removeItemFromCart(serviceId, (success) => {
                        if (success) {
                            const itemRow = delBtn.closest('.cart-item-row');
                            if (itemRow) itemRow.remove();
                            updateCartVisuals(-1);
                        } else {
                            alert("Delete service failed");
                        }
                    });
                }
            });
        });
    }
)
();