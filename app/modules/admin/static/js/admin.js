function toggleUserDropdown() {
    const dropdown = document.getElementById('user-dropdown-menu');
    dropdown.classList.toggle('hidden');
}

window.addEventListener('click', function (e) {
    const dropdown = document.getElementById('user-dropdown-menu');
    const button = document.querySelector('button[onclick="toggleUserDropdown()"]');

    if (!dropdown.contains(e.target) && !button.contains(e.target)) {
        dropdown.classList.add('hidden');
    }
});