function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('mobile-open');
}

function toggleNotification(event) {
    event.stopPropagation();

    const notifMenu = document.getElementById('notification-menu');
    const userMenu = document.getElementById('user-menu');

    if (userMenu) userMenu.classList.remove('show');
    if (notifMenu) notifMenu.classList.toggle('show');
}
function toggleUserDropdown(event) {
    event.stopPropagation();

    const notifMenu = document.getElementById('notification-menu');
    const userMenu = document.getElementById('user-menu');
    if (notifMenu) notifMenu.classList.remove('show');

    if (userMenu) userMenu.classList.toggle('show');
}

window.onclick = function (event) {
    const notifMenu = document.getElementById('notification-menu');
    const userMenu = document.getElementById('user-menu');
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.querySelector('.lg\\:hidden'); // Nút menu mobile

    if (notifMenu && notifMenu.classList.contains('show')) {
        if (!notifMenu.contains(event.target)) {
            notifMenu.classList.remove('show');
        }
    }

    if (userMenu && userMenu.classList.contains('show')) {
        if (!userMenu.contains(event.target)) {
            userMenu.classList.remove('show');
        }
    }

    if (window.innerWidth <= 1024 && sidebar.classList.contains('mobile-open')) {
        if (!sidebar.contains(event.target) && !event.target.closest('button[onclick="toggleSidebar()"]')) {
            sidebar.classList.remove('mobile-open');
        }
    }
}
